#!/usr/bin/env python3
"""Check database for metrics data."""
import json
from db import Database

db = Database('llama_monitor.db')
db.connect()

# Check combined_metrics
cursor = db.conn.cursor()
cursor.execute('SELECT COUNT(*) FROM combined_metrics')
count = cursor.fetchone()[0]
print(f'combined_metrics row count: {count}')

cursor.execute('SELECT timestamp, server_data, system_data FROM combined_metrics ORDER BY timestamp DESC LIMIT 3')
rows = cursor.fetchall()
print('\nRecent combined_metrics:')
for row in rows:
    print(f'  ts={row[0]}')
    if row[1]:
        server = json.loads(row[1])
        print(f'    server keys: {list(server.keys())}')
    if row[2]:
        system = json.loads(row[2])
        print(f'    system keys: {list(system.keys())}')

db.close()
