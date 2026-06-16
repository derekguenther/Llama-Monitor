---
name: database-corruption-fixes
description: Implementation of fixes for SQLite database corruption
metadata:
  type: project
---

## SQLite Database Corruption Fixes

### Problem
The SQLite database became malformed twice with "database disk image is malformed" errors. Root causes identified:
1. Unlocked database operations - many methods bypassed the threading lock
2. Race condition - `update_today_energy()` called every second while compression runs
3. Connection sharing without proper isolation (`check_same_thread=False`)
4. No Write-Ahead Logging (WAL) mode enabled
5. No retry logic for locked database errors

### Fixes Implemented in db.py

1. **WAL Mode** (line 48): `self.conn.execute("PRAGMA journal_mode=WAL")`
   - Enables better concurrency for read/write operations

2. **Busy Timeout** (line 51): `self.conn.execute("PRAGMA busy_timeout=30000")`
   - 30 second timeout for lock waiting

3. **Retry Logic** (lines 79-120): `_execute_with_retry()` helper
   - Retries up to 3 times with exponential backoff (0.1s, 0.2s, 0.4s)
   - Catches "database is locked" OperationalErrors

4. **Lock Coverage** - All database methods now use `with self._lock:`:
   - `get_cumulative_energy()` (line 1022)
   - `get_today_energy()` (line 1042)
   - `get_monthly_energy()` (line 1067)
   - `get_server_metrics()` (line 1164)
   - `get_system_metrics()` (line 1201)
   - `get_tables()` (line 1262)
   - `get_setting()` (line 1272)
   - `get_all_token_tracking()` (line 1411)
   - `get_all_vendor_rates()` (line 1420)
   - `get_vendor_rate_by_name()` (line 1439)
   - `compress_to_1m()` (line 1548)
   - `compress_to_1h()` (line 1685)
   - `vacuum()` (line 1224)
   - `get_table_size()` (line 1251)

5. **Integrity Checks** (lines 1228-1240): `integrity_check()` method
   - Runs `PRAGMA integrity_check` to detect corruption early

### Test Results
- 33 of 34 tests pass (1 pre-existing failure unrelated to these changes)

### Related Beads Issues
- `llama-monitor-001`: Fix SQLite database corruption - database disk image is malformed (P0, CLOSED)
- `llama-monitor-jml`: Database Corruption Recovery (P0, in_progress)
