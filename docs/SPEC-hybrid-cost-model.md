# Hybrid "Direct + Baseline" Cost Model — Implementation Spec (Rev 8)

**Beads resolved:** `llama-monitor-h9z0` (design), `llama-monitor-ym0` (P1 idle cost bug), `llama-monitor-2byy` (idle baseline never consumed)
**Design source:** `llama-monitor-h9z0` notes — HYBRID 'Direct + baseline' model finalized 2026-08-18.
**Rev 8 changes:** final revision incorporating all spec-reviewer findings (B1–B6, G1–G6, N1–N3) and subsequent blocker resolutions; see §10 Review Log.

## 1. Problem Statement

The current cost calculation charges llama.cpp for **all** system power:
`cost = (gpu_power_w + cpu_power_w) * duration_hours * rate`. This inflates
llama.cpp's apparent cost because it captures unrelated user activity
(Netflix, games, etc.) — e.g. evening user activity ~146W while llama.cpp is
idle, vs. true idle ~36W. The idle baseline is stored but never consumed.

## 2. Chosen Model (from design)

```
totalPower      = idleBaseline + activityDelta
activityDelta   = totalPower - idleBaseline
llamaShare      = llamaUtil / totalUtil            (ratio, NOT watts)
otherShare      = 1 - llamaShare
llamaDirectDelta = llamaShare * activityDelta
otherAppsDelta   = otherShare * activityDelta

Blame categories (exhaustive, sum to totalPower):
  1. llama.cpp direct     = llamaDirectDelta
  2. llama.cpp baseline   = idleBaseline, blamed ONLY while llama.cpp running
  3. otherApps            = otherAppsDelta
  4. unattributed         = remainder category (see 4.3)
```

Default llama.cpp cost = **direct + baseline** (hybrid).

### Resolves Netflix case
- llama.cpp idle + Netflix active → llamaShare=0, llamaDirectDelta=0, llama gets only baseline, NOT Netflix delta.
- Both active → delta splits proportionally by share.

## 3. Verified Foundations

- `system_metrics.py:41` default `tracked_processes=['llama-server.exe']`, but **production overrides** it from config (`llamamonitor.py:160` defaults to `["llama.cpp"]`, assigned at :170-171). All llama-share / llama_running logic must key off `self.tracked_processes`, NOT a hardcoded name.
- `process_cpu` uses psutil (works without NVML); `process_gpu` requires NVML (`system_metrics.py:327-328` returns `{}` without NVML).
- Frontend `filteredGpuPower`/`filteredCpuPower` (`index.html:1340-1355`) are **watts** (`share × power`), not share ratios.
- `update_power_readings(gpu_power_w, cpu_power_w, duration_seconds)` (`electricity_cost.py:216`) — must stay backward-compatible.
- `calculate_idle_baseline(cpu_percent, gpu_percent, system_power_w)` (`electricity_cost.py:311`) returns a scalar.
- `IdleBaselineTracker.check_idle(cpu_percent, gpu_percent, system_power_w)` (`idle_baseline.py:39`) writes scalar baseline; read methods exist but unused in production.
- **CRITICAL:** `system_power_w = cpu_power_w` (`system_metrics.py:479`) — GPU power lives in separate `gpu.power_w` (NVML). So a single `system_power_w` is CPU-only, NOT total.
- `_migrate_schema` (`db.py:223`) creates **missing tables only** — no column-addition mechanism exists.

## 4. Architectural Resolutions (from review)

### 4.1 Define totalPower
`totalPower = gpu_power_w + cpu_power_w` (matches `update_power_readings` math at
`electricity_cost.py:237-239`). Store the raw components per interval. The
"exhaustive sum" invariant (§4.3) is defined against this totalPower.

### 4.2 Per-component idle baseline data path
The single-scalar baseline path is insufficient. Changes:

- **`IdleBaselineTracker.check_idle`** (`idle_baseline.py:39`): change signature to
  `check_idle(cpu_percent, gpu_percent, gpu_power_w, cpu_power_w)` and accumulate
  per-component samples internally. Return per-component baselines as
  `(cpu_idle_w, gpu_idle_w)` when the system just became idle.
