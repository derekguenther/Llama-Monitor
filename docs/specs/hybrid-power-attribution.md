# Spec: Hybrid Power Attribution for llama-monitor

**Status:** Draft for spec-reviewer review (rev 4)
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
attributes the delta by utilization share. The math is **per-component** (CPU and GPU
computed separately, then summed).

### 2.1 Per-Component Core Equation

For each component `c ∈ {cpu, gpu}`:

```
totalPower_c = measured total power of component c
activityDelta_c = max(0, totalPower_c - idleBaseline_c)
```

### 2.2 Per-Component Attribution of the Activity Delta

```
llamaDirect_c = llamaShare_c * activityDelta_c
otherApps_c  = (1 - llamaShare_c) * activityDelta_c
```

Where `llamaShare_c` is clamped to `[0, 1]`:

```
llamaShare_c = clamp( llamaUtil_c / util_c, 0, 1 )
llamaUtil_c  = sum of llama.cpp per-process util for component c (from process_cpu/process_gpu)
util_c       = total utilization of component c
```

`llamaShare` is clamped because summed per-process `cpu_percent` values are each a % of
system capacity and can exceed the reported system util; without clamping,
`otherApps_c` would go negative.

### 2.3 Utilization Share — Denominator Definition (CRITICAL)

**The collector filters `process_cpu`/`process_gpu` to tracked processes (llama-server.exe)
only** (system_metrics.py `_collect_cpu` ~line 158 and `_collect_process_gpu` ~line 363).
Therefore "sum over ALL processes" is NOT available from `process_cpu`; it equals the
llama sum and would force `llama_cpu_share = 1.0`, reintroducing the Netflix bug for CPU.

The denominator must therefore be the **total system utilization** for the component,
which IS collected:

```
llama_cpu_share = clamp( sum(process_cpu[proc].cpu_percent for llama procs) / cpu.percent , 0, 1 )
llama_gpu_share = clamp( sum(process_gpu[proc].gpu_utilization for llama procs) / gpu.usage, 0, 1 )
```

- `cpu.percent` is the total CPU utilization (the `percent` field of `_collect_cpu`,
  same unit as the per-process `cpu_percent` — both are % of system capacity over the
  poll interval).
- `gpu.usage` is the total GPU utilization (same unit as per-process `gpu_utilization`).
- Both numerator and denominator are in the SAME unit, so no `cpu_count` normalization
  is applied on either side (aggregator.py's `cpu_percent/cpu_count` normalization at
  lines 96-99 is for a different display purpose and must NOT be used for share).
- If `cpu.percent`/`gpu.usage` is 0 or absent → share = 0.

### 2.4 Blame Categories (exhaustive, sum to totalPower)

1. **llama.cpp direct** = `llamaDirect_cpu + llamaDirect_gpu`.
2. **llama.cpp baseline** = `baselineAttributed_cpu + baselineAttributed_gpu`, blamed
   ONLY while `llama-server.exe` is running, and **capped** so it never exceeds the
   component's total power:

   ```
   baselineAttributed_c = llama_running ? min(idleBaseline_c, totalPower_c) : 0
   ```

   (Capping prevents `baseline + direct + otherApps > totalPower_c` when a component sits
   at or below its baseline while llama runs — e.g. CPU-only inference where the GPU
   component is at its ~14W baseline.)
3. **otherApps** = `otherApps_cpu + otherApps_gpu`.
4. **unattributed** = idle baseline (cpu+gpu) when llama.cpp NOT running + measurement
   residual (any gap between the sum of categories and totalPower).

**Invariant:** `direct + baseline + otherApps + unattributed == totalPower` (within
floating-point residual).

### 2.5 llama.cpp Default Cost

```
llama.cpp cost = direct + baseline (the hybrid)
```

### 2.6 Netflix Case Resolution

