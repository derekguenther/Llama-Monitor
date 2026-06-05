#!/usr/bin/env python3
"""Unit tests for system_metrics.py."""

import unittest
from unittest.mock import Mock, patch, MagicMock

from system_metrics import SystemMetricsCollector


class TestSystemMetricsCollectorInit(unittest.TestCase):
    """Tests for SystemMetricsCollector initialization."""

    def test_init_default_tracked_processes(self):
        """Test default tracked processes."""
        collector = SystemMetricsCollector()
        self.assertEqual(collector.tracked_processes, ["llama-server.exe"])

    def test_init_custom_tracked_processes(self):
        """Test custom tracked processes."""
        collector = SystemMetricsCollector(tracked_processes=["test.exe", "another.exe"])
        self.assertEqual(collector.tracked_processes, ["test.exe", "another.exe"])

    @patch("system_metrics.wmi")
    def test_init_with_wmi(self, mock_wmi):
        """Test initialization with WMI available."""
        mock_wmi_instance = Mock()
        mock_wmi.WMI.return_value = mock_wmi_instance

        with patch("system_metrics.wmi", mock_wmi):
            collector = SystemMetricsCollector()
            self.assertEqual(collector.wmi, mock_wmi_instance)

    @patch("system_metrics.wmi")
    def test_init_wmi_exception(self, mock_wmi):
        """Test initialization when WMI raises exception."""
        mock_wmi.WMI.side_effect = Exception("WMI error")

        with patch("system_metrics.wmi", mock_wmi):
            collector = SystemMetricsCollector()
            # Should not crash, wmi should remain None
            self.assertIsNone(collector.wmi)


class TestContextManager(unittest.TestCase):
    """Tests for context manager functionality."""

    def test_enter_returns_self(self):
        """Test __enter__ returns self."""
        collector = SystemMetricsCollector()
        result = collector.__enter__()
        self.assertIs(result, collector)

    @patch("system_metrics.nvml")
    def test_exit_calls_close(self, mock_nvml):
        """Test __exit__ calls close."""
        mock_nvml.nvmlInit.return_value = None
        collector = SystemMetricsCollector()
        collector.nvml_init = True
        collector.nvml = mock_nvml

        collector.__exit__(None, None, None)

        mock_nvml.nvmlShutdown.assert_called_once()


