#!/usr/bin/env python3
"""Unit tests for GPU/CPU Power (Filtered) calculation fix (bead 8rn).

The filtered power attributes llama.cpp's share of total GPU/CPU wattage. The
original formula had two bugs:
1. CPU scale mismatch: per-process cpu_percent from psutil is per-core scale
   (0-100 per core, can exceed 100), while the aggregator's cpu.percent is
   normalized to 0-100 across all cores. Summing raw per-process values for
   llamaCpuUtil and dividing by the already-normalized cpu.percent made the
   fraction wrong (it could exceed 1 and attribute 100% of CPU power to llama
   even when other processes used CPU). Fix: normalize llama's raw sum by the
   core count, and clamp the fraction to [0,1].
2. GPU: process_gpu requires NVML; without it the object is empty so
   hasProcessGpu is false and filtered GPU power stays 0 (correct, since we
   cannot attribute without per-process data). When NVML IS present, the
   fraction is clamped to [0,1].
"""

import os

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")


def _read_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()


def test_cpu_normalizes_per_core_scale():
    """llama's per-process CPU must be normalized by core count."""
    content = _read_template()
    update_idx = content.find("function updateDisplay")
    assert update_idx != -1, "updateDisplay not found"
    next_func = content.find("function ", update_idx + 20)
    section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    # Must capture core count
    assert "cpu.count || 1" in section, \
        "Missing cpu count for per-core normalization"
    assert "cpuCount > 0 ? llamaCpuUtil / cpuCount : llamaCpuUtil" in section, \
        "llamaCpuUtil not normalized by core count"
    print("[PASS] llama's per-process CPU normalized by core count")


def test_cpu_fraction_clamped_to_1():
    """The llama CPU fraction must be clamped to [0,1] to avoid over-attribution."""
    content = _read_template()
    update_idx = content.find("function updateDisplay")
    next_func = content.find("function ", update_idx + 20)
    section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    assert "Math.min(llamaCpuUtilNorm / cpuUtil, 1)" in section, \
        "CPU fraction not clamped to [0,1]"
    # The denominator must be the TRUE total OS CPU from system_raw, not the
    # aggregator's tracked-process-only cpu.percent.
    assert "data.system_raw?.cpu?.percent || cpu.percent || 0" in section, \
        "CPU denominator not using true total OS CPU"
    print("[PASS] CPU fraction clamped to [0,1] with true total OS CPU denominator")


def test_gpu_fraction_clamped_to_1():
    """The GPU fraction must be clamped to [0,1]."""
    content = _read_template()
    update_idx = content.find("function updateDisplay")
    next_func = content.find("function ", update_idx + 20)
    section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    assert "Math.min(llamaGpuUtil / gpuUtil, 1)" in section, \
        "GPU fraction not clamped to [0,1]"
    print("[PASS] GPU fraction clamped to [0,1]")


def test_gpu_requires_process_data():
    """Filtered GPU power must gate on per-process GPU data (NVML)."""
    content = _read_template()
    update_idx = content.find("function updateDisplay")
    next_func = content.find("function ", update_idx + 20)
    section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    assert "hasProcessGpu && validGpu && gpuUtil > 0" in section, \
        "Filtered GPU power must require per-process GPU data"
    print("[PASS] Filtered GPU power requires per-process GPU data")


def test_charts_section_normalizes_cpu():
    """updateCharts must apply the same per-core normalization."""
    content = _read_template()
    update_idx = content.find("function updateCharts")
    next_func = content.find("function ", update_idx + 20)
    section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    assert "llamaCpuUtilNorm" in section, \
        "updateCharts missing CPU normalization"
    assert "Math.min(llamaCpuUtilNorm / totalCpuUtil, 1)" in section, \
        "updateCharts CPU fraction not clamped"
    assert "Math.min(llamaGpuUtil / gpuUtil, 1)" in section, \
        "updateCharts GPU fraction not clamped"
    # Denominator must use the TRUE total OS CPU (all processes), not the
    # aggregator's tracked-process-only cpu.percent.
    assert "data.system_raw?.cpu?.percent" in section, \
        "updateCharts denominator not using true total OS CPU"
    print("[PASS] updateCharts applies normalized+clamped fractions")


def test_cpu_filtered_uses_ratio_not_raw_min():
    """CPU %(ƒ) must be llama's SHARE of total OS CPU (ratio), not a raw min.

    The bug (bead ujwb): filteredCpu = Math.min(llamaCpuUtil, cpuUtil) returned
    the unfiltered cpuUtil whenever llama was active, because llamaCpuUtil is
    per-core scale (can exceed 100) while cpuUtil is normalized 0-100. The
    corrected formula is (llamaCpuUtilNorm / totalCpuUtil) * 100 clamped to
    [0,100], mirroring the filtered-power ratio logic.
    """
    content = _read_template()
    update_idx = content.find("function updateCharts")
    next_func = content.find("function ", update_idx + 20)
    section = content[update_idx:next_func if next_func != -1 else update_idx + 3000]

    # The old buggy form must NOT be present in updateCharts
    assert "Math.min(llamaCpuUtil, cpuUtil)" not in section, \
        "filteredCpu must not use the raw min (returns unfiltered cpuUtil)"
    # The corrected form: normalized llama / true total * 100, clamped to [0,100]
    assert "Math.min(llamaCpuUtilNorm / totalCpuUtil, 1) * 100" in section, \
        "filteredCpu must use llama's share of total OS CPU, scaled to 100"
    print("[PASS] CPU %(ƒ) uses ratio (llama/total * 100) instead of raw min")


if __name__ == "__main__":
    tests = [
        test_cpu_normalizes_per_core_scale,
        test_cpu_fraction_clamped_to_1,
        test_gpu_fraction_clamped_to_1,
        test_gpu_requires_process_data,
        test_charts_section_normalizes_cpu,
        test_cpu_filtered_uses_ratio_not_raw_min,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    import sys
    sys.exit(1 if failed else 0)