- **`_store_baseline`** (`idle_baseline.py:84`): store `cpu_idle_w` and `gpu_idle_w`.
- **`get_baseline_average` / `get_recent_baseline`** (`idle_baseline.py:100,119`):
  return per-component values, e.g. `(cpu_idle_w, gpu_idle_w)` averaged from the
  new columns.
- **`calculate_idle_baseline`** (`electricity_cost.py:311`): change signature to
  `calculate_idle_baseline(cpu_percent, gpu_percent, gpu_power_w, cpu_power_w)`
  and return per-component `(cpu_idle_w, gpu_idle_w)` when
  `cpu_percent + gpu_percent < 5.0`, else `None`. It has no production callers
  today, so replacing the scalar return with the tuple is safe; update any tests
  that call it. Do NOT keep an overload — a single tuple-returning contract is
  unambiguous.
- **Scalar seeding rule:** when no auto-calibrated per-component baseline exists
  yet (first run), the scalar `idle_baseline_w` (default 40.0) seeds the
  baseline. Split it **proportionally to the current measured CPU vs GPU power**:
  `cpu_idle_w = idle_baseline_w * cpu_power_w / (cpu_power_w + gpu_power_w)`
  and `gpu_idle_w = idle_baseline_w - cpu_idle_w` (guard divide-by-zero → 50/50,
  i.e. `cpu_idle_w = gpu_idle_w = idle_baseline_w/2`, when both powers are 0).
  This keeps the manual setting as a meaningful fallback while preserving
  per-component granularity.
- **Call-site** `aggregator.py:195-196`: pass `cpu_power_w` and `gpu_power_w`
  (from `system_data`) instead of the scalar `system_power_w`. Read the
  auto-calibrated per-component baselines back from the tracker and feed them to
  the cost path (fixing `2byy` finding 2).

### 4.3 Exhaustiveness + unattributed (resolve B4)
The four categories must sum to exactly totalPower. Define `unattributed`
(the remainder category) explicitly. Because `direct + other == activityDelta`
(shares sum to 1), the unattributed term MUST also subtract the baseline
category to avoid double-counting it:

```
# llama running:
baseline        = idleBaseline                    (blamed)
direct          = llamaShare * activityDelta
other           = otherShare * activityDelta
unattributed    = max(0, totalPower - (direct + other + baseline))
# => direct + other + baseline + unattributed == totalPower

# llama NOT running:
direct = 0, other = 0, baseline = 0               (nothing blamed to llama)
unattributed = totalPower                         (entire power is unattributed)
# => 0 + 0 + 0 + totalPower == totalPower
```

When measured power is BELOW the baseline (`totalPower < idleBaseline`), clamp:
```
activityDelta = max(0, totalPower - idleBaseline)
direct = llamaShare * activityDelta
other  = otherShare * activityDelta
baseline = min(idleBaseline, totalPower)
unattributed = max(0, totalPower - (direct + other + baseline))
```
This keeps every term in `[0, totalPower]` and preserves the invariant in all
cases (llama running / not / power-below-baseline).

### 4.4 `cpu_util` denominator (resolve B5)
At aggregation time, `system_data["cpu_percent"]` is **not** raw OS percent when
`process_cpu` present — it is the tracked-process-derived value normalized by
core count (`aggregator.py:104-127`). The true OS-wide denominator is
`system_raw.cpu.percent` (`index.html:1351`). Therefore store the share
denominator from `system_raw.cpu.percent` (raw OS percent), not
`system_data["cpu_percent"]`. Same for GPU: denominator is raw `gpu.usage`.

### 4.5 `llamaShare` is a ratio; `otherShare` defined (resolve B6)
- `llamaCpuShare = (llamaCpuUtil / cpuCount) / cpuUtilOsPercent` (clamped to [0,1])
- `llamaGpuShare = llamaGpuUtil / gpuUtil` (clamped to [0,1])
- `llamaShare = max(llamaCpuShare, llamaGpuShare)` — the dominant share of
  activity. `otherShare = 1 - llamaShare`.