class TestCollectCPU(unittest.TestCase):
    """Tests for CPU metrics collection."""

    @patch("system_metrics.psutil")
    def test_collect_cpu_success(self, mock_psutil):
        """Test successful CPU metrics collection."""
        mock_psutil.cpu_percent.side_effect = [50.0, [45.0] * 8]
        mock_psutil.cpu_count.return_value = 8
        mock_psutil.process_iter.return_value = [
            Mock(info={"pid": 1234, "name": "llama-server.exe", "cpu_percent": 25.0}),
            Mock(info={"pid": 5678, "name": "other.exe", "cpu_percent": 10.0}),
        ]

        collector = SystemMetricsCollector()
        result = collector._collect_cpu()

        self.assertEqual(result["percent"], 50.0)
        self.assertEqual(result["cores"], [45.0] * 8)
        self.assertEqual(result["count"], 8)
        self.assertIn("llama-server.exe", result["process_cpu"])
        self.assertEqual(result["process_cpu"]["llama-server.exe"]["pid"], 1234)
        self.assertEqual(result["process_cpu"]["llama-server.exe"]["cpu_percent"], 25.0)

    @patch("system_metrics.psutil")
    def test_collect_cpu_no_psutil(self, mock_psutil):
        """Test CPU collection when psutil is not available."""
        mock_psutil.cpu_percent.side_effect = ImportError("psutil not found")

        collector = SystemMetricsCollector()
        # Temporarily set psutil to None
        original_psutil = collector.__class__.__module__
        with patch.dict("sys.modules", {"psutil": None}):
            # Reimport to get fresh module
            import importlib
            import system_metrics
            importlib.reload(system_metrics)
            collector = system_metrics.SystemMetricsCollector()
            result = collector._collect_cpu()
            self.assertEqual(result["error"], "psutil not installed")

    def test_collect_cpu_process_filtering(self):
        """Test that only tracked processes are included."""
        mock_proc1 = Mock()
        mock_proc1.info = {"pid": 1234, "name": "llama-server.exe", "cpu_percent": 25.0}
        mock_proc2 = Mock()
        mock_proc2.info = {"pid": 5678, "name": "not-tracked.exe", "cpu_percent": 10.0}
        mock_proc3 = Mock()
        mock_proc3.info = {"pid": 9012, "name": "llama-server.exe", "cpu_percent": 15.0}

        with patch("system_metrics.psutil") as mock_psutil:
            mock_psutil.cpu_percent.return_value = 50.0
            mock_psutil.cpu_count.return_value = 4
            mock_psutil.process_iter.return_value = [mock_proc1, mock_proc2, mock_proc3]

            collector = SystemMetricsCollector()
            result = collector._collect_cpu()

            # Should only include llama-server.exe processes
            self.assertIn("llama-server.exe", result["process_cpu"])
            self.assertNotIn("not-tracked.exe", result["process_cpu"])

    def test_collect_cpu_process_exception_handling(self):
        """Test handling of process access exceptions."""
        mock_proc = Mock()
        mock_proc.info = {"pid": 1234, "name": "llama-server.exe", "cpu_percent": None}

        with patch("system_metrics.psutil") as mock_psutil:
            mock_psutil.cpu_percent.return_value = 50.0
            mock_psutil.cpu_count.return_value = 4
            mock_psutil.process_iter.return_value = [mock_proc]

            collector = SystemMetricsCollector()
            result = collector._collect_cpu()

            # None cpu_percent should default to 0.0
            self.assertEqual(result["process_cpu"]["llama-server.exe"]["cpu_percent"], 0.0)


class TestCollectGPU(unittest.TestCase):
    """Tests for GPU metrics collection."""

    @patch("system_metrics.nvml")
    def test_collect_gpu_nvml_success(self, mock_nvml):
        """Test GPU metrics collection with NVML."""
        mock_nvml.nvmlInit.return_value = None
        mock_nvml.nvmlDeviceGetCount.return_value = 1

        mock_handle = Mock()
        mock_nvml.nvmlDeviceGetHandleByIndex.return_value = mock_handle

        mock_util = Mock()
        mock_util.gpu = 85
        mock_util.memory = 70
        mock_nvml.nvmlDeviceGetUtilizationRates.return_value = mock_util

        mock_mem = Mock()
        mock_mem.used = 8589934592  # 8 GB
        mock_mem.total = 17179869184  # 16 GB
        mock_nvml.nvmlDeviceGetMemoryInfo.return_value = mock_mem

        mock_nvml.NVML_TEMPERATURE_GPU = 0
        mock_nvml.nvmlDeviceGetTemperature.return_value = 75

        mock_nvml.nvmlDeviceGetFanSpeed.return_value = 2500

        mock_nvml.nvmlDeviceGetPowerUsage.return_value = 220000  # 220 W

        collector = SystemMetricsCollector()
        collector.nvml_init = True
        collector.nvml = mock_nvml

        result = collector._collect_gpu()

        self.assertEqual(result["usage"], 85)
        self.assertEqual(result["memory_usage"], 70)
        self.assertEqual(result["memory_used"], 8192)
        self.assertEqual(result["memory_total"], 16384)
        self.assertEqual(result["temperature_c"], 75)
        self.assertEqual(result["fan_speed_rpm"], 2500)
        self.assertEqual(result["power_w"], 220.0)

    @patch("system_metrics.nvml")
    def test_collect_gpu_no_gpus(self, mock_nvml):
        """Test GPU collection when no GPUs found."""
        mock_nvml.nvmlInit.return_value = None
        mock_nvml.nvmlDeviceGetCount.return_value = 0

        collector = SystemMetricsCollector()
        collector.nvml_init = True
        collector.nvml = mock_nvml

        result = collector._collect_gpu()

        self.assertEqual(result["error"], "No NVIDIA GPUs found")

    @patch("system_metrics.wmi")
    def test_collect_gpu_wmi(self, mock_wmi):
        """Test GPU metrics collection with WMI."""
        mock_gpu = Mock()
        mock_gpu.AdapterCompatibility = "NVIDIA"
        mock_gpu.AdapterRAM = 17179869184  # 16 GB
        mock_gpu.Description = "NVIDIA GeForce RTX 3080"
        mock_gpu.DriverVersion = "527.41"
        mock_gpu.Name = "NVIDIA GeForce RTX 3080"
        mock_gpu.VideoMemoryBudget = 16384

        mock_perf = Mock()
        mock_perf.PercentProcessorTime = 85

        mock_wmi_instance = Mock()
        mock_wmi_instance.Win32_VideoController.return_value = [mock_gpu]
        mock_wmi_instance.Win32_PerfFormattedDataGPUProfile.return_value = [mock_perf]
        mock_wmi.WMI.return_value = mock_wmi_instance

        with patch("system_metrics.wmi", mock_wmi):
            collector = SystemMetricsCollector()
            collector.wmi = mock_wmi_instance

            result = collector._collect_gpu()

            self.assertEqual(result["name"], "NVIDIA GeForce RTX 3080")
            self.assertEqual(result["usage"], 85)

    def test_collect_gpu_no_monitoring_available(self):
        """Test GPU collection when no monitoring library is available."""
        collector = SystemMetricsCollector()
        collector.nvml_init = False
        collector.wmi = None

        result = collector._collect_gpu()

        self.assertEqual(result["error"], "No GPU monitoring library available")


