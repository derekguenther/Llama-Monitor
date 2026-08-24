# PLAN: Eliminate `aggregator_daemon.py`, backport into `aggregator.py`

**Bead:** llama-monitor-bp3 · **Status:** needs_human_input → pending plan review
**Date:** 2026-08-23

---

## 1. Problem Statement

`aggregator_daemon.py` is an accidental parallel copy of `aggregator.py` created during a
PC-layout change where two agents worked on two different copies and, when asked to merge,
produced two `Aggregator` classes instead of one. Since then the two have drifted in
parallel, causing real bugs (beads 9kf.8, 9kf.9, dmo).

### Evidence of accidental split
- Both files appeared in the **same initial commit** `036caf8` (2026-05-31).
- 9 commits touched **both** files (e.g. `f4c50ba`, `9020365`, `148b1c5`, `d9923ed`).
- Bead `dmo` (closed) explicitly flagged: "aggregator_daemon.py duplicates aggregator.py logic."
- Bead `9kf.8`: both write to `combined_metrics` with incompatible key naming (`_mb` suffix).
- Bead `9kf.9`: both write to the same tables with incompatible timestamp formats (int vs ISO).
- Bead `9kf.23`: `IdleBaselineTracker` was "dead code" that should be integrated into the
  aggregator pipeline — but it was wired into the **daemon**, not the main aggregator.

### No functional justification for keeping it
- **No launcher invokes it.** No `.bat` references it; no app code launches it.
- Its only consumers are 3 test files and a fallback hook in `web_server.py` (`get_aggregator()`).
- Its claimed NSSM/service advantage is hypothetical — one would point NSSM at `llamamonitor.py`.
- Its HTTP API (`/api/metrics`, `/api/status`, `/api/range`) is **already duplicated** in
  `web_server.py` (lines 235, 300, 602). Its `/api/shutdown`/`/api/restart` are called by nothing.

---

## 2. Scope

**In scope:** eliminate `aggregator_daemon.py`; backport its genuine enhancements into
`aggregator.py`; migrate its 3 test files; remove the per-request aggregator fallback in
`web_server.py` (rely on `metrics_cache` + DB), OR safely repoint if a fallback is truly
needed — but NEVER keep per-request `Aggregator()` instantiation (B6).

**Out of scope:** the idle-baseline / cost-attribution redesign (beads ym0, h9z0 — separate
design decision). We backport the *mechanical* idle-baseline integration only, not the
hybrid attribution model.

---

## 3. Divergence Catalog (what differs between the two)

### 3.1 Genuine enhancements in the daemon worth backporting
| # | Daemon feature | Location | aggregator.py status | Action |
|---|---|---|---|---|
| D1 | **IdleBaselineTracker integration** | `__init__` (L75), `collect_all_metrics` (L125) | absent | backport wiring |
| D2 | **Real-time elapsed-duration energy deltas** | `_calculate_cost` tracks `now - _last_cost_time` | hardcoded `duration_seconds=1.0` | backport time-tracking into cost calc |
| D3 | **Persist cumulative energy** | `store_raw_metrics` calls `update_cumulative_energy` | absent | backport persistence |
| D4 | **Session cost fields** | `_calculate_cost` adds `session_cost_usd`, `cost_rate` | partially | backport missing fields |

### 3.2 Duplicative/divergent logic to reconcile (keep aggregator.py's version)
| # | Divergence | aggregator.py (canonical) | daemon | Decision |
|---|---|---|---|---|
| C1 | `store_raw_metrics` DB methods | `insert_*_raw` + process CPU power allocation | `insert_*` (table param), no process CPU | keep aggregator.py |
| C2 | Compression | `db.compress_to_1m/1h` + `vacuum` (centralized in db.py) | inline SQL `_compress_to_minute/_hour` | keep aggregator.py |
| C3 | `safe_float` default | `0.0` | `-1.0` sentinel | **revisit** — see §5 risk |
| C4 | `collect_all_metrics` structure | returns `system_raw` + process_gpu | `_extract_*` helpers + idle check | reconcile (see D1) |
| C5 | Timestamp format | `int(time.time())` | (historically ISO) — already aligned by 9kf.9 | keep aggregator.py |

