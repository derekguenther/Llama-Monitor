import sqlite3
import json

conn = sqlite3.connect('/c/Users/ClaudeCode/Documents/llama-monitor/llama-monitor.db')
cursor = conn.cursor()

# Check tables
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables:', [t[0] for t in tables])

# Check combined_metrics columns
try:
    cols = cursor.execute('PRAGMA table_info(combined_metrics)').fetchall()
    print('combined_metrics columns:', [c[1] for c in cols])
except Exception as e:
    print('Error getting columns:', e)

# Check row counts
for table in ['server_metrics_raw', 'system_metrics_raw', 'combined_metrics']:
    try:
        count = cursor.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f'{table}: {count} rows')
    except Exception as e:
        print(f'{table}: error - {e}')

# Check latest combined_metrics
row = cursor.execute('SELECT timestamp, server_data, system_data, cost_data, process_gpu_data FROM combined_metrics ORDER BY timestamp DESC LIMIT 1').fetchone()
if row:
    print('\n=== LATEST COMBINED METRICS ===')
    print(f'Timestamp: {row["timestamp"]}')
    server = json.loads(row['server_data'])
    system = json.loads(row['system_data'])
    cost = json.loads(row['cost_data'])
    print(f'Server keys: {list(server.keys())}')
    print(f'System keys: {list(system.keys())}')
    print(f'Cost: {cost}')
    if row[4]:
        process_gpu = json.loads(row['process_gpu_data'])
        print(f'Process GPU: {process_gpu}')
else:
    print('\nNo data in combined_metrics')

conn.close()