class TestCollectMemory(unittest.TestCase):
    """Tests for memory metrics collection."""

    def test_collect_memory_success(self):
        """Test successful memory metrics collection."""
        collector = SystemMetricsCollector()
        result = collector._collect_memory()

        # Check that result contains expected keys
        self.assertIn("used", result)
        self.assertIn("total", result)
        self.assertIn("percent", result)
        self.assertIn("available", result)

        # Values should be positive integers
        self.assertIsInstance(result["used"], int)
        self.assertIsInstance(result["total"], int)
        self.assertIsInstance(result["percent"], float)
        self.assertIsInstance(result["available"], int)

        # Values should be non-negative
        self.assertGreaterEqual(result["used"], 0)
        self.assertGreaterEqual(result["total"], 0)
        self.assertGreaterEqual(result["percent"], 0)
        self.assertGreaterEqual(result["available"], 0)


class TestCollectProcessGPU(unittest.TestCase):
    """Tests for per-process GPU metrics collection."""

    @patch("system_metrics.psutil")
    @patch("system_metrics.nvml")
    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
        """Test successful per-process GPU metrics collection."""
        mock_nvml.nvmlDeviceGetCount.return_value = 1

        mock_handle = Mock()
        mock_nvml.nvmlDeviceGetHandleByIndex.return_value = mock_handle

        mock_proc = Mock()
        mock_proc.pid = 1234
        mock_proc.gpuUtilization = 85
        mock_proc.memSize = 8589934592  # 8 GB

        mock_nvml.nvmlDeviceGetGraphicsRunningProcesses_v2.return_value = [mock_proc]

        mock_process = Mock()
        mock_process.name.return_value = "llama-server.exe"
        mock_process.memory_info.return_value = Mock(rss=4294967296, vms=2147483648)  # 4GB RSS, 2GB VMS
        mock_psutil.Process.return_value = mock_process

        collector = SystemMetricsCollector()
        collector.nvml_init = True
        collector.nvml = mock_nvml

        result = collector._collect_process_gpu()

        self.assertIn("llama-server.exe", result)
        self.assertEqual(result["llama-server.exe"]["pid"], 1234)
        self.assertEqual(result["llama-server.exe"]["gpu_utilization"], 85)
        self.assertEqual(result["llama-server.exe"]["gpu_memory_mb"], 8192)
        self.assertEqual(result["llama-server.exe"]["ram_rss_mb"], 4096)

    @patch("system_metrics.nvml")
    def test_collect_process_gpu_no_nvml(self, mock_nvml):
        """Test per-process GPU collection when NVML is not initialized."""
        collector = SystemMetricsCollector()
        collector.nvml_init = False
        collector.nvml = None

        result = collector._collect_process_gpu()

        self.assertEqual(result, {})

    @patch("system_metrics.nvml")
    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
        """Test fallback to v1 API when v2 is not available."""
        mock_nvml.nvmlDeviceGetCount.return_value = 1

        mock_handle = Mock()
        mock_nvml.nvmlDeviceGetHandleByIndex.return_value = mock_handle

        # v2 raises AttributeError, v1 returns data
        mock_nvml.nvmlDeviceGetGraphicsRunningProcesses_v2.side_effect = AttributeError
        mock_nvml.nvmlDeviceGetGraphicsRunningProcesses.return_value = []

        collector = SystemMetricsCollector()
        collector.nvml_init = True
        collector.nvml = mock_nvml

        result = collector._collect_process_gpu()

        # Should not raise exception, should return empty
        self.assertEqual(result, {})