- **Division-by-zero guard:** if any denominator (`cpuUtilOsPercent`, `gpuUtil`,
  `cpuCount`) is `<= 0`, the corresponding share is `0`. This covers the fully
  idle OS case (`system_raw.cpu.percent == 0`, `gpu.usage == 0`).
These are computed at aggregation time and stored as primitives; the frontend
re-uses them at display time so stored share matches displayed share.

**Rationale for `max(cpu, gpu)` (dominant share):** llama.cpp workloads are
typically either compute-bound (high GPU) or prompt-bound (high CPU). Using the
dominant share avoids under-attributing when llama saturates one resource while
the other idles; it is deliberately conservative for llama attribution. This is
an explicit design choice; if a weighted blend is preferred, revisit later.

### 4.6 Column migration mechanism (resolve B3)
Add a column-addition migration in `_migrate_schema` (`db.py:223`):
- Use `PRAGMA table_info(idle_baseline)` to detect missing columns, then
  `ALTER TABLE idle_baseline ADD COLUMN cpu_idle_w REAL DEFAULT 0;` and
  `ADD COLUMN gpu_idle_w REAL DEFAULT 0;`.
- Add the columns to the fresh `CREATE TABLE idle_baseline` (`db.py:503`).
- Update BOTH write paths: `_store_baseline` (`idle_baseline.py:90-97`) and
  `insert_idle_baseline` (`db.py:778`) to the new column list.

### 4.7 Idle gate reconciliation (resolve G1)
The gate at `aggregator.py:195` requires `system_power_w > 0 and cpu_percent > 0
and gpu_usage > 0`. But a truly idle system usually has `gpu_usage == 0`, which
the gate rejects → auto-calibration dead. Change the gate to call `check_idle`
when power is meaningful but allow zero utilization:
```
if (cpu_power_w > 0 or gpu_power_w > 0):
    self.idle_tracker.check_idle(cpu_percent, gpu_usage, gpu_power_w, cpu_power_w)
```
This preserves the anti-false-zero-guard intent (no 0W baselines from momentary
zero power) while allowing true idle (0% util, >0W power) to be captured.

### 4.8 `llama_running` derivation (resolve G2)
Derived from the **union** of process data:
`llama_running = (len(process_cpu) > 0) or (len(process_gpu) > 0)`, keyed off
`self.tracked_processes`. On non-NVML systems `process_gpu` is empty but
`process_cpu` still signals running.

### 4.9 `update_power_readings` backward compatibility (resolve G5)
Keep the existing signature and add an optional kwargs block:
```python
def update_power_readings(self, gpu_power_w, cpu_power_w, duration_seconds,
                          *, primitives: Optional[dict] = None):
```
When `primitives` provided, compute blame categories; when absent, behave
exactly as today (raw total cost). All existing tests continue to pass.

## 5. Data Model Changes

### 5.1 Per-interval raw primitives in `cost_data` (JSON, `combined_metrics`)
Add to the per-interval cost dict built in `aggregator.py`:
```json
{
  "gpu_power_w": float,
  "cpu_power_w": float,
  "gpu_idle_w": float,
  "cpu_idle_w": float,
  "llama_gpu_share": float,
  "llama_cpu_share": float,
  "llama_share": float,
  "gpu_util": float,
  "cpu_util": float,
  "llama_running": bool,
  "llama_direct_w": float,
  "baseline_w": float,
  "other_w": float,
  "unattributed_w": float
}
```
These are **watts/ratios**, distinct from the cumulative `gpu_wh`/`cpu_wh`
fields. Blame math operates on watts then × duration (avoid double-counting with
cumulative energy). The four `*_w` blame keys are persisted per interval for
**client-side checkbox toggles / display**; the monthly endpoint sums the
persisted `daily_energy` blame columns (5.2b), NOT these per-interval watts.

### 5.2 `idle_baseline` table (extend)
Add columns `cpu_idle_w REAL DEFAULT 0`, `gpu_idle_w REAL DEFAULT 0` (see 4.6).