### 3.3 To DELETE (no longer needed)
- `aggregator_daemon.py` file + its `Aggregator`, `MetricsHandler`, `WebSocketHandler`,
  `create_app`, `main()`.
- The daemon's `/api/shutdown` and `/api/restart` endpoints (nothing calls them).

---

## 4. Backport Implementation Steps

### Step 1 — Backport idle-baseline integration (D1) into aggregator.py
- **NOTE:** `aggregator.py`'s `Aggregator.__init__` (L21) is **not** config-driven — it takes
  explicit `server_url/db_path/idle_baseline_w/cost_rate/collect_metrics` args and has **no
  `self.config`**. (Spec-reviewer B2.)
- Add `from idle_baseline import IdleBaselineTracker` import.
- In `Aggregator.__init__`, add (pass NO config — `IdleBaselineTracker` accepts `config=None`
  and falls back to global `get_config()`):
  ```python
  self.idle_tracker = IdleBaselineTracker(
      self.db,
      config=None,                 # falls back to global get_config()
      minimum_time_seconds=5,      # hardcode sane default (not config-driven in this class)
  )
  ```
- **SENTINEL DECISION FIRST (B3):** aggregator.py's `_safe_float` defaults to `0.0`, NOT the
  daemon's `-1.0`. A guard of `>= 0` is therefore **always true**, and `check_idle(0,0,0)`
  evaluates `(0+0) < 5` → true, writing a FALSE 0W idle baseline. To wire idle tracking
  safely, gate on **meaningful values**:
  ```python
  # Placement: just before `return` at aggregator.py L166.
  # cpu_percent is a LOCAL (L99/113); gpu_usage & system_power_w are keys in system_data.
  gpu_usage = system_data["gpu_usage"]           # L121
  system_power_w = system_data["system_power_w"] # L131
  if system_power_w > 0 and cpu_percent > 0 and gpu_usage > 0:
      self.idle_tracker.check_idle(cpu_percent, gpu_usage, system_power_w)
  ```
  - **Finding 4:** in `aggregator.py.collect_all_metrics`, only `cpu_percent` is a bare local;
    `gpu_usage`/`system_power_w` live INSIDE the `system_data` dict (L121, L131). Read them
    from `system_data` and insert BEFORE the `return` (L166), not after the metric collection.
  - This requires the `-1` sentinel question (Step 5) to be resolved FIRST. If we adopt the
    `-1` sentinel in the shared class, the guard becomes `>= 0`. If we keep `0.0`, the guard
    must be `> 0` (as above). **Decision documented in Step 5; Step 1 depends on it.**

### Step 1a — Add `last_metrics` to aggregator.py (B1)
- `web_server.py:250` reads `aggregator.last_metrics` with **no try/except**. That attribute
  exists ONLY in the daemon — aggregator.py lacks it, so repointing would crash
  `/api/metrics/latest` with `AttributeError`.
- Add to `Aggregator.__init__`: `self.last_metrics: Dict[str, Any] = {}`.
- Set `self.last_metrics = metrics` at the end of `collect_all_metrics`.

### Step 2 — Backport real-time energy deltas (D2) into store_raw_metrics
- Currently `update_power_readings(..., duration_seconds=1.0)`.
- Change to track real elapsed time:
  ```python
  now = time.time()
  if not hasattr(self, '_last_cost_time'):
      self._last_cost_time = now
  duration = now - self._last_cost_time
  self._last_cost_time = now
  ```
  then `update_power_readings(..., duration_seconds=duration)`.
- **G1 fix:** the `cost` dict built right after still hardcodes `"duration_seconds": 1.0`
  and `"duration_hours": 1.0/3600.0` (aggregator.py L280–281). These MUST use the real
  `duration` value, otherwise displayed interval duration diverges from the energy math:
  ```python
  cost = {
      ...
      "duration_seconds": duration,
      "duration_hours": duration / 3600.0,
      ...
  }
  ```
