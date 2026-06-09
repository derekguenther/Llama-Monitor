#!/usr/bin/env python3
"""Test aggregator directly."""
import json
from aggregator import Aggregator

print("Initializing aggregator...")
agg = Aggregator(
    server_url="http://localhost:8000",
    db_path="llama_monitor.db",
    idle_baseline_w=150.0,
    cost_rate=0.12,
    collect_metrics=True
)

print("Collecting metrics...")
metrics = agg.collect_all_metrics()

print("\nCollected metrics:")
print(f"  timestamp: {metrics.get('timestamp')}")
print(f"  server keys: {list(metrics.get('server', {}).keys())}")
print(f"  system keys: {list(metrics.get('system', {}).keys())}")

server = metrics.get('server', {})
system = metrics.get('system', {})

print("\nServer metrics:")
print(f"  prompt_tokens_total: {server.get('prompt_tokens_total')}")
print(f"  tokens_predicted_total: {server.get('tokens_predicted_total')}")

print("\nSystem metrics:")
cpu = system.get('cpu', {})
gpu = system.get('gpu', {})
memory = system.get('memory', {})
print(f"  cpu.percent: {cpu.get('percent')}")
print(f"  gpu.usage: {gpu.get('usage')}")
print(f"  gpu.memory_used: {gpu.get('memory_used')}")
print(f"  memory.used: {memory.get('used')}")

print("\nStoring metrics...")
agg.store_raw_metrics(metrics)

print("Checking database after storage...")
import sqlite3
conn = sqlite3.connect('llama_monitor.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM combined_metrics')
print(f'  combined_metrics row count: {cursor.fetchone()[0]}')
cursor.execute('SELECT timestamp, server_data, system_data FROM combined_metrics ORDER BY timestamp DESC LIMIT 1')
row = cursor.fetchone()
if row:
    print(f'  Latest: ts={row["timestamp"]}')
    server_data = json.loads(row["server_data"])
    system_data = json.loads(row["system_data"])
    print(f'    server prompt_tokens_total: {server_data.get("prompt_tokens_total")}')
    print(f'    system cpu.percent: {system_data.get("cpu", {}).get("percent")}')
conn.close()

agg.close()
print("\nDone!")