### 5.2b `daily_energy` attribution columns (monthly aggregation)
Extend `daily_energy` (db.py:557) with blame columns so the monthly endpoint is a
fast SQL SUM instead of parsing millions of JSON rows:
```
ALTER TABLE daily_energy ADD COLUMN direct_wh REAL DEFAULT 0;
ALTER TABLE daily_energy ADD COLUMN baseline_wh REAL DEFAULT 0;
ALTER TABLE daily_energy ADD COLUMN other_wh REAL DEFAULT 0;
ALTER TABLE daily_energy ADD COLUMN unattributed_wh REAL DEFAULT 0;
```
The aggregator accumulates these per-interval (blame_w × duration_hours) and
persists them via `update_today_energy` alongside `total_wh`/`gpu_wh`/`cpu_wh`.
Same column-migration mechanism as 4.6 (PRAGMA table_info + ALTER ADD COLUMN).

**Backfill on migration:** existing `daily_energy` rows have `total_wh > 0` but
blame columns = 0 (new columns default 0). On first run against an existing DB,
run a one-time backfill so the row invariant holds and the monthly endpoint
doesn't under-report the migration day:
```
UPDATE daily_energy SET unattributed_wh = total_wh
WHERE direct_wh + baseline_wh + other_wh + unattributed_wh = 0 AND total_wh > 0;
```
This runs once during `_migrate_schema` after adding the columns (guarded by the
same column-presence check so it does not re-run).

### 5.3 Settings
Keep `idle_baseline.power_w` (40.0) as manual override / pre-calibration fallback.
Add settings keys:
- `cost_show_llama_direct` (bool, default True)
- `cost_show_llama_baseline` (bool, default True)
- `cost_show_other_apps` (bool, default False)
- `cost_show_unattributed` (bool, default False)

## 6. Component Changes

### 6.1 `electricity_cost.py` — `ElectricityCostCalculator`
- `update_power_readings`: optional `primitives` kwarg (4.9); when present,
  compute `compute_blame` and include blame categories in returned stats dict.
- `calculate_idle_baseline`: per-component (4.2).
- Add `compute_blame(primitives, show_* flags)` → dict of 4 blame categories
  (watts) per interval, per 4.3.
- `idle_baseline_w` no longer dead: seeds per-component baseline when no
  auto-calibrated value exists (fallback), consumed by blame math.

### 6.1b Day-blame accumulator + write-path contract (resolves rollover gap)

Blame energy must live in the **cost_calculator's today-counters**, not a
separate aggregator accumulator, so there is a single writer per interval and
the existing day-rollover logic handles reset/archive naturally.

- `ElectricityCostCalculator` adds four today counters alongside
  `today_energy_wh`/`today_gpu_wh`/`today_cpu_wh`:
  `today_direct_wh`, `today_baseline_wh`, `today_other_wh`,
  `today_unattributed_wh`. These are initialized to `0.0` in `__init__` only,
  and reset to `0.0` at midnight rollover and `clear_session_energy`. They are
  NOT reset in `start_session` (see Lockstep Lifecycle below).
- `update_power_readings` (with `primitives`) computes blame watts, converts to
  Wh (`blame_w × duration_hours`), and accumulates into these counters in the
  SAME place it accumulates `today_gpu_wh`/`today_cpu_wh` (lines 271-273).
- **Midnight rollover** (lines 246-268): when `date` changes, archive the prior
  day's final blame values via `update_today_energy_archived` (extended to accept
  the four blame params) and reset the four counters to 0 — exactly mirroring the
  existing `today_*` handling. This keeps each `daily_energy` row internally
  consistent (`direct+baseline+other+unattributed == total_wh`).
- **`update_today_energy` signature** (db.py:1079): extend with
  `direct_wh=0.0, baseline_wh=0.0, other_wh=0.0, unattributed_wh=0.0` defaults so
  the SQL `INSERT ... ON CONFLICT DO UPDATE` writes all columns in one call.
- **All callers updated to pass blame values**:
  - `update_power_readings:281` (energy + blame, single call)
  - `persist_today_energy:305` (energy + blame)
  - `stop_session:123` (pass current today blame counters)
  - `clear_session_energy:570` (pass 0.0 for all — consistent with zeroing total)
  - `update_today_energy_archived` extended with the four blame params; rollover
    at :257 passes the archived values.