- **Risk check:** `llamamonitor.py` calls `store_raw_metrics` once per polling interval
  (configurable, default 1s). Real-duration is *more correct*. Verify no consumer assumes
  the 1.0 hardcode (grep `duration_seconds` / `duration_hours` across the codebase).

### Step 3 — Backport cumulative-energy persistence (D3) into store_raw_metrics
- After storing combined_metrics, add:
  ```python
  session_start = self.cost_calculator.session_start or \
      datetime.now().isoformat()   # G2: ISO, NOT int(time.time())
  self.db.update_cumulative_energy(
      session_start=session_start,
      total_wh=self.cost_calculator.total_energy_wh,
      gpu_wh=self.cost_calculator.gpu_energy_wh,
      cpu_wh=self.cost_calculator.cpu_energy_wh,
      session_cost_usd=self.cost_calculator.calculate_cost(self.cost_calculator.total_energy_wh),
  )
  ```
- **G2 fix (reintroducing the 9kf.9 bug class):** `session_start` is set to an ISO string by
  `start_session()`/`_load_cumulative_energy()`. The fallback MUST be ISO (`datetime.now()
  .isoformat()`), NOT `int(time.time())` — an integer would be written into a TEXT column,
  recreating the exact int-vs-ISO bug the plan eliminates.
- **Verify** `update_cumulative_energy` exists in `db.py` (confirmed at line 986) and that its
  `session_start` column is TEXT. Confirm the exact parameter names match `db.py`'s signature.

### Step 4 — Backport session cost fields (D4) into calculate_cost
- **Verify only (likely a no-op):** aggregator.py's `calculate_cost` (L338–365) already returns
  `session_cost_usd` transitively via `get_session_stats()` plus `cost_rate` (L356). Confirm
  no daemon-only cost fields are missing; if all present, record as verified and move on.
- Add missing fields only if the daemon's version has them and aggregator.py's doesn't.

### Step 5 — Reconcile `safe_float` default (C3) — **HARD PREREQUISITE for Step 1**
- **Decision needed:** aggregator.py uses `0.0` (L55); daemon uses `-1.0` sentinel. The
  sentinel detects broken data paths but risks `-1` leaking into display (guardrail).
- **This decision MUST be made BEFORE Step 1**, because the idle-check guard depends on it:
  - If `-1` sentinel adopted in shared class: idle guard is `>= 0` (sentinel-safe).
  - If `0.0` kept (recommended for this merge): idle guard is `> 0` (meaningful-value),
    as written in Step 1.
- **Recommendation (keep `0.0`):** do NOT adopt `-1` in the shared class during this merge.
  llamamonitor.py and the dashboard are built around `0.0`. The `-1` sentinel unification
  becomes a follow-up design bead. Step 1 uses the `> 0` guard accordingly.
- **Flag follow-up** for sentinel `-1` vs `0` unification (see §7).

