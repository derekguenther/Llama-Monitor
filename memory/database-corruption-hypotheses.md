---
name: database-corruption-hypotheses
description: Hypotheses for SQLite database corruption causes
metadata:
  type: reference
---

## SQLite Database Corruption - Hypotheses

The database has become malformed twice. Here are the potential causes based on code analysis:

### 1. Concurrent Write Without Proper Locking (Most Likely)

**Location:** `db.py` lines 72-89, `electricity_cost.py` lines 255-260

**Problem:** The `execute()` method uses `with self._lock:` but several methods **bypass the lock entirely**:

```python
# db.py line 72-89 - execute() uses lock correctly
def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
    with self._lock:  # ✓ Lock is used
        cursor = self.conn.cursor()
        ...
        self.conn.commit()
```

But many methods **do NOT use the lock**:
- `get_today_energy()` (line 984-1003) - SELECT only, but...
- `get_server_metrics()` (line 1092+) - SELECT only
- `get_system_metrics()` (line 1129+) - SELECT only
- Many `execute()` calls in `compress_to_1m()` and `compress_to_1h()` bypass lock

**Critical Issue:** `electricity_cost.py` line 256 calls `update_today_energy()` every **second** during `update_power_readings()`. If `compress_to_1m()` or `compress_to_1h()` runs concurrently (which also modifies the `daily_energy` table), there could be write conflicts even though locks exist.

### 2. RLock Reentrancy Issue

**Location:** `db.py` line 26

```python
self._lock = threading.RLock()  # Reentrant lock for thread-safe access
```

While `RLock` allows reentrant locking (same thread can acquire multiple times), it doesn't help if:
- Thread A acquires lock, then calls a method that indirectly calls another locked method
- Thread B tries to acquire while Thread A is still in nested calls
- The lock acquisition doesn't prevent the issue if connection is shared

### 3. Connection Sharing Without Proper Isolation

**Location:** `db.py` line 44

```python
self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
```

The `check_same_thread=False` allows using the connection from any thread, but SQLite connections are **not truly thread-safe** even with locks:
- Multiple threads can call methods on the same connection
- But SQLite's internal state can get corrupted if transactions overlap
- The `commit()` at line 88 happens inside the lock, but the connection's internal state is shared

### 4. Write-Ahead Logging (WAL) Mode Not Enabled

SQLite's default locking mode is `LOCKING_MODE = EXCLUSIVE`, which can cause issues with concurrent access. WAL mode would allow better concurrency.

### 5. Compression Running During Power Readings

**Location:** `electricity_cost.py` line 256

```python
# Persist today's energy to database (every second for crash recovery)
self.database.update_today_energy(...)
```

This runs every second. Meanwhile, `compress_to_1m()` and `compress_to_1h()` can run periodically (every 5 minutes in aggregator_daemon.py). If compression coincides with a power reading update, both are trying to modify the `daily_energy` table.

### 6. No Write Retry Logic for Locked Database

SQLite can return `database is locked` errors. The code doesn't implement any retry logic with exponential backoff, so transient lock conflicts could lead to incomplete transactions and corruption.

### 7. Memory-Mapped I/O Issues

If the system has memory pressure or the database file is on a network drive, memory-mapped I/O could cause issues. The code doesn't configure `mmap_size` or disable mmap.

## Recommended Fixes

1. **Ensure all database operations use the lock** - wrap every cursor operation with `with self._lock:`
2. **Enable WAL mode** - `PRAGMA journal_mode=WAL` after connection
3. **Add retry logic** - wrap execute/commit in retry loop with backoff
4. **Use separate connections per thread** - or use SQLite's serialized threading mode
5. **Add database integrity checks** - run `PRAGMA integrity_check` periodically