- **Lockstep lifecycle (critical):** the four blame counters
  (`today_direct_wh`, `today_baseline_wh`, `today_other_wh`,
  `today_unattributed_wh`) MUST always be mutated in lockstep with
  `today_energy_wh`. Every code path that reads, resets, archives, or clears
  `today_energy_wh` must do the same to the blame counters:
  - **Init / restart load** (`_load_today_energy`, electricity_cost.py:70):
    extend `get_today_energy` (db.py:1036) to SELECT the four blame columns and
    restore them into the counters, alongside `today_energy_wh`. This preserves
    the row invariant across a mid-day restart.
  - **`start_session`** (electricity_cost.py:84): does NOT reset
    `today_energy_wh` ("don't reset energy" comment at :89). Therefore the
    blame counters are ALSO NOT reset there — they persist in lockstep.
  - **Midnight rollover** (:246-268): archive prior-day blame values and reset
    the four counters to 0.0, exactly mirroring the `today_*` reset.
  - **`clear_session_energy`** (:548): zeroes `today_energy_wh`; must zero the
    blame counters too.
- **Invariant (both modes):** each `daily_energy` row satisfies
  `direct_wh + baseline_wh + other_wh + unattributed_wh == total_wh`.
  - Hybrid mode (primitives present): blame split per §4.3.
  - Backward-compat mode (primitives absent, §4.9): all interval energy is
    attributed to `unattributed` (`unattributed_wh += total_wh` per interval),
    so the invariant holds even without blame computation. This is consistent
    with the llama-not-running case in §4.3. The existing `total_wh`/`gpu_wh`/
    `cpu_wh` behavior and returned stats-dict keys are UNCHANGED; the new blame
    columns are purely additive — so test #8 ("behaves identically to today")
    holds for the pre-existing columns and return keys.

### 6.2 `idle_baseline.py` — `IdleBaselineTracker`
- Per-component tracking + storage + reads (4.2).
- Normalize the write path: use `insert_idle_baseline` (db.py:778) or unify
  timestamp format (resolve N1).

### 6.3 `aggregator.py`
- Fix idle gate (4.7), pass per-component powers to `check_idle`.
- Read auto-calibrated baselines from tracker; feed to `update_power_readings`.
- Compute llama shares at aggregation time from `system_raw` (4.4, 4.5).
- Populate raw-primitive keys in per-interval `cost_data` (5.1), including the
  four blame watts.
- Persist daily blame accumulation into `daily_energy` blame columns (5.2b) via
  `update_today_energy` alongside `total_wh`/`gpu_wh`/`cpu_wh`.

### 6.4 `web_server.py`
- `/api/metrics/monthly-cost` (line 318): per-day attribution breakdown
  (direct, baseline, other, unattributed) computed by summing the persisted
  blame columns from `daily_energy` (5.2b) — a fast SQL SUM over ~30 rows, not a
  JSON parse of millions of `combined_metrics` rows. Honor show_* settings. Keep
  `cost_usd` for backward compat.
- `/api/settings`: persist new `cost_show_*`.
- `/settings` route: expose checkboxes for the 4 blame categories.
- `/api/metrics/latest` / historical: include raw primitives so frontend toggles
  views client-side.

### 6.5 `templates/index.html`
- Monthly cost chart: render segmented attribution honoring show_* checkboxes.
- Add checkbox UI (default: llama direct + llama baseline checked).
- Keep standalone "Filtered" direct metric always visible.
- Guard all numeric displays against -1 / negative (AGENTS.md guardrail).

## 7. Testing Plan

New tests (mirror `test_energy_deltas.py`, `test_aggregator_integration.py`):
1. Blame categories sum to totalPower (invariant) for representative primitives.
2. Netflix case: llama idle + high other-activity → llamaDirectDelta=0, llama
   gets baseline only.
3. Both-active case: delta splits proportionally by share.
4. `idle_baseline` read methods return per-component values in production path.
5. Auto-calibrated baseline used when available; manual setting as fallback.
6. Monthly-cost API returns attribution breakdown honoring show_* flags, summed
   from `daily_energy` blame columns.
