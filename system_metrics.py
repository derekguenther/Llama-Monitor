"""System metrics collector using Windows performance counters and Linux power monitoring.

Windows: Uses Energy Meter performance counter for CPU power, WMI for battery.
Linux: Uses RAPL (/sys/class/powercap/intel-rapl:*) for CPU power when available.
        Falls back to 0.0 if RAPL not available (requires lm-sensors or NVML for GPU).
"""

import time
import os
import sys
import csv
import subprocess
import tempfile
import threading
from typing import Any, Dict, List, Optional

IS_WINDOWS = sys.platform == "win32"

try:
    import psutil
except ImportError:
    psutil = None

try:
    import wmi
except ImportError:
    wmi = None

try:
    import nvml_wrapper as nvmlw
except ImportError:
    try:
        import pynvml as nvml
    except ImportError:
        nvml = None


class SystemMetricsCollector:
    """Collects system metrics (CPU, GPU, memory) on Windows and Linux."""

    def __init__(
        self,
        tracked_processes: Optional[List[str]] = None,
        polling_interval: float = 1.0,
    ):
        """Initialize the collector.

        Args:
            tracked_processes: List of process names to track specifically
            polling_interval: How often (seconds) the aggregator polls metrics.
                On Windows this drives the background typeperf sampling cadence
                so CPU power is captured at the same rate as the rest of the
                software (e.g. 1s by default) without spawning a PowerShell
                subprocess on every read.
        """
        self.tracked_processes = tracked_processes or ["llama-server.exe"]
        self.polling_interval = max(0.1, float(polling_interval))

        # Background typeperf process (Windows only) for CPU power reads.
        self._typeperf_proc: Optional[subprocess.Popen] = None
        self._typeperf_csv: Optional[str] = None
        self._typeperf_lock = threading.RLock()

        # Initialize NVML if available
        self.nvml_init = False
        self.nvml = None
        self._init_nvml()

        # Initialize WMI if available
        self.wmi = None
        if wmi:
            try:
                self.wmi = wmi.WMI()
            except Exception:
                pass

        # Start the background typeperf logger (best-effort; no-op on Linux).
        self._start_typeperf()

    def _init_nvml(self) -> bool:
        """Initialize NVML library.

        Returns:
            True if initialization successful
        """
        if nvml is None:
            return False

        try:
            nvml.nvmlInit()
            self.nvml = nvml
            self.nvml_init = True
            return True
        except Exception:
            self.nvml_init = False
            return False

    def close(self) -> None:
        """Cleanup resources."""
        # Terminate the background typeperf process if running.
        if self._typeperf_proc is not None:
            with self._typeperf_lock:
                try:
                    self._typeperf_proc.terminate()
                except Exception:
                    pass
                try:
                    self._typeperf_proc.wait(timeout=5)
                except Exception:
                    self._typeperf_proc.kill()
                self._typeperf_proc = None
        if self.nvml_init and self.nvml:
            try:
                self.nvml.nvmlShutdown()
            except Exception:
                pass

    def __enter__(self) -> "SystemMetricsCollector":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def _collect_process_ram(self) -> Dict[str, Any]:
        """Collect per-process RAM usage for tracked processes.

        Returns:
            Dictionary mapping process names to RAM metrics
        """
        result = {}

        if psutil is None:
            return {"error": "psutil not installed"}

        try:
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    name = proc.info["name"]
                    if name and any(
                        name.lower().endswith(proc_name.lower())
                        for proc_name in self.tracked_processes
                    ):
                        pid = proc.info["pid"]
                        process = psutil.Process(pid)
                        mem_info = process.memory_info()
                        result[name] = {
                            "pid": pid,
                            "ram_rss_mb": mem_info.rss // (1024 * 1024),
                            "ram_vms_mb": mem_info.vms // (1024 * 1024),
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            result["error"] = str(e)

        return result

    def collect(self) -> Dict[str, Any]:
        """Collect all system metrics.

        Returns:
            Dictionary with timestamped system metrics
        """
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

        result = {
            "timestamp": timestamp,
            "cpu": self._collect_cpu(),
            "gpu": self._collect_gpu(),
            "memory": self._collect_memory(),
            "process_gpu": self._collect_process_gpu(),
            "process_ram": self._collect_process_ram(),
            "system": self._collect_system_power(),
        }

        return result

    def _collect_cpu(self) -> Dict[str, Any]:
        """Collect CPU metrics.

        Returns:
            Dictionary with CPU metrics
        """
        if psutil is None:
            return {"error": "psutil not installed"}

        cpu_percent = psutil.cpu_percent()
        cpu_cores = psutil.cpu_percent(percpu=True)
        cpu_count = psutil.cpu_count(logical=True)

        # Get per-process CPU usage
        process_cpu = {}
        for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
            try:
                name = proc.info["name"]
                if name and any(
                    name.lower().endswith(proc_name.lower())
                    for proc_name in self.tracked_processes
                ):
                    process_cpu[name] = {
                        "pid": proc.info["pid"],
                        "cpu_percent": proc.info["cpu_percent"] or 0.0,
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return {
            "percent": cpu_percent,
            "cores": cpu_cores,
            "count": cpu_count,
            "process_cpu": process_cpu,
        }

    def _collect_gpu(self) -> Dict[str, Any]:
        """Collect GPU metrics.

        Returns:
            Dictionary with GPU metrics
        """
        result = {}

        # Try NVML first
        if self.nvml_init:
            result = self._collect_gpu_nvml()
        elif self.wmi:
            result = self._collect_gpu_wmi()
        else:
            result = {"error": "No GPU monitoring library available"}

        return result

    def _collect_gpu_nvml(self) -> Dict[str, Any]:
        """Collect GPU metrics using NVML.

        Returns:
            Dictionary with GPU metrics
        """
        result = {}

        try:
            device_count = self.nvml.nvmlDeviceGetCount()

            if device_count == 0:
                return {"error": "No NVIDIA GPUs found"}

            # Get first GPU for now (multi-GPU support can be added later)
            handle = self.nvml.nvmlDeviceGetHandleByIndex(0)

            # GPU utilization
            utilization = self.nvml.nvmlDeviceGetUtilizationRates(handle)
            result["usage"] = utilization.gpu
            result["memory_usage"] = utilization.memory

            # GPU memory
            memory_info = self.nvml.nvmlDeviceGetMemoryInfo(handle)
            result["memory_used"] = memory_info.used // (1024 * 1024)  # MB
            result["memory_total"] = memory_info.total // (1024 * 1024)  # MB

            # Temperature
            result["temperature_c"] = self.nvml.nvmlDeviceGetTemperature(
                handle, self.nvml.NVML_TEMPERATURE_GPU
            )

            # Fan speed
            try:
                result["fan_speed_rpm"] = self.nvml.nvmlDeviceGetFanSpeed(handle)
            except Exception:
                result["fan_speed_rpm"] = 0

            # Power usage
            try:
                result["power_w"] = self.nvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # W
            except Exception:
                result["power_w"] = 0.0

            # Clock speeds
            try:
                result["clock_graphics_mhz"] = self.nvml.nvmlDeviceGetClockInfo(
                    handle, self.nvml.NVML_CLOCK_GRAPHICS
                )
                result["clock_sm_mhz"] = self.nvml.nvmlDeviceGetClockInfo(
                    handle, self.nvml.NVML_CLOCK_SM
                )
                result["clock_memory_mhz"] = self.nvml.nvmlDeviceGetClockInfo(
                    handle, self.nvml.NVML_CLOCK_MEM
                )
            except Exception:
                pass

            # Power limit
            try:
                result["power_limit_w"] = self.nvml.nvmlDeviceGetPowerManagementLimit(
                    handle
                ) / 1000.0
            except Exception:
                pass

        except Exception as e:
            result["error"] = str(e)

        return result

    def _collect_gpu_wmi(self) -> Dict[str, Any]:
        """Collect GPU metrics using WMI.

        Returns:
            Dictionary with GPU metrics
        """
        result = {}

        try:
            # Get GPU information
            gpu = self.wmi.Win32_VideoController()[0]

            result["adapter_compatibility"] = gpu.AdapterCompatibility
            result["adapter_dac_type"] = gpu.AdapterDACType
            result["adapter_ram"] = gpu.AdapterRAM // (1024 * 1024)  # MB
            result["description"] = gpu.Description
            result["driver_version"] = gpu.DriverVersion
            result["name"] = gpu.Name
            result["video_memory"] = gpu.VideoMemoryBudget

            # Performance counters for utilization
            perf = self.wmi.Win32_PerfFormattedDataGPUProfile()
            if perf:
                result["usage"] = perf[0].PercentProcessorTime

        except Exception as e:
            result["error"] = str(e)

        return result

    def _collect_memory(self) -> Dict[str, Any]:
        """Collect memory metrics.

        Returns:
            Dictionary with memory metrics
        """
        try:
            import psutil
        except ImportError:
            return {"error": "psutil not installed"}

        mem = psutil.virtual_memory()

        return {
            "used": mem.used // (1024 * 1024),  # MB
            "total": mem.total // (1024 * 1024),  # MB
            "percent": mem.percent,
            "available": mem.available // (1024 * 1024),  # MB
        }

    def _collect_process_gpu(self) -> Dict[str, Any]:
        """Collect per-process GPU utilization.

        Returns:
            Dictionary mapping process names to GPU metrics
        """
        result = {}

        if not self.nvml_init:
            return result

        try:
            device_count = self.nvml.nvmlDeviceGetCount()

            for i in range(device_count):
                handle = self.nvml.nvmlDeviceGetHandleByIndex(i)

                # Get running graphics processes
                try:
                    procs = self.nvml.nvmlDeviceGetGraphicsRunningProcesses_v2(handle)
                except AttributeError:
                    # Fallback to v1 if v2 not available
                    try:
                        procs = self.nvml.nvmlDeviceGetGraphicsRunningProcesses(handle)
                    except Exception:
                        continue

                for proc in procs:
                    try:
                        pid = proc.pid
                        gpu_util = proc.gpuUtilization
                        mem_size = proc.memSize

                        # Try to get process name and RAM usage
                        try:
                            process = psutil.Process(pid)
                            process_name = process.name()
                            # Get process memory info (RSS = resident set size = actual RAM)
                            process_mem = process.memory_info()
                            ram_rss_mb = process_mem.rss // (1024 * 1024)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            process_name = f"pid_{pid}"
                            ram_rss_mb = 0

                        # Only track our tracked processes
                        if any(
                            process_name.lower().endswith(p.lower())
                            for p in self.tracked_processes
                        ):
                            result[process_name] = {
                                "pid": pid,
                                "gpu_utilization": gpu_util,
                                "gpu_memory_mb": mem_size // (1024 * 1024),
                                "ram_rss_mb": ram_rss_mb,
                            }
                    except Exception:
                        continue

        except Exception as e:
            result["error"] = str(e)

        return result

    def _start_typeperf(self) -> None:
        """Start a long-running background typeperf process (Windows only).

        typeperf writes the Energy Meter performance counter to a CSV file at
        ``polling_interval`` cadence, avoiding a per-read PowerShell spawn.
        The process is launched once and kept alive until ``close()``.

        The counter path is discovered at runtime (instance name varies, e.g.
        ``RAPL_Package0_PKG``), matching the ``*pkg*`` filter the old
        PowerShell Get-Counter command used. Best-effort: any failure leaves
        ``_typeperf_proc``/``_typeperf_csv`` unset so the reader falls back to
        the original PowerShell path.
        """
        if not IS_WINDOWS:
            return
        try:
            counter = self._discover_energy_meter_power_counter()
            if not counter:
                return

            fd, counters_path = tempfile.mkstemp(
                prefix="llama-monitor-counters-", suffix=".txt"
            )
            with os.fdopen(fd, "w") as f:
                f.write(counter + "\n")

            fd2, csv_path = tempfile.mkstemp(
                prefix="llama-monitor-typeperf-", suffix=".csv"
            )
            os.close(fd2)

            cmd = [
                "typeperf",
                "-cf",
                counters_path,
                "-si",
                str(int(round(self.polling_interval))),
                "-f",
                "CSV",
                "-o",
                csv_path,
                "-y",
            ]
            proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self._typeperf_proc = proc
            self._typeperf_csv = csv_path
        except Exception:
            # Fall back to the PowerShell path if typeperf cannot be launched.
            self._typeperf_proc = None
            self._typeperf_csv = None

    @staticmethod
    def _discover_energy_meter_power_counter() -> Optional[str]:
        r"""Discover the ``Energy Meter(*)\Power`` counter path at runtime.

        Runs ``typeperf -qx "Energy Meter"`` (a one-time startup cost) and
        returns a counter path whose instance matches ``pkg`` (the CPU package
        power), preferring ``_Total`` as a fallback. Returns None if discovery
        fails so the caller can fall back to the PowerShell read.
        """
        try:
            result = subprocess.run(
                ["typeperf", "-qx", "Energy Meter"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                return None
            pkg_candidate = None
            total_candidate = None
            for line in result.stdout.splitlines():
                line = line.strip()
                if not line.startswith("\\") or not line.endswith("\\Power"):
                    continue
                low = line.lower()
                if "energy meter" in low and "pkg" in low:
                    pkg_candidate = line
                if "energy meter" in low and "(_total)" in low:
                    total_candidate = line
            return pkg_candidate or total_candidate
        except Exception:
            return None

    def _read_typeperf_power(self) -> float:
        """Read the latest CPU package power (watts) from the typeperf CSV.

        Parses the counter-path header line (line 1) to locate the Energy Meter
        PKG Power column, then returns the value from the most recent data row.
        Energy Meter reports power in milliwatts, so it is converted to watts.
        Returns 0.0 on any failure so the caller can fall back.
        """
        if not self._typeperf_csv or not os.path.exists(self._typeperf_csv):
            return 0.0
        try:
            with open(
                self._typeperf_csv, "r", encoding="utf-8", errors="replace", newline=""
            ) as f:
                reader = csv.reader(f)
                # Row 0 is the PDH-CSV marker in column 0 plus the counter-path
                # header in columns 1+. It doubles as the header line.
                try:
                    header = next(reader)
                except StopIteration:
                    return 0.0

                pkg_col = None
                for i, name in enumerate(header):
                    low = name.lower()
                    if (
                        "energy meter" in low
                        and "pkg" in low
                        and low.rstrip().endswith("\\power")
                    ):
                        pkg_col = i
                        break
                if pkg_col is None:
                    return 0.0

                # Walk to the last data row and grab the PKG Power column.
                last_value = 0.0
                for row in reader:
                    if len(row) > pkg_col:
                        raw = row[pkg_col].strip()
                        if raw:
                            try:
                                last_value = float(raw)
                            except ValueError:
                                continue
                # Energy Meter reports milliwatts -> convert to watts.
                return last_value / 1000.0 if last_value else 0.0
        except Exception:
            return 0.0

    def _get_cpu_power_w(self) -> float:
        """Get CPU package power from the Energy Meter performance counter.

        Preferred: read the latest value from the long-running background
        typeperf CSV, which samples at ``polling_interval`` cadence without a
        per-read PowerShell spawn. If the typeperf logger is not available
        (non-Windows, startup failure, or process died), fall back to a direct
        PowerShell Get-Counter query.

        Returns:
            CPU package power in watts, or 0.0 if not available.
        """
        # Fast path: read from the background typeperf CSV (no subprocess spawn).
        with self._typeperf_lock:
            if self._typeperf_csv is not None and self._typeperf_proc is not None:
                # Restart the typeperf process if it died unexpectedly.
                if self._typeperf_proc.poll() is not None:
                    self.close()
                    self._start_typeperf()
                if self._typeperf_csv is not None:
                    return self._read_typeperf_power()

        # Fallback: direct PowerShell Get-Counter (one-off / non-Windows).
        try:
            import subprocess
            import re

            # Query the Energy Meter counter for CPU package power
            # Use PowerShell to query the Energy Meter performance counter
            powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
            counter_path = r"\Energy Meter(*)\Power"

            cmd = [
                powershell_path,
                "-Command",
                f'(Get-Counter "{counter_path}").CounterSamples | Where-Object {{ $_.InstanceName -like "*pkg*" }} | Select-Object -ExpandProperty CookedValue',
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                # Parse the numeric value from PowerShell output
                value_str = result.stdout.strip()
                match = re.match(r"[\d.]+", value_str)
                if match:
                    # Energy Meter returns power in milliwatts, convert to watts
                    return float(match.group()) / 1000.0

            return 0.0
        except Exception:
            return 0.0

    def _get_linux_cpu_power_w(self) -> float:
        """Get CPU package power from RAPL on Linux.

        Reads from /sys/class/powercap/intel-rapl:* for Intel CPU power.
        Returns power in watts, or 0.0 if not available.

        Returns:
            CPU package power in watts
        """
        if not os.path.exists('/sys/class/powercap/intel-rapl:0'):
            return 0.0

        try:
            # Try to read from the max_energy_range_uj file to get energy counter
            rapl_path = '/sys/class/powercap/intel-rapl:0'
            energy_uj_path = os.path.join(rapl_path, 'energy_uj')

            if not os.path.exists(energy_uj_path):
                return 0.0

            # Read current energy value
            with open(energy_uj_path, 'r') as f:
                energy_uj_1 = int(f.read().strip())

            # Wait a short time and read again
            time.sleep(0.5)

            with open(energy_uj_path, 'r') as f:
                energy_uj_2 = int(f.read().strip())

            # Calculate power (energy difference over time)
            energy_diff_uj = energy_uj_2 - energy_uj_1
            power_w = (energy_diff_uj / 1000000.0) / 0.5  # Convert to watts

            return max(0.0, power_w)
        except Exception:
            return 0.0

    def _collect_system_power(self) -> Dict[str, Any]:
        """Collect system power consumption.

        Returns:
            Dictionary with system power data
        """
        result = {}

        # Get CPU/package power
        # On Windows, use Energy Meter performance counter
        # On Linux, use RAPL or sensors as fallback
        cpu_power_w = self._get_cpu_power_w()
        
        # If Windows method returned 0 or negative, try Linux methods
        if cpu_power_w <= 0:
            cpu_power_w = self._get_linux_cpu_power_w()
        
        # Always set power values (0 for unavailable)
        result["cpu_power_w"] = cpu_power_w if cpu_power_w > 0 else 0.0
        result["system_power_w"] = cpu_power_w if cpu_power_w > 0 else 0.0

        # Try WMI for additional power data (Windows only)
        if self.wmi:
            try:
                # Use battery or power sensor data if available
                batteries = self.wmi.Win32_Battery()
                if batteries:
                    result["battery_percent"] = batteries[0].EstimatedChargeRemaining
            except Exception:
                pass

        return result


if __name__ == "__main__":
    # Test the collector
    collector = SystemMetricsCollector()

    print("Collecting system metrics...")
    data = collector.collect()

    import json

    print(json.dumps(data, indent=2))

    collector.close()
