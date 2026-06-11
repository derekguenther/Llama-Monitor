"""System metrics collector using Windows performance counters."""

import time
from typing import Any, Dict, List, Optional

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
    """Collects system metrics (CPU, GPU, memory) on Windows."""

    def __init__(self, tracked_processes: Optional[List[str]] = None):
        """Initialize the collector.

        Args:
            tracked_processes: List of process names to track specifically
        """
        self.tracked_processes = tracked_processes or ["llama-server.exe"]

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

        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_cores = psutil.cpu_percent(interval=0.1, percpu=True)
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

    def _get_cpu_power_w(self) -> float:
        """Get CPU package power from Energy Meter performance counter.

        Uses PowerShell's Get-Counter to query the Energy Meter counter set.
        Returns power in watts, or 0.0 if not available.

        Returns:
            CPU package power in watts
        """
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

    def _collect_system_power(self) -> Dict[str, Any]:
        """Collect system power consumption.

        Returns:
            Dictionary with system power data
        """
        result = {}

        # Get CPU/package power from Energy Meter performance counter
        cpu_power_w = self._get_cpu_power_w()
        if cpu_power_w > 0:
            result["cpu_power_w"] = cpu_power_w
            result["system_power_w"] = cpu_power_w  # System power equals CPU package power

        # Try WMI for additional power data
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