7. Migration: columns exist on `idle_baseline` AND `daily_energy` after
   `_migrate_schema` runs on an existing DB (no column → column added).
8. `update_power_readings` without `primitives` behaves identically to today.
9. Gate: true idle (0% util, >0W power) triggers baseline capture.
10. `llama_running` true on non-NVML system via process_cpu union.
11. Invariant holds for power-below-baseline case (clamped terms sum to totalPower).
12. `daily_energy` blame columns accumulate per-interval (blame_w × duration).
13. Midnight rollover: prior day's blame archived with final values, counters
    reset; next-day blame lands in the correct `daily_energy` row.
14. Each `daily_energy` row satisfies `direct+baseline+other+unattributed == total_wh`.
15. `stop_session` / `clear_session_energy` preserve the row invariant (pass blame
    values, or zero blame when zeroing total).
16. Restart mid-day: `get_today_energy`/`_load_today_energy` restore blame
    counters from the persisted row so the row invariant still holds.
17. `start_session` preserves blame counters in lockstep with `today_energy_wh`.
18. Migration backfill: pre-existing `daily_energy` rows with `total_wh > 0` get
    `unattributed_wh = total_wh` after `_migrate_schema` (backfill actually runs).

All existing 298 tests must continue to pass.

## 8. Verification Steps
- Run full test suite in worktree.
- Chrome functional review: dashboard cost display, monthly cost chart,
  settings checkboxes toggle views.
- Check for -1 guard values in all numeric displays.
- Run spec-reviewer then code-reviewer per user directive.

## 9. Out of Scope
- `llama-monitor-1nkd` (P1 freakout log investigation) — separate.
- `llama-monitor-m6p` (P4 top bar) — parked.
- `llama-monitor-bf7u` (remove dead show_temps) — separate quick win.

## 10. Review Log
- **Rev 1** (initial) → spec-reviewer found B1–B6, G1–G6, N1–N3.
- **Rev 2** → resolved B1,B2,B3,B5,B6,G1,G2,G5,G6. B4 (residual double-counted
  baseline) and G3 (blame not persisted for monthly SUM) still open.
- **Rev 3** → fixed B4 residual to subtract baseline; persisted blame keys in
  `cost_data` + `daily_energy` columns for monthly aggregation (G3); added
  division-by-zero guards, scalar-seeding rule, exact `calculate_idle_baseline`
  signature, dominant-share rationale, power-below-baseline clamping. Review
  confirmed B4/G3 + all should-fixes resolved, but flagged 2 new must-fix gaps:
  midnight blame-accumulator reset/archive and `update_today_energy`
  multi-writer/signature contract.
- **Rev 4** → added §6.1b — blame lives in cost_calculator today counters,
  reset/archived at midnight rollover, single-writer
  `update_today_energy`/`update_today_energy_archived` extended signatures, and
  all callers updated to preserve the row invariant. Added rollover +
  write-path tests (13-15). Review confirmed gaps resolved but flagged a new
  contradiction: unconditional invariant vs. backward-compat mode.
- **Rev 5** → invariant scoped to BOTH modes (backward-compat attributes all
  energy to `unattributed`); unified `residual` → `unattributed`; explicit 0.0
  init for counters. Review flagged 2 new blockers: restart/crash-recovery read
  path missing, and `start_session` init inconsistent with today_energy_wh
  persistence.
- **Rev 6** → added the Lockstep Lifecycle rule (§6.1b) — blame counters always
  mutate with `today_energy_wh` across init/restart-load, `start_session`
  (preserves, not resets), midnight rollover, and clear.
  `get_today_energy`/`_load_today_energy` extended to restore blame columns.
  Added restart-recovery + start_session-lockstep tests (16-17).
- **Rev 7** → fixed internal contradiction (blame counters NOT reset in
  `start_session`); removed stray `residual` in body (§2, §4.3); added
  `daily_energy` blame-column backfill on migration (5.2b). Review confirmed
  everything except two residual terms still in body.
- **Rev 8** (current): replaced remaining `residual` terms in §2/§4.3 with
  `remainder`; added migration-backfill test (#18); synced header to Rev 8.