- **llama.cpp idle + Netflix active**: `llamaShare_c = 0`, so `llamaDirect_c = 0`.
  llama.cpp gets only the baseline (blamed because it's running), NOT the Netflix delta.
- **Both active**: the delta splits proportionally by utilization share.

## 3. Foundations Verified in Current Code

- `system_metrics.py:41` — `tracked_processes = ["llama-server.exe"]`; `process_cpu` and
  `process_gpu` are already filtered to llama.cpp only (denominator = total util, §2.3).
- Frontend `filteredCpuPower = (llamaCpuUtil/cpuUtil)*cpuPower` (index.html:1236) already
  implements direct attribution (standalone) with the same total-util denominator.
- `calculate_idle_baseline()` (electricity_cost.py:311) exists (idle = CPU+GPU < 5%) but
  `idle_baseline_w` (config 40W) is stored and NEVER used.
- GPU idle ~14W, CPU idle ~22W (true idle ~36W from capture); **baselines differ per
  component**.
- BOTH aggregators (`aggregator.py` and `aggregator_daemon.py`) call
  `update_power_readings()` — centralizing the hybrid computation in
  `electricity_cost.py` fixes both paths at once.

## 4. Implementation Plan

### 4.1 Caller-Side Share Computation

The aggregators compute the shares and `llama_running` from the process data already
present at their call sites, and pass them into `update_power_readings`.

**In `aggregator.py`** (`store_raw_metrics`, around lines 242-258):
- `llama_cpu_share` = clamp( sum(process_cpu[proc]["cpu_percent"] for llama procs) /
  cpu.percent, 0, 1 ). If `cpu.percent` is 0 or absent, share = 0.
- `llama_gpu_share` = clamp( sum(process_gpu[proc]["gpu_utilization"] for llama procs) /
  gpu.usage, 0, 1 ). If `gpu.usage` is 0 or absent, share = 0.
- `llama_running` = True if any `llama-server.exe` entry exists in `process_cpu` or
  `process_gpu` this interval.

**In `aggregator_daemon.py`** (`_calculate_cost`, line 261):
- Same computation from the `system_metrics` it already has (`cpu.process_cpu` +
  `cpu.percent`, `process_gpu` + `gpu.usage`).
- Pass into the shared `update_power_readings` call at line 281.

Both aggregators use a **shared pure helper**
`compute_attribution_inputs(cpu, gpu) -> (llama_cpu_share, llama_gpu_share, llama_running)`
living in one place (e.g. `electricity_cost.py`) and imported by both aggregators — no
divergence.

### 4.2 Store Raw Primitives per Interval

Store per interval in a new `power_attribution` table (NOT nullable columns on
`combined_metrics` — see §4.6), one row per timestamp:

- `timestamp`
- `llama_cpu_share` — llama.cpp CPU utilization share (clamped 0.0-1.0)
- `llama_gpu_share` — llama.cpp GPU utilization share (clamped 0.0-1.0)
- `total_cpu_power_w` — total CPU power
- `total_gpu_power_w` — total GPU power
- `idle_baseline_cpu_w` — per-component CPU idle baseline
- `idle_baseline_gpu_w` — per-component GPU idle baseline
- `llama_running` — bool, whether llama-server.exe was running this interval
- `direct_wh`, `baseline_wh`, `other_apps_wh`, `unattributed_wh` — the four per-interval
  blame-category energy (watts × duration_hours), so monthly/session views are simple
  `SUM()` queries.

> Note: these total-power columns duplicate the `cpu_power_w`/`gpu_power_w` already in
> `combined_metrics.system_data` JSON, but they are stored here for attribution
> correctness (self-contained rows for SUM queries). This is intentional; see §4.6.

### 4.3 Auto-Calibrate Idle Baseline (Per-Component)

Replace hardcoded 40W with per-component auto-calibration:

- When CPU+GPU both < 5% (idle), record `cpu_power_w` as `idle_baseline_cpu_w` and
  `gpu_power_w` as `idle_baseline_gpu_w`.
- **Exponential moving average** with a long window (e.g. decay α = 0.01 per 1s poll,
  ~100s time constant) so it converges to the measured idle without chasing noise.
- Calibration runs regardless of whether llama.cpp is running (the baseline is blamed
  only while llama.cpp runs, but the calibration is a system property).
- **First-run fallback**: until calibrated, default `idle_baseline_cpu_w = 22.0` and
  `idle_baseline_gpu_w = 14.0` (from the measured capture), not a single 40W scalar.

**Calibration call site (G3):** calibration is invoked from `update_power_readings()`,
which must therefore also receive `cpu_percent` and `gpu_percent` (the total utilization
values) so it can detect the idle condition. The full signature (see §4.4) includes them.
The existing scalar `calculate_idle_baseline()`/`IdleBaselineTracker` remain for the
legacy system-idle display; the new per-component EMA calibration is separate.

**Runtime + restart persistence (G3):**
- The live EMA baseline lives as attributes on `ElectricityCostCalculator`
  (`idle_baseline_cpu_w`, `idle_baseline_gpu_w`).
- Persisted to a settings row in the DB on each calibration update (or on session stop),
  so a restart restores the last calibrated baseline instead of re-converging from the
  22W/14W fallback.

### 4.4 Centralize Hybrid Computation in `update_power_readings`

Modify `update_power_readings()` to accept the raw primitives and compute the blame
categories internally:

```
update_power_readings(
    gpu_power_w, cpu_power_w, duration_seconds,
    llama_cpu_share, llama_gpu_share,
    idle_baseline_cpu_w, idle_baseline_gpu_w,
    llama_running,
    cpu_percent, gpu_percent     # for idle-baseline calibration
)
```

Inside:
1. Calibrate per-component idle baseline when idle detected (cpu+gpu < 5%).
2. Compute per-component activityDelta and the four blame-category watts (per §2),
   applying the `baselineAttributed_c = min(idleBaseline_c, totalPower_c)` cap.
3. Accumulate the **hybrid (direct + baseline)** watts into the existing running totals
   (`gpu_energy_wh`, `cpu_energy_wh`, `total_energy_wh`, and today's equivalents), so
   the persisted Session/Monthly cost reflects the hybrid.
4. Track raw totals separately in-memory: `raw_gpu_energy_wh`, `raw_cpu_energy_wh`,
   `raw_total_energy_wh` for the "system" view (these are in-memory only; the system
   historical view reads raw power storage per §4.7 — see S6).
5. Persist the four blame-category watts per interval into `power_attribution`.
6. **Fix the daemon delta-key bug (G7):** aggregator_daemon.py:309-311 reads
   `delta.get("total_energy")`/`delta.get("gpu_energy")`/`delta.get("cpu_energy")` but
   `update_power_readings` returns `delta_total_wh`/`delta_gpu_wh`/`delta_cpu_wh`
   (electricity_cost.py:287-293), so daemon deltas are always 0. Since this change rewrites
   the return contract, align the daemon to the correct keys (or return both key sets) so
   per-interval energy is nonzero and the integration test passes.

Because BOTH aggregators call `update_power_readings`, this single change fixes both
paths. `daily_energy`, `cumulative_energy`, and `sessions` now reflect hybrid watts.

### 4.5 Accumulator Migration (G5)

`_load_cumulative_energy`/`_load_today_energy` (electricity_cost.py:56, 70) restore
previously-**raw** totals. After the change, `update_power_readings` accumulates hybrid
watts on top of those restored raw values — a mixed-unit accumulator. Migration strategy:

- Add a version flag (e.g. `attribution_v2_enabled`) to the settings row.
- On first run with the flag unset: leave legacy raw totals as-is (historical continuity),
  but mark the flag set. New accumulation is hybrid from that point forward.
- Provide a `reset` affordance (existing `clear_session_energy`) for users who want to
  zero the mixed totals and start fresh with hybrid-only accounting.
- Document in UI that switching to hybrid resets the cost baseline (Session/Today/Monthly
  reflect hybrid from activation forward).

### 4.6 Schema Choice: Separate `power_attribution` Table + Retention

Prefer a dedicated table over nullable columns on `combined_metrics` because:

- `combined_metrics` is JSON-blob based (db.py:531-538); nullable columns would need to be
  added to every SELECT and would be NULL for daemon-written rows.
- A dedicated table keeps both aggregators' JSON writes untouched and is cleanly keyed by
  timestamp.
- `combined_metrics` is NOT in the compression path, so raw per-interval data is retained.
- The total-power columns are intentionally duplicated here (self-contained attribution
  rows); they are NOT an attempt to replace `combined_metrics.system_data.cpu_power_w`.

**Retention/compression (G4):** the table grows ~86k rows/day. Add `power_attribution` to
the existing compression path (`_compress_to_minute` / `_compress_to_hour` in
aggregator_daemon), aggregating the four `*_wh` columns by SUM per minute/hour and
dropping the sub-minute rows. This bounds table growth and preserves monthly/session SUM
queries on the compressed rows.

**Write-conflict/dedup (G5-new):** `power_attribution.timestamp` is the PRIMARY KEY. Use
`INSERT OR REPLACE` (matching the aggregators' existing pattern for `combined_metrics`) so
concurrent/repeated writes for the same timestamp are idempotent and never double-attribute.

### 4.7 Historical Monthly/Session Views

- Monthly and Session attribution = `SUM(direct_wh)`, `SUM(baseline_wh)`,
  `SUM(other_apps_wh)`, `SUM(unattributed_wh)` over the date range from
  `power_attribution` (post-compression), filtered by the selected checkbox categories.
- At ~1 row/min after compression, monthly SUM queries are cheap. Index the timestamp
  column (PK).
- Raw-power ("system" view) historical totals are unchanged (computed from existing raw
  power storage).

### 4.8 UI Checkboxes

Add checkboxes in the cost UI to select which blame categories contribute to the
displayed llama.cpp cost breakdown:

```
[x] llama direct
[x] llama baseline (when running)
[ ] other apps
[ ] unattributed
```

- **Stored cost is always the hybrid** (direct + baseline) — the headline Monthly/Session
  cost is never affected by checkboxes.
- Checkboxes are a **display-only filter** that recomputes the breakdown at display time
  from the category watts stored in `power_attribution`.
- Default selection = direct + baseline. Keep the standalone direct (filtered) metric
  always visible.
- Checkbox selection is persisted as a user setting in the DB (so it survives reloads),
  but toggling never rewrites stored cost — it only changes the displayed breakdown.

## 5. Data Integrity & Error Handling

### 5.1 Sanitization of Raw Primitives

- Guard `-1` sentinels (used by aggregator_daemon's `safe_float` for broken sensor data)
  in ALL raw primitive inputs: treat any value `< 0` or `None` as missing → contribution
  of 0 for that interval, never propagate `-1` into attribution math or display.
- Division-by-zero guards:
  - `util_c == 0` (including `cpu.percent`/`gpu.usage` absent or 0) → `llamaShare_c = 0`,
    `llamaDirect_c = 0`, `otherApps_c = 0` (all of `totalPower_c` goes to
    `unattributed`/`baseline`).
  - Missing `process_cpu`/`process_gpu` snapshot → `llamaShare_c = 0`, not an error.
  - `duration_seconds <= 0` → skip accumulation (no energy added).
- `-1` guard values must never appear in any computed display.
- **Non-NVML systems (S7):** on systems without NVML, `gpu.usage` is the `-1` sentinel, so
  `llama_gpu_share` is always 0 there (correct per this sanitization). Document this so
  future "GPU share is always 0" is understood, not treated as a bug.

### 5.2 State Transitions

- `llama_running` derived from whether `llama-server.exe` appeared in the process
  snapshot this interval. Apply a short **hysteresis** (S2): treat llama.cpp as running
  until N consecutive misses (e.g. N=3) to avoid flicker from transiently missed
  snapshots.
- Idle baseline calibration is slow-moving (EMA as above). On first run with no baseline,
  fall back to `22.0` / `14.0` defaults until calibrated.
- If both `total_cpu_power_w` and `total_gpu_power_w` are missing, the interval is
  skipped (no attribution rows written).
- **tracked_processes alignment (S1):** aggregator_daemon.py:69 falls back to
  `["llama.cpp"]` while system_metrics.py:41/config default to `["llama-server.exe"]`.
  Align the daemon's fallback to `["llama-server.exe"]` so `llama_running` and shares work
  even when the config key is absent.

## 6. Testing

- **Unit tests** for `electricity_cost.py` attribution math:
  - Given totalPower, idleBaseline, llamaShare → verify `direct + baseline + otherApps +
    unattributed == totalPower` (within FP residual).
  - Netflix case: llama idle (share 0) + high total power → `llamaDirect = 0`,
    llama.cpp cost = baseline only.
  - Both-active case: delta splits proportionally.
  - Clamp: llamaShare > 1 → clamped to 1, `otherApps_c >= 0`.
  - **Baseline cap (B2):** totalPower_c < idleBaseline_c while llama running →
    `baselineAttributed_c = totalPower_c`, `direct + baseline + otherApps +
    unattributed == totalPower_c` (no negative unattributed).
  - Division by zero: cpuUtil=0 or gpuUtil=0 → shares 0, no crash.
  - `-1`/None inputs → sanitized to 0, no `-1` in output.
  - Idle baseline EMA converges to measured idle value.
  - **CPU share denominator (B1):** a multi-core case where sum(llama percents) is large
    but `cpu.percent` is smaller → share computed against `cpu.percent` and clamped, NOT
    degenerating to 1.0.
  - **Caller wiring:** `compute_attribution_inputs` returns correct shares/running from a
    sample process snapshot where `process_cpu` contains only llama procs.
- **Property test**: randomized inputs → `sum == totalPower` invariant holds when both
  components present (note: §5.1 zeroes missing components, which by design breaks the
  invariant — scope the property test to both-present inputs).
- **Integration tests**:
  - Both aggregators produce valid attribution rows (cover aggregator_daemon `-1`/`None`
    inputs).
  - Accumulator switch keeps `today_wh == SUM(hybrid_wh)` across intervals.
  - Daemon delta keys (G7) now return nonzero per-interval energy.
  - Monthly/Session `SUM` queries over `power_attribution` (pre- and post-compression)
    return correct category totals.
  - Concurrent dual-daemon writes for the same timestamp do not double-attribute
    (INSERT OR REPLACE idempotency).
- **Frontend**: toggling checkboxes changes the displayed breakdown but leaves raw-power
  ("system" view) untouched and never changes stored Monthly cost.

## 7. Non-Goals / Scope Limits

- Does NOT change the standalone direct (filtered) metric already displayed.
- Does NOT remove or break raw power display (still available as "system" view).
- Does NOT attempt to measure actual power of non-llama processes beyond share-based
  attribution.
- Does NOT collect all-process CPU percents (the collector filters to tracked processes;
  the denominator is the existing total `cpu.percent`).
- Backward compatibility: existing raw-power behavior remains available as the "system"
  view; stored hybrid cost is the new default llama.cpp cost.

## 8. Decisions Locked in This Revision

1. **Accumulator change**: `update_power_readings` accumulates hybrid (direct + baseline)
   watts into session/daily/cumulative counters; raw totals tracked per-component
   in-memory (`raw_gpu_energy_wh`/`raw_cpu_energy_wh`/`raw_total_energy_wh`).
2. **Both aggregators covered**: fix centralized in `electricity_cost.py`; shared
   `compute_attribution_inputs` helper for caller-side share derivation (B1).
3. **Per-component math**: activityDelta, llamaShare, and blame categories computed per
   CPU/GPU component and summed.
4. **llamaShare clamped** to [0,1]; **denominator = total component util**
   (`cpu.percent`/`gpu.usage`), NOT an all-process sum (B1).
5. **Separate `power_attribution` table** with retention via compression (G4) and
   timestamp PK + INSERT OR REPLACE dedup.
6. **Per-component baseline fallback** (22W/14W); EMA calibration coexists with legacy
   `IdleBaselineTracker`; runtime+restart persistence.
7. **EMA calibration** with α=0.01 per poll (~100s time constant); calibration call site
   is inside `update_power_readings`, which receives `cpu_percent`/`gpu_percent` (G3).
8. **Baseline cap**: `baselineAttributed_c = min(idleBaseline_c, totalPower_c)` when
   llama running (B2).
9. **Checkbox persistence**: stored as user setting; stored Monthly cost always hybrid;
   checkboxes display-only.
10. **Historical views** via `SUM` over compressed `power_attribution`.
11. **`-1` sanitization** defined for all raw primitive inputs; non-NVML GPU-share note
    (S7).
12. **Accumulator migration** via `attribution_v2_enabled` flag + reset affordance (G5).
13. **Daemon delta-key bug** fixed as part of the return-contract rewrite (G7).
14. **tracked_processes alignment** in aggregator_daemon to `["llama-server.exe"]` (S1).
15. **llama_running hysteresis** N=3 (S2).