### Step 6 — Rework web_server.py's aggregator coupling (B1/B6/G4)
**Do NOT simply repoint `get_aggregator()` to aggregator.py's `Aggregator`.** That class
opens `Database("llama-monitor.db")` (relative path, not config's `database.path`), calls
`set_cost_rate()` (a write), and constructs real collectors (`nvmlInit()`/`wmi.WMI()`) —
**per HTTP request** (B6). This contradicts web_server's own documented single-connection
design (L70–75) that fixes the DB-corruption bug.

**S1 (recommended): drop the per-request aggregator fallback entirely.**
- `llamamonitor.py` already shares `metrics_cache` with web_server (L271), and
  `/api/metrics/latest` checks it FIRST (L239). The aggregator fallback block (L248–256) is
  redundant and dangerous.
- Remove the aggregator-fallback block in `/api/metrics/latest` (L248–256), keeping
  metrics_cache → DB fallback.
- Remove/disable `get_aggregator()`, the `AGGREGATOR_AVAILABLE` try/except (L40–44), and the
  now-dead `fetch_metrics_from_aggregator()` (G3, L100–117).
- **Finding 1 (NEW — CRITICAL): rework `api_status()` (L602–615)** — it is a THIRD consumer
  of `AGGREGATOR_AVAILABLE` (L605) and `get_aggregator()` (L606). Removing those definitions
  without touching `api_status` → `NameError` → 500 on `/api/status`, which the settings page
  polls (`web_server.py:1076`). Rework it to report standalone unconditionally:
  ```python
  @app.route("/api/status")
  def api_status():
      """Return aggregator status (standalone; no separate daemon)."""
      return jsonify({"status": "standalone", "aggregator_available": False})
  ```
- **Finding 5: commit to S1.** Do NOT keep S2 as an open alternative. Step 1a's `last_metrics`
  is then dead in web_server.py (harmless — keep it for the aggregator's own consumers/tests),
  and DoD must reflect the S1-only decision.

**S2 (if a fallback is truly needed):** instead of `Aggregator()`, read from the shared DB
connection using `fetch_metrics_from_database()` (already used as the final fallback), and
add `last_metrics` to aggregator.py (Step 1a) so the attribute access at L250 is valid.

- **G4 note:** aggregator.py's `Aggregator` always constructs successfully (no server
  dependency in `__init__`), so `AGGREGATOR_AVAILABLE` would be permanently `True` if kept.
  Dropping the block avoids this semantic change.

### Step 7 — Migrate the 3 test files (B4/B5/G5)
This is **NOT** a simple import change — each file needs distinct handling:

- **`test_slot_charts.py`**:
  - Change `from aggregator_daemon import Aggregator` (L9) → `from aggregator import Aggregator`.
  - **B5:** repoint EVERY `@patch("aggregator_daemon.X")` decorator (L119, 140, 168, 181,
    244–247) to `"aggregator.X"` (e.g. `aggregator.ServerMetricsCollector`,
    `aggregator.SystemMetricsCollector`, `aggregator.ElectricityCostCalculator`,
    `aggregator.Database`). Otherwise the mocks won't intercept and `Aggregator()` constructs
    REAL collectors + `Database("llama-monitor.db")`, writing to production during tests.
  - **Finding 2 (NEW — HIGH): the return shape differs.** `test_full_metrics_flow_with_slots`
    asserts `assertIn("cost", result)` (L310). aggregator.py's `collect_all_metrics` returns
    `{timestamp, server, system, process_gpu, system_raw}` — **NO `"cost"` key** (daemon-only).
    This test will fail post-migration. Rewrite the assertion to aggregator.py's shape: drop
    the `assertIn("cost", result)` line, OR assert cost via `store_raw_metrics`/`cost_data`.
  - **Finding 3 (NEW — MEDIUM): patch `IdleBaselineTracker` too.** After Step 1 wires
    `self.idle_tracker` into aggregator.py's `__init__`, the tests construct real `Aggregator()`
    (L153, L194, L299), which instantiates a real `IdleBaselineTracker` → calls `get_config()`
    → reads `config.yaml`. Safe but unexamined coupling. Add
    `@patch("aggregator.IdleBaselineTracker")` to each test for isolation.

- **`test_active_slots_fix.py`**:
  - **B4:** L169 calls `Aggregator._extract_server_metrics(...)`, a **daemon-only** method
    absent from aggregator.py. aggregator.py does inline extraction. Options:
    (a) backport a `_extract_server_metrics` static method to aggregator.py and call it, OR
    (b) rewrite the test to call the inline extraction path (e.g. `collect_all_metrics` with a
    mocked server collector) and assert `slots`/`state` in the result.
  - Verify what the test actually asserts (slots extraction) and pick the option that keeps
    coverage without the daemon.

- **`test_config.py`**:
  - **G5:** L103 docstring claims "Aggregator can access all required config attributes" but
    the body only tests `Config` and never instantiates `Aggregator`. aggregator.py is NOT
    config-driven, so "verify config-integration against the new signature" is meaningless.
  - Change the import to `from aggregator import Aggregator` (if referenced) and fix the
    docstring to reflect what the test actually does (tests `Config` only).

### Step 8 — Delete aggregator_daemon.py
- Remove the file (after all consumers are repointed).
- **Guardrail check:** this is a tracked git file being intentionally removed as part of the
  documented merge (bead dmo/bp3) — NOT a user-owned untracked file. Safe to delete.

---

## 5. Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| `/api/metrics/latest` crashes on `last_metrics` after repoint (B1) | **Critical** | Add `last_metrics` to aggregator.py (Step 1a) OR drop the fallback block (Step 6) |
| Per-request `Aggregator()` opens DB writers / corrupts DB (B6) | **Critical** | Do NOT keep `get_aggregator()` returning `Aggregator()` per request; drop fallback (Step 6 S1) |
| False idle baseline from `0.0` defaults passing `>= 0` guard (B3) | High | Resolve sentinel decision FIRST (Step 5); use `> 0` guard if keeping `0.0` (Step 1) |
| Backporting `-1` sentinel into shared class breaks llamamonitor.py/dashboard | High | Keep `0.0` default; flag `-1` as separate follow-up |
| Test migration breaks on daemon-only methods (B4/B5) | High | Repoint all `@patch` paths; rewrite `_extract_server_metrics` call (Step 7) |
| Real-time duration changes energy accumulation behavior (G1) | Medium | Verify polling interval; update duration literals in cost dict; add duration test |
| IdleBaselineTracker wiring changes aggregator.py behavior | Medium | Gate `check_idle` on meaningful values (`> 0`); existing tests guard regressions |
| `update_cumulative_energy` column mismatch | Medium | Verify db.py schema (L986) + parameter names; add test |
| `session_start` fallback type hazard (G2) | Medium | Use ISO fallback, NOT `int(time.time())` (Step 3) |

---

## 6. Test Plan
- Run `python3 test_llama-monitor.py` after each step (6/6 currently passing baseline).
- Add `test_idle_tracking.py`: assert `collect_all_metrics` calls `check_idle` when values are
  meaningful (`> 0`) and does NOT when all zero (per the resolved sentinel decision).
- Add a test asserting `store_raw_metrics` persists cumulative energy (D3), with ISO
  `session_start`.
- Add a test asserting real-duration is used (D2) AND that the `cost_data["duration_seconds"]`
  matches the real elapsed time, not the hardcoded 1.0 (S4).
- Add a test asserting `last_metrics` is set on aggregator.py's `collect_all_metrics` (B1).
- After Step 7, run each migrated test file and confirm it passes with mocks intercepting
  (including `test_full_metrics_flow_with_slots` after the `"cost"` assertion is fixed, and
  `IdleBaselineTracker` patched).
- Add a test asserting `/api/status` returns `{"status": "standalone", "aggregator_available":
  False}` and does NOT 500 after Step 6 S1 (Finding 1).
- After Step 8, confirm zero references to `aggregator_daemon` remain in code (except git
  history): `grep -rn "aggregator_daemon" --include="*.py"`.

---

## 7. Out-of-Scope Follow-ups (file new beads after merge)
- Sentinel `-1` vs `0` default unification (design decision).
- Idle-baseline hybrid attribution model (ym0, h9z0).
- Whether daemon HTTP endpoints `/api/shutdown`/`/api/restart` should be resurrected in web_server.py.

---

## 8. Definition of Done
- `aggregator_daemon.py` deleted.
- All backports in `aggregator.py` (idle wiring, real-duration + duration literals, cumulative
  energy with ISO session_start, `last_metrics`), all tests passing.
- `web_server.py` aggregator coupling removed per **S1**: `get_aggregator()`,
  `AGGREGATOR_AVAILABLE`, `fetch_metrics_from_aggregator()`, the `/api/metrics/latest`
  aggregator fallback block, AND `api_status()` reworked — NO per-request `Aggregator()`.
- 3 test files migrated and passing (all `@patch` paths repointed, no daemon-only methods).
- Zero references to `aggregator_daemon` in code (except git history).
- Bead bp3 closed; follow-up beads filed for sentinel unification & idle-baseline design.