class TestCollectSystemPower(unittest.TestCase):
    """Tests for system power metrics collection."""

    @patch("system_metrics.wmi")
    def test_collect_system_power_battery(self, mock_wmi):
        """Test system power collection with battery data."""
        mock_battery = Mock()
        mock_battery.EstimatedChargeRemaining = 85

        mock_wmi_instance = Mock()
        mock_wmi_instance.Win32_Battery.return_value = [mock_battery]
        mock_wmi.WMI.return_value = mock_wmi_instance

        with patch("system_metrics.wmi", mock_wmi):
            collector = SystemMetricsCollector()
            collector.wmi = mock_wmi_instance

            result = collector._collect_system_power()

            self.assertEqual(result["battery_percent"], 85)

    @patch("system_metrics.wmi")
    def test_collect_system_power_no_battery(self, mock_wmi):
        """Test system power collection without battery data."""
        mock_wmi_instance = Mock()
        mock_wmi_instance.Win32_Battery.return_value = []
        mock_wmi.WMI.return_value = mock_wmi_instance

        with patch("system_metrics.wmi", mock_wmi):
            collector = SystemMetricsCollector()
            collector.wmi = mock_wmi_instance

            result = collector._collect_system_power()

            self.assertEqual(result, {})


class TestCollect(unittest.TestCase):
    """Tests for main collect method."""

    @patch("test_system_metrics.SystemMetricsCollector._collect_cpu")
    @patch("test_system_metrics.SystemMetricsCollector._collect_gpu")
    @patch("test_system_metrics.SystemMetricsCollector._collect_memory")
    @patch("test_system_metrics.SystemMetricsCollector._collect_process_gpu")
    @patch("test_system_metrics.SystemMetricsCollector._collect_system_power")
    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
        """Test full metrics collection."""
        mock_cpu.return_value = {"percent": 50.0}
        mock_gpu.return_value = {"usage": 85.0}
        mock_memory.return_value = {"percent": 50.0}
        mock_process_gpu.return_value = {}
        mock_system_power.return_value = {}

        collector = SystemMetricsCollector()
        result = collector.collect()

        self.assertIn("timestamp", result)
        self.assertIn("cpu", result)
        self.assertIn("gpu", result)
        self.assertIn("memory", result)
        self.assertIn("process_gpu", result)
        self.assertIn("system", result)

        mock_cpu.assert_called_once()
        mock_gpu.assert_called_once()
        mock_memory.assert_called_once()
        mock_process_gpu.assert_called_once()
        mock_system_power.assert_called_once()


if __name__ == "__main__":
    unittest.main()
