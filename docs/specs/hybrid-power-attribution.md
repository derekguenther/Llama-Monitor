# Spec: Hybrid Power Attribution for llama-monitor

**Status:** Draft for spec-reviewer review
**Related beads:** llama-monitor-ym0 (reopened), llama-monitor-h9z0 (design tracking)
**Date:** 2026-08-18
**Author:** Agent (per user's design decision)

## 1. Problem Statement

The goal of llama-monitor is to power-meter **llama-server.exe specifically**, not the
whole system. The current implementation does not achieve this:

- `electricity_cost.py update_power_readings` (line 216) computes
  `cost = (gpu_power_w + cpu_power_w) * duration_hours * rate` using **raw total system
  power**.
- `idle_baseline_w` is stored (`config.py DEFAULT_CONFIG idle_baseline.power_w=40.0`,
  DB setting, calculator attribute) and `calculate_idle_baseline()` exists (line 311),
  but `idle_baseline_w` is **never subtracted** from any power reading or cost.
- The 8rn bead fixed the frontend **filtered-power display** but not the **cost
  calculation**.

Capture data (session `20260816-111156`) confirms the impact:

- **True idle** (overnight 03-07h, midday 12-19h, n=45946): CPU 0.2%, GPU 0%,
  cpu_power ~22W + gpu_power ~14W = **~36W total**.
- **Evening active** (20-23h, n=14133): CPU 60-90%, GPU up to 11.6%, **~146W total**
  — user activity (games/Netflix/etc.), NOT llama.cpp.

So while llama.cpp is idle, Monthly/Session Cost captures user activity, inflating
llama.cpp's apparent cost. The **Netflix case** (llama.cpp idle + Netflix active)
demonstrates the flaw: raw power would attribute ~146W to llama.cpp when it contributed
nothing.

## 2. Design Decision (User-Selected: HYBRID "Direct + baseline" model)

The model separates total power into an idle baseline and an activity delta, then
attributes the delta by utilization share.

### 2.1 Core Equation

```
totalPower = idleBaseline + activityDelta
activityDelta = max(0, totalPower - idleBaseline)
```

### 2.2 Attribution of the Activity Delta

The activity delta splits by utilization share (per component, CPU and GPU separately):

```
llamaDirectDelta = llamaShare * activityDelta
otherAppsDelta  = (1 - llamaShare) * activityDelta
```

Where `llamaShare` is the fraction of total utilization attributable to llama.cpp:

```
llamaShare_cpu = llamaCpuUtil / cpuUtil      # llama.cpp CPU share
llamaShare_gpu = llamaGpuUtil / gpuUtil      # llama.cpp GPU share
```

This is the same "Filtered" ratio already computed in the frontend
(`templates/index.html` lines 1233-1239): `filteredGpuPower = (llamaGpuUtil/gpuUtil)*gpuPower`.

### 2.3 Blame Categories (exhaustive, sum to totalPower)

1. **llama.cpp direct** = `llamaDirectDelta` (share of the activity delta attributable to
   llama.cpp).
2. **llama.cpp baseline** = `idleBaseline`, blamed ONLY while `llama-server.exe` is
   running.
3. **otherApps** = `otherAppsDelta`.
4. **unattributed** = idle baseline when llama.cpp NOT running + measurement residual.

### 2.4 llama.cpp Default Cost

```
llama.cpp cost = direct + baseline (the hybrid)
```

### 2.5 Netflix Case Resolution

- **llama.cpp idle + Netflix active**: `llamaDirectDelta = 0`. llama.cpp gets only the
  baseline (blamed because it's running), NOT the Netflix delta.
- **Both active**: the delta splits proportionally by utilization share.

## 3. Foundations Verified in Current Code

- `system_metrics.py:41` — `tracked_processes = ["llama-server.exe"]`; `process_cpu` and
  `process_gpu` are already filtered to llama.cpp only.
- Frontend `filteredCpuPower = (llamaCpuUtil/cpuUtil)*cpuPower` (index.html:1236) already
  implements direct attribution (standalone).
- `calculate_idle_baseline()` (electricity_cost.py:311) exists (idle = CPU+GPU < 5%) but
  `idle_baseline_w` (config 40W) is stored and NEVER used.
- GPU idle ~14W, CPU idle ~22W (true idle ~36W from capture); **baselines differ per
  component**.

## 4. Implementation Plan

### 4.1 Store Raw Primitives per Interval

Store per interval (in `combined_metrics` and/or a new table), NOT baked into cost:

- `llama_cpu_share` — llama.cpp CPU utilization share (0.0-1.0)
- `llama_gpu_share` — llama.cpp GPU utilization share (0.0-1.0)
- `total_cpu_power_w` — total CPU power
- `total_gpu_power_w` — total GPU power
- `idle_baseline_cpu_w` — per-component CPU idle baseline (auto-calibrated)
- `idle_baseline_gpu_w` — per-component GPU idle baseline (auto-calibrated)
- `llama_running` — bool, whether llama-server.exe was running this interval

### 4.2 Auto-Calibrate Idle Baseline

Replace hardcoded 40W with per-component auto-calibration from
`calculate_idle_baseline()`:

- When CPU+GPU both < 5% (idle), record cpu_power as `idle_baseline_cpu_w` and gpu_power
  as `idle_baseline_gpu_w` (moving average or last-known-good).
- This reflects measured ~36W (CPU 22W + GPU 14W) instead of assumed 40W.

### 4.3 Compute Views at Display Time

Do NOT bake attribution into the stored cost. Compute blame categories at display time
from the raw primitives. The cost calculator accumulates
`(blameCategorySum) * duration * rate`.

### 4.4 UI Checkboxes

Add checkboxes in the cost UI to select which blame categories contribute to the
llama.cpp cost display:

```
[x] llama direct
[x] llama baseline (when running)
[ ] other apps
[ ] unattributed
```

Default: llama direct + llama baseline (the hybrid). Keep the standalone direct metric
always visible.

## 5. Data Integrity & Schema

### 5.1 New/Modified Columns

The raw primitives need a storage location. Options considered:
- Add nullable columns to `combined_metrics` (extensible per DESIGN.md line 191).
- Or a new `power_attribution` table with one row per interval.

Preferred: nullable columns on `combined_metrics` to align with the existing
"extensible metrics" pattern. All new columns nullable (default NULL) so existing rows
remain valid.

### 5.2 State Transitions

- `llama_running` derived from whether llama-server.exe appeared in the process snapshot
  this interval.
- Idle baseline calibration is a slow-moving state: update only when idle detected, decay
  toward the measured idle value.
- On first run with no baseline yet, fall back to config default (40W) until calibrated.

## 6. Testing

- **Unit tests** for `electricity_cost.py`:
  - Attribution math: given totalPower, idleBaseline, llamaShare → verify direct,
    baseline, otherApps, unattributed sums equal totalPower.
  - Netflix case: llama idle (share 0) + high total power → llamaDirectDelta = 0,
    llama.cpp cost = baseline only.
  - Both-active case: delta splits proportionally.
  - Idle baseline auto-calibration: feed idle readings → baseline converges to measured.
  - `-1` guard values never appear in any computed display.
- **Integration tests**: aggregator stores raw primitives correctly per interval.
- **Frontend**: checkboxes toggle blame categories; llama.cpp cost updates accordingly.

## 7. Non-Goals / Scope Limits

- Does NOT change the standalone direct (filtered) metric already displayed.
- Does NOT remove or break raw power display (still available as "system" view).
- Does NOT attempt to measure actual power of non-llama processes beyond share-based
  attribution.
- Backward compatibility: existing raw-power behavior remains available.

## 8. Open Questions for Review

1. Storage schema: nullable columns on `combined_metrics` vs. separate table — confirm
   preferred approach.
2. Idle baseline calibration: moving average window size and decay rate not specified.
3. Whether the UI checkboxes persist as a user setting (DB) or default to the hybrid
   selection each load.
4. Exact placement of attribution computation (aggregator vs. web_server) for display-time
   views.
