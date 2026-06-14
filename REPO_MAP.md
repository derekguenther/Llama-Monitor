./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:class Aggregator:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def __init__(
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def compress_if_needed(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def close(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def __enter__(self):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:class Aggregator:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def connect(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def close(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def check_compression(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:        def collection_loop():
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def stop(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def log_message(self, format, *args):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def do_GET(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _handle_status(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:        def do_shutdown():
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def _handle_restart(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:        def do_restart():
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:class WebSocketHandler:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:        def handle_connect(sid):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:        def handle_disconnect(sid):
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./.claude/worktrees/agent-a10a5789c899fd06f/aggregator_daemon.py:def main() -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/cli_stats.py:def parse_args():
./.claude/worktrees/agent-a10a5789c899fd06f/cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./.claude/worktrees/agent-a10a5789c899fd06f/cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a10a5789c899fd06f/cli_stats.py:def main():
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:class Config:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def _load_config(self, config_path: str) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def get(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def set(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def get_compression_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:    def get_server_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:def find_config(default_path: str = "config.yaml") -> str:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:def load_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:def get_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a10a5789c899fd06f/config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:class Database:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def __init__(self, db_path: str):
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def _ensure_directory(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def connect(self) -> sqlite3.Connection:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def close(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def __enter__(self) -> "Database":
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def lock(self):
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def _initialize_schema(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_server_metrics(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_system_metrics(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_process_gpu_metrics(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_idle_baseline(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_server_metrics_raw(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_system_metrics_raw(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_process_gpu_metrics_raw(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def insert_process_cpu_metrics_raw(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def update_cumulative_energy(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_server_metrics(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_system_metrics(
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def vacuum(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_table_size(self, table: str) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_tables(self) -> List[str]:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def set_setting(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_cost_rate(self) -> float:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def compress_to_1m(self) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def compress_to_1h(self) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/db.py:    def get_daily_cost_data(self, days: int = 30) -> List[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:class ElectricityCostCalculator:
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def __init__(
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def start_session(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def calculate_power_cost(
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def update_power_readings(
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def calculate_idle_baseline(
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def format_cost_display(
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:class IdleBaselineTracker:
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:    def __init__(
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:    def check_idle(
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:    def clear_baseline_data(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/idle_baseline.py:    def reset(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:class MetricsCache:
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def __init__(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def update(self, metrics: Dict[str, Any]):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def get(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:class Monitor:
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def __init__(
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def initialize(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def run_aggregator_loop(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def shutdown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def run_web_mode(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def run_tui_mode(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def show_statistics(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def run(self):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:def parse_args() -> argparse.Namespace:
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:def ensure_dependencies(check_tui: bool = False):
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:def main():
./.claude/worktrees/agent-a10a5789c899fd06f/main.py:    def signal_handler(signum, frame):
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:class ServerMetricsCollector:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./.claude/worktrees/agent-a10a5789c899fd06f/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:class SystemMetricsCollector:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _init_nvml(self) -> bool:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def close(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _get_cpu_power_w(self) -> float:
./.claude/worktrees/agent-a10a5789c899fd06f/system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_init_creates_all_components(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_context_manager(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:class TestConfigDefaults(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_database_path_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_server_url_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_server_metrics_endpoint_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_tracked_processes_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_compression_enabled_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_polling_interval_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_web_http_port_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:class TestConfigSetMethod(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_set_simple_key(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_set_nested_key(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_set_nested_key_creates_intermediate(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_override_existing_value(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:class TestConfigIntegration(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_config.py:    def test_aggregator_config_attributes(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestDatabaseInit(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_connect_creates_connection(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_context_manager(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_schema_version_created(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestServerMetrics(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_insert_server_metrics(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_get_server_metrics_with_filter(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_get_server_metrics_limit(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestSystemMetrics(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_insert_system_metrics(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_get_system_metrics(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestIdleBaseline(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_insert_idle_baseline(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_insert_invalid_idle_baseline(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_update_and_get_cumulative_energy(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_get_cumulative_energy_empty(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestSettings(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_set_and_get_setting(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_get_setting_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_cost_rate_default(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_set_cost_rate(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_insert_process_gpu_metrics(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestDatabaseTables(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_all_tables_created(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_table_row_counts(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestSchemaValidation(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_create_table_columns_match_insert_statements(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:class TestCompression(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_database.py:    def test_compression_with_data(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_imports.py:def test_imports():
./.claude/worktrees/agent-a10a5789c899fd06f/test_llama-monitor.py:def run_tests():
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_make_request_success(self, mock_get):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_get_props(self, mock_make_request):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_collect(self, mock_make_request):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_metrics_dict(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_slots_list(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_slots_dict_single(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_slots_empty_list(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_slots_none(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_format_metrics_display_full(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_format_metrics_display_empty(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_init_default_tracked_processes(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestContextManager(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_enter_returns_self(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_memory_success(self):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:class TestCollect(unittest.TestCase):
./.claude/worktrees/agent-a10a5789c899fd06f/test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:class TUI:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _init_colors(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_header(self, stdscr) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _draw_footer(self, stdscr) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def _main_loop(self, stdscr) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def run(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:    def stop(self) -> None:
./.claude/worktrees/agent-a10a5789c899fd06f/tui.py:def main() -> int:
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def get_aggregator() -> Optional[Aggregator]:
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def get_config() -> Any:
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def index() -> str:
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def api_latest_metrics():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def api_latest_metrics_db():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def api_range_metrics():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def api_monthly_cost():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def api_metrics_list():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def api_status():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def handle_connect():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def handle_disconnect():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False):
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None):
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:    def run():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def stop_server():
./.claude/worktrees/agent-a10a5789c899fd06f/web_server.py:def main():
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:class Aggregator:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def __init__(
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def compress_if_needed(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def close(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def __enter__(self):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:class Aggregator:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def connect(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def close(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def check_compression(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:        def collection_loop():
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def stop(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def log_message(self, format, *args):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def do_GET(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _handle_status(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:        def do_shutdown():
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def _handle_restart(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:        def do_restart():
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:class WebSocketHandler:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:        def handle_connect(sid):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:        def handle_disconnect(sid):
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./.claude/worktrees/agent-a666ec159e0856a2b/aggregator_daemon.py:def main() -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/cli_stats.py:def parse_args():
./.claude/worktrees/agent-a666ec159e0856a2b/cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./.claude/worktrees/agent-a666ec159e0856a2b/cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a666ec159e0856a2b/cli_stats.py:def main():
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:class Config:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def _load_config(self, config_path: str) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def get(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def set(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def get_compression_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:    def get_server_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:def find_config(default_path: str = "config.yaml") -> str:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:def load_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:def get_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a666ec159e0856a2b/config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:class Database:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def __init__(self, db_path: str):
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def _ensure_directory(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def connect(self) -> sqlite3.Connection:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def close(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def __enter__(self) -> "Database":
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def lock(self):
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def _initialize_schema(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_server_metrics(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_system_metrics(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_process_gpu_metrics(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_idle_baseline(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_server_metrics_raw(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_system_metrics_raw(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_process_gpu_metrics_raw(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def insert_process_cpu_metrics_raw(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def update_cumulative_energy(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def get_server_metrics(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def get_system_metrics(
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def vacuum(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def get_table_size(self, table: str) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def get_tables(self) -> List[str]:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def set_setting(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def get_cost_rate(self) -> float:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def compress_to_1m(self) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/db.py:    def compress_to_1h(self) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:class ElectricityCostCalculator:
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def __init__(
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def start_session(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def calculate_power_cost(
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def update_power_readings(
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def calculate_idle_baseline(
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def format_cost_display(
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:class IdleBaselineTracker:
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:    def __init__(
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:    def check_idle(
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:    def clear_baseline_data(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/idle_baseline.py:    def reset(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:class MetricsCache:
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def __init__(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def update(self, metrics: Dict[str, Any]):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def get(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:class Monitor:
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def __init__(
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def initialize(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def run_aggregator_loop(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def shutdown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def run_web_mode(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def run_tui_mode(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def show_statistics(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def run(self):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:def parse_args() -> argparse.Namespace:
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:def ensure_dependencies(check_tui: bool = False):
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:def main():
./.claude/worktrees/agent-a666ec159e0856a2b/main.py:    def signal_handler(signum, frame):
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:class ServerMetricsCollector:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./.claude/worktrees/agent-a666ec159e0856a2b/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:class SystemMetricsCollector:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _init_nvml(self) -> bool:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def close(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _get_cpu_power_w(self) -> float:
./.claude/worktrees/agent-a666ec159e0856a2b/system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_init_creates_all_components(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_context_manager(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:class TestConfigDefaults(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_database_path_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_server_url_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_server_metrics_endpoint_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_tracked_processes_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_compression_enabled_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_polling_interval_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_web_http_port_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:class TestConfigSetMethod(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_set_simple_key(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_set_nested_key(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_set_nested_key_creates_intermediate(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_override_existing_value(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:class TestConfigIntegration(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_config.py:    def test_aggregator_config_attributes(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestDatabaseInit(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_connect_creates_connection(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_context_manager(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_schema_version_created(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestServerMetrics(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_insert_server_metrics(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_get_server_metrics_with_filter(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_get_server_metrics_limit(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestSystemMetrics(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_insert_system_metrics(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_get_system_metrics(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestIdleBaseline(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_insert_idle_baseline(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_insert_invalid_idle_baseline(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_update_and_get_cumulative_energy(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_get_cumulative_energy_empty(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestSettings(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_set_and_get_setting(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_get_setting_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_cost_rate_default(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_set_cost_rate(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_insert_process_gpu_metrics(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestDatabaseTables(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_all_tables_created(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_table_row_counts(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestSchemaValidation(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_create_table_columns_match_insert_statements(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:class TestCompression(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_database.py:    def test_compression_with_data(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_imports.py:def test_imports():
./.claude/worktrees/agent-a666ec159e0856a2b/test_llama-monitor.py:def run_tests():
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_make_request_success(self, mock_get):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_get_props(self, mock_make_request):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_collect(self, mock_make_request):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_metrics_dict(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_slots_list(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_slots_dict_single(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_slots_empty_list(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_slots_none(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_format_metrics_display_full(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_format_metrics_display_empty(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_init_default_tracked_processes(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestContextManager(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_enter_returns_self(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_memory_success(self):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:class TestCollect(unittest.TestCase):
./.claude/worktrees/agent-a666ec159e0856a2b/test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:class TUI:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _init_colors(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_header(self, stdscr) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _draw_footer(self, stdscr) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def _main_loop(self, stdscr) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def run(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:    def stop(self) -> None:
./.claude/worktrees/agent-a666ec159e0856a2b/tui.py:def main() -> int:
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def get_aggregator() -> Optional[Aggregator]:
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def get_config() -> Any:
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def index() -> str:
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def api_latest_metrics():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def api_latest_metrics_db():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def api_range_metrics():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def api_metrics_list():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def api_status():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def handle_connect():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def handle_disconnect():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False):
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None):
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:    def run():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def stop_server():
./.claude/worktrees/agent-a666ec159e0856a2b/web_server.py:def main():
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:class Aggregator:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def __init__(
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def compress_if_needed(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def close(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def __enter__(self):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:class Aggregator:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def connect(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def close(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def check_compression(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:        def collection_loop():
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def stop(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def log_message(self, format, *args):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def do_GET(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _handle_status(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:        def do_shutdown():
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def _handle_restart(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:        def do_restart():
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:class WebSocketHandler:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:        def handle_connect(sid):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:        def handle_disconnect(sid):
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./.claude/worktrees/agent-a791d6738f913ef7f/aggregator_daemon.py:def main() -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/cli_stats.py:def parse_args():
./.claude/worktrees/agent-a791d6738f913ef7f/cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./.claude/worktrees/agent-a791d6738f913ef7f/cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a791d6738f913ef7f/cli_stats.py:def main():
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:class Config:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def _load_config(self, config_path: str) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def get(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def set(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def get_compression_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:    def get_server_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:def find_config(default_path: str = "config.yaml") -> str:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:def load_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:def get_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a791d6738f913ef7f/config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:class Database:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def __init__(self, db_path: str):
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def _ensure_directory(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def connect(self) -> sqlite3.Connection:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def close(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def __enter__(self) -> "Database":
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def lock(self):
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def _initialize_schema(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_server_metrics(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_system_metrics(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_process_gpu_metrics(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_idle_baseline(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_server_metrics_raw(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_system_metrics_raw(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_process_gpu_metrics_raw(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def insert_process_cpu_metrics_raw(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def update_cumulative_energy(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def get_server_metrics(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def get_system_metrics(
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def vacuum(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def get_table_size(self, table: str) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def get_tables(self) -> List[str]:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def set_setting(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def get_cost_rate(self) -> float:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def compress_to_1m(self) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/db.py:    def compress_to_1h(self) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:class ElectricityCostCalculator:
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def __init__(
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def start_session(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def calculate_power_cost(
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def update_power_readings(
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def calculate_idle_baseline(
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def format_cost_display(
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:class IdleBaselineTracker:
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:    def __init__(
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:    def check_idle(
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:    def clear_baseline_data(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/idle_baseline.py:    def reset(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:class MetricsCache:
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def __init__(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def update(self, metrics: Dict[str, Any]):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def get(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:class Monitor:
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def __init__(
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def initialize(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def run_aggregator_loop(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def shutdown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def run_web_mode(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def run_tui_mode(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def show_statistics(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def run(self):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:def parse_args() -> argparse.Namespace:
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:def ensure_dependencies(check_tui: bool = False):
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:def main():
./.claude/worktrees/agent-a791d6738f913ef7f/main.py:    def signal_handler(signum, frame):
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:class ServerMetricsCollector:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./.claude/worktrees/agent-a791d6738f913ef7f/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:class SystemMetricsCollector:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _init_nvml(self) -> bool:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def close(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _get_cpu_power_w(self) -> float:
./.claude/worktrees/agent-a791d6738f913ef7f/system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_init_creates_all_components(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_context_manager(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:class TestConfigDefaults(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_database_path_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_server_url_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_server_metrics_endpoint_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_tracked_processes_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_compression_enabled_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_polling_interval_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_web_http_port_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:class TestConfigSetMethod(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_set_simple_key(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_set_nested_key(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_set_nested_key_creates_intermediate(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_override_existing_value(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:class TestConfigIntegration(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_config.py:    def test_aggregator_config_attributes(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestDatabaseInit(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_connect_creates_connection(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_context_manager(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_schema_version_created(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestServerMetrics(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_insert_server_metrics(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_get_server_metrics_with_filter(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_get_server_metrics_limit(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestSystemMetrics(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_insert_system_metrics(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_get_system_metrics(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestIdleBaseline(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_insert_idle_baseline(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_insert_invalid_idle_baseline(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_update_and_get_cumulative_energy(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_get_cumulative_energy_empty(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestSettings(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_set_and_get_setting(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_get_setting_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_cost_rate_default(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_set_cost_rate(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_insert_process_gpu_metrics(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestDatabaseTables(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_all_tables_created(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_table_row_counts(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestSchemaValidation(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_create_table_columns_match_insert_statements(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:class TestCompression(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_database.py:    def test_compression_with_data(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_imports.py:def test_imports():
./.claude/worktrees/agent-a791d6738f913ef7f/test_llama-monitor.py:def run_tests():
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_make_request_success(self, mock_get):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_get_props(self, mock_make_request):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_collect(self, mock_make_request):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_metrics_dict(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_slots_list(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_slots_dict_single(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_slots_empty_list(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_slots_none(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_format_metrics_display_full(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_format_metrics_display_empty(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_init_default_tracked_processes(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestContextManager(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_enter_returns_self(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_memory_success(self):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:class TestCollect(unittest.TestCase):
./.claude/worktrees/agent-a791d6738f913ef7f/test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:class TUI:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _init_colors(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_header(self, stdscr) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _draw_footer(self, stdscr) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def _main_loop(self, stdscr) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def run(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:    def stop(self) -> None:
./.claude/worktrees/agent-a791d6738f913ef7f/tui.py:def main() -> int:
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def get_aggregator() -> Optional[Aggregator]:
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def get_config() -> Any:
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def index() -> str:
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def api_latest_metrics():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def api_latest_metrics_db():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def api_range_metrics():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def api_metrics_list():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def api_status():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def handle_connect():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def handle_disconnect():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False):
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None):
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:    def run():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def stop_server():
./.claude/worktrees/agent-a791d6738f913ef7f/web_server.py:def main():
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:class Aggregator:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def __init__(
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def compress_if_needed(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def close(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def __enter__(self):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:class Aggregator:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def connect(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def close(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def check_compression(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:        def collection_loop():
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def stop(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def log_message(self, format, *args):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def do_GET(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _handle_status(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:        def do_shutdown():
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def _handle_restart(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:        def do_restart():
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:class WebSocketHandler:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:        def handle_connect(sid):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:        def handle_disconnect(sid):
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./.claude/worktrees/agent-a9869eb207a425b4a/aggregator_daemon.py:def main() -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/cli_stats.py:def parse_args():
./.claude/worktrees/agent-a9869eb207a425b4a/cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./.claude/worktrees/agent-a9869eb207a425b4a/cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a9869eb207a425b4a/cli_stats.py:def main():
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:class Config:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def _load_config(self, config_path: str) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def get(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def set(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def get_compression_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:    def get_server_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:def find_config(default_path: str = "config.yaml") -> str:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:def load_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:def get_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a9869eb207a425b4a/config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:class Database:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def __init__(self, db_path: str):
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def _ensure_directory(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def connect(self) -> sqlite3.Connection:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def close(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def __enter__(self) -> "Database":
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def lock(self):
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def _initialize_schema(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_server_metrics(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_system_metrics(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_process_gpu_metrics(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_idle_baseline(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_server_metrics_raw(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_system_metrics_raw(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_process_gpu_metrics_raw(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def insert_process_cpu_metrics_raw(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def update_cumulative_energy(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def update_daily_energy(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_daily_energy(self, date: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_today_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_server_metrics(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_system_metrics(
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def vacuum(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_table_size(self, table: str) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_tables(self) -> List[str]:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def set_setting(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def get_cost_rate(self) -> float:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def compress_to_1m(self) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/db.py:    def compress_to_1h(self) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:class ElectricityCostCalculator:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def __init__(
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def _get_today_date(self) -> str:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def _load_today_energy(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def start_session(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def calculate_power_cost(
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def update_power_readings(
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def calculate_idle_baseline(
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def format_cost_display(
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:class IdleBaselineTracker:
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:    def __init__(
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:    def check_idle(
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:    def clear_baseline_data(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/idle_baseline.py:    def reset(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:class MetricsCache:
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def __init__(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def update(self, metrics: Dict[str, Any]):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def get(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:class Monitor:
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def __init__(
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def initialize(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def run_aggregator_loop(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def shutdown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def run_web_mode(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def run_tui_mode(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def show_statistics(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def run(self):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:def parse_args() -> argparse.Namespace:
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:def ensure_dependencies(check_tui: bool = False):
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:def main():
./.claude/worktrees/agent-a9869eb207a425b4a/main.py:    def signal_handler(signum, frame):
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:class ServerMetricsCollector:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./.claude/worktrees/agent-a9869eb207a425b4a/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:class SystemMetricsCollector:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _init_nvml(self) -> bool:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def close(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _get_cpu_power_w(self) -> float:
./.claude/worktrees/agent-a9869eb207a425b4a/system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_init_creates_all_components(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_context_manager(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:class TestConfigDefaults(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_database_path_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_server_url_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_server_metrics_endpoint_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_tracked_processes_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_compression_enabled_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_polling_interval_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_web_http_port_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:class TestConfigSetMethod(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_set_simple_key(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_set_nested_key(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_set_nested_key_creates_intermediate(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_override_existing_value(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:class TestConfigIntegration(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_config.py:    def test_aggregator_config_attributes(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestDatabaseInit(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_connect_creates_connection(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_context_manager(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_schema_version_created(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestServerMetrics(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_insert_server_metrics(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_get_server_metrics_with_filter(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_get_server_metrics_limit(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestSystemMetrics(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_insert_system_metrics(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_get_system_metrics(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestIdleBaseline(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_insert_idle_baseline(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_insert_invalid_idle_baseline(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_update_and_get_cumulative_energy(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_get_cumulative_energy_empty(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestSettings(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_set_and_get_setting(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_get_setting_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_cost_rate_default(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_set_cost_rate(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_insert_process_gpu_metrics(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestDatabaseTables(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_all_tables_created(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_table_row_counts(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestSchemaValidation(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_create_table_columns_match_insert_statements(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:class TestCompression(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_database.py:    def test_compression_with_data(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_imports.py:def test_imports():
./.claude/worktrees/agent-a9869eb207a425b4a/test_llama-monitor.py:def run_tests():
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_make_request_success(self, mock_get):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_get_props(self, mock_make_request):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_collect(self, mock_make_request):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_metrics_dict(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_slots_list(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_slots_dict_single(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_slots_empty_list(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_slots_none(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_format_metrics_display_full(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_format_metrics_display_empty(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_init_default_tracked_processes(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestContextManager(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_enter_returns_self(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_memory_success(self):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:class TestCollect(unittest.TestCase):
./.claude/worktrees/agent-a9869eb207a425b4a/test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:class TUI:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _init_colors(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_header(self, stdscr) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _draw_footer(self, stdscr) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def _main_loop(self, stdscr) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def run(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:    def stop(self) -> None:
./.claude/worktrees/agent-a9869eb207a425b4a/tui.py:def main() -> int:
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def get_aggregator() -> Optional[Aggregator]:
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def get_config() -> Any:
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def index() -> str:
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def api_latest_metrics():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def api_latest_metrics_db():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def api_range_metrics():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def api_metrics_list():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def api_status():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def handle_connect():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def handle_disconnect():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False):
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None):
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:    def run():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def stop_server():
./.claude/worktrees/agent-a9869eb207a425b4a/web_server.py:def main():
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:class Aggregator:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def __init__(
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def compress_if_needed(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def close(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def __enter__(self):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:class Aggregator:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def connect(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def close(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def check_compression(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:        def collection_loop():
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def stop(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def log_message(self, format, *args):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def do_GET(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _handle_status(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:        def do_shutdown():
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def _handle_restart(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:        def do_restart():
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:class WebSocketHandler:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:        def handle_connect(sid):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:        def handle_disconnect(sid):
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./.claude/worktrees/agent-aa69ebbc357249334/aggregator_daemon.py:def main() -> int:
./.claude/worktrees/agent-aa69ebbc357249334/cli_stats.py:def parse_args():
./.claude/worktrees/agent-aa69ebbc357249334/cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./.claude/worktrees/agent-aa69ebbc357249334/cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-aa69ebbc357249334/cli_stats.py:def main():
./.claude/worktrees/agent-aa69ebbc357249334/config.py:class Config:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def _load_config(self, config_path: str) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def get(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def set(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def get_compression_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:    def get_server_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:def find_config(default_path: str = "config.yaml") -> str:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:def load_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:def get_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-aa69ebbc357249334/config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:class Database:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def __init__(self, db_path: str):
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def _ensure_directory(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def connect(self) -> sqlite3.Connection:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def close(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def __enter__(self) -> "Database":
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def lock(self):
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def _initialize_schema(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_server_metrics(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_system_metrics(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_process_gpu_metrics(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_idle_baseline(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_server_metrics_raw(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_system_metrics_raw(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_process_gpu_metrics_raw(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def insert_process_cpu_metrics_raw(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def update_cumulative_energy(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def get_server_metrics(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def get_system_metrics(
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def vacuum(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def get_table_size(self, table: str) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def get_tables(self) -> List[str]:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def set_setting(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def get_cost_rate(self) -> float:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def compress_to_1m(self) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/db.py:    def compress_to_1h(self) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:class ElectricityCostCalculator:
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def __init__(
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def start_session(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def calculate_power_cost(
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def update_power_readings(
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def calculate_idle_baseline(
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def format_cost_display(
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:class IdleBaselineTracker:
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:    def __init__(
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:    def check_idle(
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:    def clear_baseline_data(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/idle_baseline.py:    def reset(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/main.py:class MetricsCache:
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def __init__(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def update(self, metrics: Dict[str, Any]):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def get(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/main.py:class Monitor:
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def __init__(
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def initialize(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def run_aggregator_loop(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def shutdown(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def run_web_mode(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def run_tui_mode(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def show_statistics(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def run(self):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:def parse_args() -> argparse.Namespace:
./.claude/worktrees/agent-aa69ebbc357249334/main.py:def ensure_dependencies(check_tui: bool = False):
./.claude/worktrees/agent-aa69ebbc357249334/main.py:def main():
./.claude/worktrees/agent-aa69ebbc357249334/main.py:    def signal_handler(signum, frame):
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:class ServerMetricsCollector:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./.claude/worktrees/agent-aa69ebbc357249334/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:class SystemMetricsCollector:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _init_nvml(self) -> bool:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def close(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _get_cpu_power_w(self) -> float:
./.claude/worktrees/agent-aa69ebbc357249334/system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_init_creates_all_components(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_context_manager(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:class TestConfigDefaults(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_database_path_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_server_url_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_server_metrics_endpoint_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_tracked_processes_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_compression_enabled_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_polling_interval_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_web_http_port_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:class TestConfigSetMethod(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_set_simple_key(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_set_nested_key(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_set_nested_key_creates_intermediate(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_override_existing_value(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:class TestConfigIntegration(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_config.py:    def test_aggregator_config_attributes(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestDatabaseInit(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_connect_creates_connection(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_context_manager(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_schema_version_created(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestServerMetrics(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_insert_server_metrics(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_get_server_metrics_with_filter(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_get_server_metrics_limit(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestSystemMetrics(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_insert_system_metrics(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_get_system_metrics(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestIdleBaseline(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_insert_idle_baseline(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_insert_invalid_idle_baseline(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_update_and_get_cumulative_energy(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_get_cumulative_energy_empty(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestSettings(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_set_and_get_setting(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_get_setting_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_cost_rate_default(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_set_cost_rate(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_insert_process_gpu_metrics(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestDatabaseTables(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_all_tables_created(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_table_row_counts(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestSchemaValidation(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_create_table_columns_match_insert_statements(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:class TestCompression(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_database.py:    def test_compression_with_data(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_imports.py:def test_imports():
./.claude/worktrees/agent-aa69ebbc357249334/test_llama-monitor.py:def run_tests():
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_make_request_success(self, mock_get):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_get_props(self, mock_make_request):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_collect(self, mock_make_request):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_metrics_dict(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_slots_list(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_slots_dict_single(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_slots_empty_list(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_slots_none(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_format_metrics_display_full(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_format_metrics_display_empty(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_init_default_tracked_processes(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestContextManager(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_enter_returns_self(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_memory_success(self):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:class TestCollect(unittest.TestCase):
./.claude/worktrees/agent-aa69ebbc357249334/test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:class TUI:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _init_colors(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_header(self, stdscr) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _draw_footer(self, stdscr) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def _main_loop(self, stdscr) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def run(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:    def stop(self) -> None:
./.claude/worktrees/agent-aa69ebbc357249334/tui.py:def main() -> int:
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def get_aggregator() -> Optional[Aggregator]:
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def get_config() -> Any:
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def index() -> str:
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def api_latest_metrics():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def api_latest_metrics_db():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def api_range_metrics():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def api_metrics_list():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def api_status():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def handle_connect():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def handle_disconnect():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False):
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None):
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:    def run():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def stop_server():
./.claude/worktrees/agent-aa69ebbc357249334/web_server.py:def main():
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:class Aggregator:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def __init__(
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def compress_if_needed(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def close(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def __enter__(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:class Aggregator:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def connect(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def close(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def check_compression(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:        def collection_loop():
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def stop(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def log_message(self, format, *args):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def do_GET(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _handle_status(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:        def do_shutdown():
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def _handle_restart(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:        def do_restart():
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:class WebSocketHandler:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:        def handle_connect(sid):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:        def handle_disconnect(sid):
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./.claude/worktrees/agent-ab4e3e5a86f632eee/aggregator_daemon.py:def main() -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/cli_stats.py:def parse_args():
./.claude/worktrees/agent-ab4e3e5a86f632eee/cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./.claude/worktrees/agent-ab4e3e5a86f632eee/cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-ab4e3e5a86f632eee/cli_stats.py:def main():
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:class Config:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def _load_config(self, config_path: str) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def get(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def set(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def get_compression_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def get_server_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:    def save(self, config_path: Optional[str] = None) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:def find_config(default_path: str = "config.yaml") -> str:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:def load_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:def get_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-ab4e3e5a86f632eee/config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:class Database:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def __init__(self, db_path: str):
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def _ensure_directory(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def connect(self) -> sqlite3.Connection:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def close(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def __enter__(self) -> "Database":
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def lock(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def _initialize_schema(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_server_metrics(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_system_metrics(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_process_gpu_metrics(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_idle_baseline(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_server_metrics_raw(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_system_metrics_raw(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_process_gpu_metrics_raw(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def insert_process_cpu_metrics_raw(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def update_cumulative_energy(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def get_server_metrics(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def get_system_metrics(
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def vacuum(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def get_table_size(self, table: str) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def get_tables(self) -> List[str]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def set_setting(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def get_cost_rate(self) -> float:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def compress_to_1m(self) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/db.py:    def compress_to_1h(self) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:class ElectricityCostCalculator:
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def __init__(
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def start_session(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def calculate_power_cost(
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def update_power_readings(
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def calculate_idle_baseline(
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def format_cost_display(
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:class IdleBaselineTracker:
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:    def __init__(
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:    def check_idle(
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:    def clear_baseline_data(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/idle_baseline.py:    def reset(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:class MetricsCache:
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def __init__(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def update(self, metrics: Dict[str, Any]):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def get(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:class Monitor:
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def __init__(
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def initialize(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def run_aggregator_loop(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def shutdown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def run_web_mode(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def run_tui_mode(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def show_statistics(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def run(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:def parse_args() -> argparse.Namespace:
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:def ensure_dependencies(check_tui: bool = False):
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:def main():
./.claude/worktrees/agent-ab4e3e5a86f632eee/main.py:    def signal_handler(signum, frame):
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:class ServerMetricsCollector:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./.claude/worktrees/agent-ab4e3e5a86f632eee/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:class SystemMetricsCollector:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _init_nvml(self) -> bool:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def close(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _get_cpu_power_w(self) -> float:
./.claude/worktrees/agent-ab4e3e5a86f632eee/system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_init_creates_all_components(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_context_manager(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:class TestConfigDefaults(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_database_path_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_server_url_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_server_metrics_endpoint_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_tracked_processes_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_compression_enabled_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_polling_interval_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_web_http_port_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:class TestConfigSetMethod(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_set_simple_key(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_set_nested_key(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_set_nested_key_creates_intermediate(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_override_existing_value(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:class TestConfigIntegration(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_config.py:    def test_aggregator_config_attributes(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestDatabaseInit(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_connect_creates_connection(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_context_manager(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_schema_version_created(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestServerMetrics(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_insert_server_metrics(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_get_server_metrics_with_filter(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_get_server_metrics_limit(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestSystemMetrics(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_insert_system_metrics(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_get_system_metrics(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestIdleBaseline(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_insert_idle_baseline(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_insert_invalid_idle_baseline(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_update_and_get_cumulative_energy(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_get_cumulative_energy_empty(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestSettings(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_set_and_get_setting(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_get_setting_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_cost_rate_default(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_set_cost_rate(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_insert_process_gpu_metrics(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestDatabaseTables(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_all_tables_created(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_table_row_counts(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestSchemaValidation(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_create_table_columns_match_insert_statements(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:class TestCompression(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_database.py:    def test_compression_with_data(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_imports.py:def test_imports():
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_llama-monitor.py:def run_tests():
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_make_request_success(self, mock_get):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_get_props(self, mock_make_request):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_collect(self, mock_make_request):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_metrics_dict(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_slots_list(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_slots_dict_single(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_slots_empty_list(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_slots_none(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_format_metrics_display_full(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_format_metrics_display_empty(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_init_default_tracked_processes(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestContextManager(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_enter_returns_self(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_memory_success(self):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:class TestCollect(unittest.TestCase):
./.claude/worktrees/agent-ab4e3e5a86f632eee/test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:class TUI:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _init_colors(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_header(self, stdscr) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _draw_footer(self, stdscr) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def _main_loop(self, stdscr) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def run(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:    def stop(self) -> None:
./.claude/worktrees/agent-ab4e3e5a86f632eee/tui.py:def main() -> int:
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def get_aggregator() -> Optional[Aggregator]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def get_config() -> Any:
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def index() -> str:
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def api_latest_metrics():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def api_latest_metrics_db():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def api_range_metrics():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def api_metrics_list():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def api_status():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def handle_connect():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def handle_disconnect():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False):
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None):
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:    def run():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def stop_server():
./.claude/worktrees/agent-ab4e3e5a86f632eee/web_server.py:def main():
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:class Aggregator:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def __init__(
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def compress_if_needed(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def close(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def __enter__(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:class Aggregator:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def connect(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def close(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def check_compression(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:        def collection_loop():
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def stop(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def log_message(self, format, *args):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def do_GET(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _handle_status(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:        def do_shutdown():
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def _handle_restart(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:        def do_restart():
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:class WebSocketHandler:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def start(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:        def handle_connect(sid):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:        def handle_disconnect(sid):
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./.claude/worktrees/agent-abb8b3cb2c5046275/aggregator_daemon.py:def main() -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/cli_stats.py:def parse_args():
./.claude/worktrees/agent-abb8b3cb2c5046275/cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./.claude/worktrees/agent-abb8b3cb2c5046275/cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-abb8b3cb2c5046275/cli_stats.py:def main():
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:class Config:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def __init__(self, config_path: Optional[str] = None):
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def _load_config(self, config_path: str) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def get(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def set(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def get_compression_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:    def get_server_config(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:def find_config(default_path: str = "config.yaml") -> str:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:def load_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:def get_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-abb8b3cb2c5046275/config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:class Database:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def __init__(self, db_path: str):
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def _ensure_directory(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def connect(self) -> sqlite3.Connection:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def close(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def __enter__(self) -> "Database":
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def lock(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def _initialize_schema(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_server_metrics(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_system_metrics(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_process_gpu_metrics(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_idle_baseline(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_server_metrics_raw(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_system_metrics_raw(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_process_gpu_metrics_raw(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def insert_process_cpu_metrics_raw(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def update_cumulative_energy(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def get_server_metrics(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def get_system_metrics(
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def vacuum(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def get_table_size(self, table: str) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def get_tables(self) -> List[str]:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def set_setting(self, key: str, value: Any) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def get_cost_rate(self) -> float:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def compress_to_1m(self) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/db.py:    def compress_to_1h(self) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:class ElectricityCostCalculator:
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def __init__(
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def start_session(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def calculate_power_cost(
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def update_power_readings(
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def calculate_idle_baseline(
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def format_cost_display(
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:class IdleBaselineTracker:
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:    def __init__(
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:    def check_idle(
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:    def clear_baseline_data(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/idle_baseline.py:    def reset(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:class MetricsCache:
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def __init__(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def update(self, metrics: Dict[str, Any]):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def get(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:class Monitor:
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def __init__(
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def initialize(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def run_aggregator_loop(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def shutdown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def run_web_mode(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def run_tui_mode(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def show_statistics(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def run(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:def parse_args() -> argparse.Namespace:
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:def ensure_dependencies(check_tui: bool = False):
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:def main():
./.claude/worktrees/agent-abb8b3cb2c5046275/main.py:    def signal_handler(signum, frame):
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:class ServerMetricsCollector:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./.claude/worktrees/agent-abb8b3cb2c5046275/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:class SystemMetricsCollector:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _init_nvml(self) -> bool:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def close(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def collect(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _get_cpu_power_w(self) -> float:
./.claude/worktrees/agent-abb8b3cb2c5046275/system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_init_creates_all_components(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_context_manager(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:class TestConfigDefaults(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_database_path_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_server_url_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_server_metrics_endpoint_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_tracked_processes_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_compression_enabled_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_polling_interval_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_web_http_port_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:class TestConfigSetMethod(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_set_simple_key(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_set_nested_key(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_set_nested_key_creates_intermediate(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_override_existing_value(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:class TestConfigIntegration(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_config.py:    def test_aggregator_config_attributes(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestDatabaseInit(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_connect_creates_connection(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_context_manager(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_schema_version_created(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestServerMetrics(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_insert_server_metrics(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_get_server_metrics_with_filter(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_get_server_metrics_limit(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestSystemMetrics(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_insert_system_metrics(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_get_system_metrics(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestIdleBaseline(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_insert_idle_baseline(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_insert_invalid_idle_baseline(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_update_and_get_cumulative_energy(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_get_cumulative_energy_empty(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestSettings(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_set_and_get_setting(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_get_setting_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_cost_rate_default(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_set_cost_rate(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_insert_process_gpu_metrics(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestDatabaseTables(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_all_tables_created(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_table_row_counts(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestSchemaValidation(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_create_table_columns_match_insert_statements(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:class TestCompression(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def tearDown(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_database.py:    def test_compression_with_data(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_imports.py:def test_imports():
./.claude/worktrees/agent-abb8b3cb2c5046275/test_llama-monitor.py:def run_tests():
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_make_request_success(self, mock_get):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_get_props(self, mock_make_request):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_collect(self, mock_make_request):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:        def mock_side_effect(endpoint):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_metrics_dict(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def setUp(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_slots_list(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_slots_dict_single(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_slots_empty_list(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_slots_none(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_format_metrics_display_full(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_format_metrics_display_empty(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_init_default_tracked_processes(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestContextManager(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_enter_returns_self(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_memory_success(self):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:class TestCollect(unittest.TestCase):
./.claude/worktrees/agent-abb8b3cb2c5046275/test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:class TUI:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _init_colors(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_header(self, stdscr) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _draw_footer(self, stdscr) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def _main_loop(self, stdscr) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def run(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:    def stop(self) -> None:
./.claude/worktrees/agent-abb8b3cb2c5046275/tui.py:def main() -> int:
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def get_aggregator() -> Optional[Aggregator]:
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def get_config() -> Any:
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def index() -> str:
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def api_latest_metrics():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def api_latest_metrics_db():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def api_range_metrics():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def api_historical_metrics():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def api_metrics_list():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def api_status():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def handle_connect():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def handle_disconnect():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False):
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None):
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:    def run():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def stop_server():
./.claude/worktrees/agent-abb8b3cb2c5046275/web_server.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/config_loader.py:class Condition:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/config_loader.py:    def from_dict(cls, data: Dict[str, Any]) -> 'Condition':
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/config_loader.py:class Rule:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/config_loader.py:    def from_dict(cls, frontmatter: Dict[str, Any], message: str) -> 'Rule':
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/config_loader.py:def extract_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/config_loader.py:def load_rules(event: Optional[str] = None) -> List[Rule]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/config_loader.py:def load_rule_file(file_path: str) -> Optional[Rule]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:def compile_regex(pattern: str) -> re.Pattern:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:class RuleEngine:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:    def __init__(self):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:    def evaluate_rules(self, rules: List[Rule], input_data: Dict[str, Any]) -> Dict[str, Any]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:    def _rule_matches(self, rule: Rule, input_data: Dict[str, Any]) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:    def _matches_tool(self, matcher: str, tool_name: str) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:    def _check_condition(self, condition: Condition, tool_name: str,
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:    def _extract_field(self, field: str, tool_name: str,
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/core/rule_engine.py:    def _regex_match(self, pattern: str, text: str) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/hooks/posttooluse.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/hooks/pretooluse.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/hooks/stop.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/hookify/hooks/userpromptsubmit.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def save_baseline_sha(session_id, sha):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:    def _save(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def load_baseline_sha(session_id):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:    def _load(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def record_touched_path(session_id, file_path):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:    def _record(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def consume_stop_state(session_id):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:    def _snap(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def restore_unreviewed_stop_state(session_id, paths, baseline_sha):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:    def _restore(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def get_baseline_file_content(session_id, file_path, cwd):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def capture_git_baseline(cwd):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def _reviewed_shas_path(repo_root):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def _load_reviewed_shas(repo_root):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def _append_reviewed_shas(repo_root, shas, vulns_found=0):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def _list_untracked(cwd):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:def compute_v2_review_set(cwd, baseline_sha, head_at_capture, untracked_at_baseline=None):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/diffstate.py:    def _unchanged_since_baseline(p):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _encode_phase(s):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _encode_err_kind(s):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _encode_rc(err_kind):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _is_signal_kill(returncode) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _cooldown_remaining(state_dir) -> float:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _write_cooldown(state_dir) -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _encode_stderr_sig(err_kind):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _encode_exc_kind(err_kind):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _encode_errno(err_kind):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _probe_has_pip() -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _pip_err_from_stderr(stderr_b):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _target_dir(state_dir) -> Path:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _target_sdk_importable(state_dir) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _build_via_target(state_dir) -> tuple[int, str, str]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _sdk_on_syspath() -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _plugin_version_int() -> int:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def main() -> tuple[int, str, str]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/ensure_agent_sdk.py:def _maybe_emit_user_notice(outcome: int, pv: int) -> str | None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def load_for_session(cwd: Optional[str]) -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def guidance_block() -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def user_patterns() -> List[Dict[str, Any]]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _config_paths(cwd: Optional[str], basename: str) -> List[Tuple[str, str]]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _load_guidance(cwd: Optional[str]) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _wrap_guidance(guidance: str) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _load_user_patterns(cwd: Optional[str]) -> List[Dict[str, Any]]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _read_config(path: str) -> Optional[Dict[str, Any]]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _validate_pattern(entry: Any, source: str) -> Optional[Dict[str, Any]]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _glob_match(path: str, include: Tuple[str, ...], exclude: Tuple[str, ...]) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:    def _hit(globs: Tuple[str, ...]) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/extensibility.py:def _has_redos_structure(regex: str) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_rev_parse_head(cwd):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _find_git_index(cwd):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _diff_pathspec(cwd, paths):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _temp_index(cwd, untracked_paths=None):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_toplevel(cwd):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_dir(repo_root):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_rev_list_range(repo_root, base, head="HEAD"):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_diff_range(repo_root, base, head="HEAD"):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _detect_main_branch(repo_root):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_reflog_recent_commits(repo_root, max_age_s=120, max_n=5):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_name_only(cwd, base, include_untracked=False):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:    def _run(env):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _git_status_porcelain(cwd):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _is_ancestor(cwd, maybe_ancestor, descendant):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def get_git_diff(cwd, baseline_sha, full_context=False, paths=None, untracked_paths=None):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _prioritize_diff_files(diff_files, cap):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:    def _score(item):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def _is_reviewable_source(file_path):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def extract_file_paths_from_diff(diff_output):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def parse_diff_into_files(diff_output):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/gitutil.py:def filter_preexisting_from_diff(diff_files, cwd, baseline_sha):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _inject_agent_sdk_venv_into_syspath(state_dir):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _bootstrap_pywin32(site_packages_dir):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _anthropic_base_url() -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _probe_anthropic(timeout: float = 5.0) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _strip_anthropic_from_no_proxy() -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def ensure_anthropic_reachable() -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _cap_files_for_prompt(files):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _build_auth_headers(use_token):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _model_supports_adaptive_thinking(model: str) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _is_3p_provider() -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _call_claude_via_sdk(prompt, output_schema, *, max_tokens=16000, model=None):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _call_claude(prompt, output_schema, thinking_budget=10000, max_tokens=16000, model=None,
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _dual_or_enabled() -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _call_claude_dual_or(prompt, output_schema, *, bool_key: str, list_key: str,
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:    def _leg():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _format_vulns_guidance(vulns: List[Dict[str, Any]]) -> Optional[str]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _format_vulns_summary(vulns: List[Dict[str, Any]],
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:    def _item(v):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:    def _render(items):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _finding_keys(findings: List[Dict[str, Any]]) -> set:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _dedup_against_state(session_id: str, vulns: List[Dict[str, Any]],
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def analyze_code_security(files: List[Tuple[str, str]], is_diff: bool = False, previous_findings: Optional[List[str]] = None) -> Tuple[Optional[str], List[Dict[str, Any]]]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _agentic_commit_review_enabled() -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def _agentic_spawn_env() -> Dict[str, str]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def agentic_review(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:            def _tolerant(data):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:    def _run(system: str, prompt: str, *, schema: Dict[str, Any]
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:        def _scrub(s: object) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:        def _norm(s: str) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:        def _intersects_diff(cand: Dict[str, Any]) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/llm.py:def analyze_security_concerns(files: List[Tuple[str, str]], is_diff: bool = False) -> Optional[str]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/patterns.py:class RuleId(IntEnum):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/patterns.py:def rule_names_to_mask(rule_names):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:def cap_diff_for_prompt(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:def build_investigate_prompt(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:def build_refute_prompt(candidates: list[dict[str, Any]], diff_text: str) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:def tag_diff_anchor(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:    def _norm(s: str) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:    def _intersects(cand: dict[str, Any]) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:def filter_by_severity(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/review_api.py:def format_findings(findings: list[dict[str, Any]]) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def emit_metrics(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def atomic_check_and_mark_warning(session_id, warning_key):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _check(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def atomic_check_counter(session_id, counter_key, max_count):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _check(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def atomic_check_rate_limit(session_id, key, max_per_window, window_s):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _check(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def record_pending_warnings(session_id, file_path, rule_names):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _record(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def sweep_pending_warnings(session_id):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _sweep(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def check_patterns(file_path, content):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def extract_content_from_input(tool_name, tool_input):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def handle_user_prompt_submit(input_data):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _save(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def _resolve_amend_pre_sha(repo_root, expected_post_sha=None):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def _claim_bash_hook_once(input_data):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def is_push_sweep_enabled():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def _compute_push_sweep_base(prev_upstream, push_range, reviewed):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def _push_section(bash_output):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def _detect_prev_upstream(repo_root, bash_output):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def is_commit_review_enabled():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def _agentic_review_with_race(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _agentic() -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _fallback() -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def handle_commit_review_posttooluse(input_data):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _read_previous(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _record_findings(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def handle_push_sweep_posttooluse(input_data):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _record(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def handle_stop_hook(input_data):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:    def _skip(reason, restore=False, **extra):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:        def _record_fire(state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def _maybe_bootstrap_agent_sdk_async():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/security_reminder_hook.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/session_state.py:def _state_key(session_id):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/session_state.py:def get_state_file(session_id):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/session_state.py:def get_lock_file(session_id):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/session_state.py:def cleanup_old_state_files():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/session_state.py:def load_state(session_id):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/session_state.py:def save_state(session_id, state):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/session_state.py:def with_locked_state(session_id, callback):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/_base.py:def state_dir():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/_base.py:def debug_log(message):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/_base.py:def _read_plugin_version_int():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/_base.py:def _record_usage(usage, model, cost_usd=None):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/_base.py:def _record_http_error(status):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/security-guidance/hooks/_base.py:def _usage_metrics():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def get_mime_type(path: Path) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def find_runs(workspace: Path) -> list[dict]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def _find_runs_recursive(root: Path, current: Path, runs: list[dict]) -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def build_run(root: Path, run_dir: Path) -> dict | None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def embed_file(path: Path) -> dict:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def load_previous_iteration(workspace: Path) -> dict[str, dict]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def generate_html(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def _kill_port(port: int) -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:class ReviewHandler(BaseHTTPRequestHandler):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:    def __init__(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:    def do_GET(self) -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:    def do_POST(self) -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:    def log_message(self, format: str, *args: object) -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py:def main() -> None:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py:def calculate_stats(values: list[float]) -> dict:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py:def load_run_results(benchmark_dir: Path) -> dict:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py:def aggregate_results(results: dict) -> dict:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py:def generate_benchmark(benchmark_dir: Path, skill_name: str = "", skill_path: str = "") -> dict:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py:def generate_markdown(benchmark: dict) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/generate_report.py:def generate_html(data: dict, auto_refresh: bool = False, skill_name: str = "") -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/generate_report.py:        def aggregate_runs(results: list[dict]) -> tuple[int, int]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/generate_report.py:        def score_class(correct: int, total: int) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/generate_report.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/improve_description.py:def _call_claude(prompt: str, model: str | None, timeout: int = 300) -> str:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/improve_description.py:def improve_description(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/improve_description.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/package_skill.py:def should_exclude(rel_path: Path) -> bool:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/package_skill.py:def package_skill(skill_path, output_dir=None):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/package_skill.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py:def validate_skill(skill_path):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_eval.py:def find_project_root() -> Path:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_eval.py:def run_single_query(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_eval.py:def run_eval(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_eval.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_loop.py:def split_eval_set(eval_set: list[dict], holdout: float, seed: int = 42) -> tuple[list[dict], list[dict]]:
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_loop.py:def run_loop(
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_loop.py:            def print_eval_stats(label, results, elapsed):
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/run_loop.py:def main():
./.claude-history/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/utils.py:def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
./aggregator.py:class Aggregator:
./aggregator.py:    def __init__(
./aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./aggregator.py:    def compress_if_needed(self) -> None:
./aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./aggregator.py:    def calculate_today_cost(self) -> Dict[str, Any]:
./aggregator.py:    def close(self) -> None:
./aggregator.py:    def __enter__(self):
./aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./aggregator_daemon.py:class Aggregator:
./aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):
./aggregator_daemon.py:    def connect(self) -> None:
./aggregator_daemon.py:    def close(self) -> None:
./aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
./aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
./aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
./aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./aggregator_daemon.py:    def check_compression(self) -> None:
./aggregator_daemon.py:    def _compress_to_minute(self) -> None:
./aggregator_daemon.py:    def _compress_to_hour(self) -> None:
./aggregator_daemon.py:    def start(self) -> None:
./aggregator_daemon.py:        def collection_loop():
./aggregator_daemon.py:    def stop(self) -> None:
./aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):
./aggregator_daemon.py:    def log_message(self, format, *args):
./aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:
./aggregator_daemon.py:    def do_GET(self) -> None:
./aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:
./aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:
./aggregator_daemon.py:    def _handle_metrics_list(self) -> None:
./aggregator_daemon.py:    def _handle_status(self) -> None:
./aggregator_daemon.py:    def _handle_shutdown(self) -> None:
./aggregator_daemon.py:        def do_shutdown():
./aggregator_daemon.py:    def _handle_restart(self) -> None:
./aggregator_daemon.py:        def do_restart():
./aggregator_daemon.py:class WebSocketHandler:
./aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):
./aggregator_daemon.py:    def start(self) -> None:
./aggregator_daemon.py:        def handle_connect(sid):
./aggregator_daemon.py:        def handle_disconnect(sid):
./aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:
./aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:
./aggregator_daemon.py:def main() -> int:
./cli_stats.py:def parse_args():
./cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:
./cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:
./cli_stats.py:def main():
./config.py:class Config:
./config.py:    def __init__(self, config_path: Optional[str] = None):
./config.py:    def _load_config(self, config_path: str) -> None:
./config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
./config.py:    def get(self, key: str, default: Any = None) -> Any:
./config.py:    def set(self, key: str, value: Any) -> None:
./config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:
./config.py:    def get_compression_config(self) -> Dict[str, Any]:
./config.py:    def get_server_config(self) -> Dict[str, Any]:
./config.py:def find_config(default_path: str = "config.yaml") -> str:
./config.py:def load_config(config_path: Optional[str] = None) -> Config:
./config.py:def get_config(config_path: Optional[str] = None) -> Config:
./config.py:def reload_config(config_path: Optional[str] = None) -> Config:
./db.py:class Database:
./db.py:    def __init__(self, db_path: str):
./db.py:    def _ensure_directory(self) -> None:
./db.py:    def connect(self) -> sqlite3.Connection:
./db.py:    def close(self) -> None:
./db.py:    def __enter__(self) -> "Database":
./db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./db.py:    def lock(self):
./db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
./db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
./db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:
./db.py:    def _initialize_schema(self) -> None:
./db.py:    def _migrate_schema(self, cursor: sqlite3.Cursor) -> None:
./db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:
./db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:
./db.py:    def insert_server_metrics(
./db.py:    def insert_system_metrics(
./db.py:    def insert_process_gpu_metrics(
./db.py:    def insert_idle_baseline(
./db.py:    def insert_server_metrics_raw(
./db.py:    def insert_system_metrics_raw(
./db.py:    def insert_process_gpu_metrics_raw(
./db.py:    def insert_process_cpu_metrics_raw(
./db.py:    def update_cumulative_energy(
./db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:
./db.py:    def get_today_energy(self) -> Optional[Dict[str, Any]]:
./db.py:    def update_today_energy(
./db.py:    def update_today_energy_archived(
./db.py:    def get_server_metrics(
./db.py:    def get_system_metrics(
./db.py:    def vacuum(self) -> None:
./db.py:    def get_table_size(self, table: str) -> int:
./db.py:    def get_tables(self) -> List[str]:
./db.py:    def get_setting(self, key: str, default: Any = None) -> Any:
./db.py:    def set_setting(self, key: str, value: Any) -> None:
./db.py:    def get_cost_rate(self) -> float:
./db.py:    def set_cost_rate(self, rate: float) -> None:
./db.py:    def get_today_token_tracking(self) -> Optional[Dict[str, Any]]:
./db.py:    def update_today_token_tracking(
./db.py:    def update_today_token_tracking_archived(
./db.py:    def get_all_token_tracking(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
./db.py:    def get_all_vendor_rates(self) -> List[Dict[str, Any]]:
./db.py:    def get_vendor_rate_by_name(self, vendor_name: str) -> Optional[Dict[str, Any]]:
./db.py:    def add_vendor_rate(self, vendor_name: str, rate_usd_per_token: float, is_local_server: bool = False) -> bool:
./db.py:    def update_vendor_rate(self, vendor_name: str, rate_usd_per_token: Optional[float] = None, is_local_server: Optional[bool] = None) -> bool:
./db.py:    def delete_vendor_rate(self, vendor_name: str) -> bool:
./db.py:    def compress_to_1m(self) -> int:
./db.py:    def compress_to_1h(self) -> int:
./electricity_cost.py:class ElectricityCostCalculator:
./electricity_cost.py:    def __init__(
./electricity_cost.py:    def _load_today_energy(self) -> None:
./electricity_cost.py:    def start_session(self) -> None:
./electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:
./electricity_cost.py:    def calculate_power_cost(
./electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:
./electricity_cost.py:    def update_power_readings(
./electricity_cost.py:    def persist_today_energy(self) -> None:
./electricity_cost.py:    def calculate_idle_baseline(
./electricity_cost.py:    def format_cost_display(
./electricity_cost.py:    def get_today_token_stats(self) -> Optional[Dict[str, Any]]:
./electricity_cost.py:    def update_token_tracking(
./electricity_cost.py:    def calculate_local_server_rate(self) -> float:
./electricity_cost.py:    def get_vendor_comparison(self) -> List[Dict[str, Any]]:
./electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:
./electricity_cost.py:    def get_today_stats(self) -> Optional[Dict[str, Any]]:
./electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:
./idle_baseline.py:class IdleBaselineTracker:
./idle_baseline.py:    def __init__(
./idle_baseline.py:    def check_idle(
./idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./idle_baseline.py:    def clear_baseline_data(self) -> None:
./idle_baseline.py:    def reset(self) -> None:
./main.py:def format_significant_digits(value: float, digits: int = 4) -> str:
./main.py:class MetricsCache:
./main.py:    def __init__(self):
./main.py:    def update(self, metrics: Dict[str, Any]):
./main.py:    def get(self) -> Dict[str, Any]:
./main.py:class Monitor:
./main.py:    def __init__(
./main.py:    def initialize(self):
./main.py:    def run_aggregator_loop(self):
./main.py:    def shutdown(self):
./main.py:    def run_web_mode(self):
./main.py:    def run_tui_mode(self):
./main.py:    def show_statistics(self):
./main.py:    def run(self):
./main.py:def parse_args() -> argparse.Namespace:
./main.py:def ensure_dependencies(check_tui: bool = False):
./main.py:def main():
./main.py:    def signal_handler(signum, frame):
./server_metrics.py:class ServerMetricsCollector:
./server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./server_metrics.py:    def collect(self) -> Dict[str, Any]:
./server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:
./system_metrics.py:class SystemMetricsCollector:
./system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):
./system_metrics.py:    def _init_nvml(self) -> bool:
./system_metrics.py:    def close(self) -> None:
./system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":
./system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
./system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:
./system_metrics.py:    def collect(self) -> Dict[str, Any]:
./system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:
./system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:
./system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:
./system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:
./system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:
./system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:
./system_metrics.py:    def _get_cpu_power_w(self) -> float:
./system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):
./test_aggregator_integration.py:    def setUp(self):
./test_aggregator_integration.py:    def tearDown(self):
./test_aggregator_integration.py:    def test_init_creates_all_components(self):
./test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):
./test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):
./test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):
./test_aggregator_integration.py:    def test_full_integration_with_real_components(self):
./test_aggregator_integration.py:    def test_context_manager(self):
./test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):
./test_aggregator_integration.py:    def setUp(self):
./test_aggregator_integration.py:    def tearDown(self):
./test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):
./test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):
./test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):
./test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):
./test_config.py:class TestConfigDefaults(unittest.TestCase):
./test_config.py:    def setUp(self):
./test_config.py:    def test_database_path_default(self):
./test_config.py:    def test_server_url_default(self):
./test_config.py:    def test_server_metrics_endpoint_default(self):
./test_config.py:    def test_tracked_processes_default(self):
./test_config.py:    def test_compression_enabled_default(self):
./test_config.py:    def test_polling_interval_default(self):
./test_config.py:    def test_web_http_port_default(self):
./test_config.py:class TestConfigSetMethod(unittest.TestCase):
./test_config.py:    def setUp(self):
./test_config.py:    def test_set_simple_key(self):
./test_config.py:    def test_set_nested_key(self):
./test_config.py:    def test_set_nested_key_creates_intermediate(self):
./test_config.py:    def test_override_existing_value(self):
./test_config.py:class TestConfigIntegration(unittest.TestCase):
./test_config.py:    def test_aggregator_config_attributes(self):
./test_database.py:class TestDatabaseInit(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_connect_creates_connection(self):
./test_database.py:    def test_context_manager(self):
./test_database.py:    def test_schema_version_created(self):
./test_database.py:class TestServerMetrics(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_insert_server_metrics(self):
./test_database.py:    def test_get_server_metrics_with_filter(self):
./test_database.py:    def test_get_server_metrics_limit(self):
./test_database.py:class TestSystemMetrics(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_insert_system_metrics(self):
./test_database.py:    def test_get_system_metrics(self):
./test_database.py:class TestIdleBaseline(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_insert_idle_baseline(self):
./test_database.py:    def test_insert_invalid_idle_baseline(self):
./test_database.py:class TestCumulativeEnergy(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_update_and_get_cumulative_energy(self):
./test_database.py:    def test_get_cumulative_energy_empty(self):
./test_database.py:class TestSettings(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_set_and_get_setting(self):
./test_database.py:    def test_get_setting_default(self):
./test_database.py:    def test_cost_rate_default(self):
./test_database.py:    def test_set_cost_rate(self):
./test_database.py:class TestProcessGpuMetrics(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_insert_process_gpu_metrics(self):
./test_database.py:class TestDatabaseTables(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_all_tables_created(self):
./test_database.py:    def test_table_row_counts(self):
./test_database.py:class TestSchemaValidation(unittest.TestCase):
./test_database.py:    def test_create_table_columns_match_insert_statements(self):
./test_database.py:class TestCompression(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_compression_with_data(self):
./test_historical_viewer.py:class TestHistoricalDataAPI(unittest.TestCase):
./test_historical_viewer.py:    def setUp(self):
./test_historical_viewer.py:    def tearDown(self):
./test_historical_viewer.py:    def test_api_historical_metrics_hour(self):
./test_historical_viewer.py:    def test_api_historical_metrics_day(self):
./test_historical_viewer.py:    def test_api_historical_metrics_week(self):
./test_historical_viewer.py:    def test_api_historical_metrics_custom_range(self):
./test_historical_viewer.py:    def test_api_historical_metrics_missing_params(self):
./test_historical_viewer.py:    def test_api_historical_metrics_data_structure(self):
./test_historical_viewer.py:    def test_api_historical_metrics_with_limit(self):
./test_historical_viewer.py:class TestHistoricalDataDatabase(unittest.TestCase):
./test_historical_viewer.py:    def setUp(self):
./test_historical_viewer.py:    def tearDown(self):
./test_historical_viewer.py:    def test_get_system_metrics_with_time_range(self):
./test_historical_viewer.py:    def test_get_server_metrics_with_time_range(self):
./test_historical_viewer.py:class TestHistoricalDataJavaScript(unittest.TestCase):
./test_historical_viewer.py:    def test_timeframe_options(self):
./test_historical_viewer.py:    def test_historical_chart_datasets(self):
./test_imports.py:def test_imports():
./test_llama-monitor.py:def run_tests():
./test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):
./test_server_metrics.py:    def setUp(self):
./test_server_metrics.py:    def test_init_strips_trailing_slash(self):
./test_server_metrics.py:    def test_make_request_success(self, mock_get):
./test_server_metrics.py:    def test_make_request_failure(self, mock_get):
./test_server_metrics.py:    def test_get_metrics(self, mock_make_request):
./test_server_metrics.py:    def test_get_slots(self, mock_make_request):
./test_server_metrics.py:    def test_get_props(self, mock_make_request):
./test_server_metrics.py:    def test_collect(self, mock_make_request):
./test_server_metrics.py:        def mock_side_effect(endpoint):
./test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):
./test_server_metrics.py:        def mock_side_effect(endpoint):
./test_server_metrics.py:class TestParseMetrics(unittest.TestCase):
./test_server_metrics.py:    def setUp(self):
./test_server_metrics.py:    def test_parse_metrics_dict(self):
./test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):
./test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):
./test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):
./test_server_metrics.py:    def test_parse_metrics_empty_string(self):
./test_server_metrics.py:    def test_parse_metrics_empty_dict(self):
./test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./test_server_metrics.py:    def setUp(self):
./test_server_metrics.py:    def test_parse_slots_list(self):
./test_server_metrics.py:    def test_parse_slots_dict_single(self):
./test_server_metrics.py:    def test_parse_slots_empty_list(self):
./test_server_metrics.py:    def test_parse_slots_none(self):
./test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./test_server_metrics.py:    def test_format_metrics_display_full(self):
./test_server_metrics.py:    def test_format_metrics_display_empty(self):
./test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):
./test_system_metrics.py:    def test_init_default_tracked_processes(self):
./test_system_metrics.py:    def test_init_custom_tracked_processes(self):
./test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):
./test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):
./test_system_metrics.py:class TestContextManager(unittest.TestCase):
./test_system_metrics.py:    def test_enter_returns_self(self):
./test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):
./test_system_metrics.py:class TestCollectCPU(unittest.TestCase):
./test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):
./test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):
./test_system_metrics.py:    def test_collect_cpu_process_filtering(self):
./test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):
./test_system_metrics.py:class TestCollectGPU(unittest.TestCase):
./test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):
./test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):
./test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):
./test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):
./test_system_metrics.py:class TestCollectMemory(unittest.TestCase):
./test_system_metrics.py:    def test_collect_memory_success(self):
./test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):
./test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):
./test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):
./test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):
./test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):
./test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):
./test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):
./test_system_metrics.py:class TestCollect(unittest.TestCase):
./test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):
./tui.py:def format_significant_digits(value: float, digits: int = 4) -> str:
./tui.py:class TUI:
./tui.py:    def __init__(self, aggregator_host: str = "localhost", aggregator_port: int = 8080):
./tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:
./tui.py:    def _init_colors(self) -> None:
./tui.py:    def _draw_header(self, stdscr) -> None:
./tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:
./tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:
./tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:
./tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:
./tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:
./tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:
./tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:
./tui.py:    def _draw_footer(self, stdscr) -> None:
./tui.py:    def _main_loop(self, stdscr) -> None:
./tui.py:    def run(self) -> None:
./tui.py:    def stop(self) -> None:
./tui.py:def main() -> int:
./web_server.py:def get_aggregator() -> Optional[Aggregator]:
./web_server.py:def get_config() -> Any:
./web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:
./web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./web_server.py:def index() -> str:
./web_server.py:def api_latest_metrics():
./web_server.py:def api_latest_metrics_db():
./web_server.py:def api_range_metrics():
./web_server.py:def api_metrics_list():
./web_server.py:def api_historical_metrics():
./web_server.py:def api_historical_range():
./web_server.py:def api_status():
./web_server.py:def get_db():
./web_server.py:def settings_page():
./web_server.py:def api_get_settings():
./web_server.py:def api_set_settings():
./web_server.py:def api_reset_settings():
./web_server.py:def api_get_vendor_rates():
./web_server.py:def api_add_vendor_rate():
./web_server.py:def api_update_vendor_rate(vendor_name):
./web_server.py:def api_delete_vendor_rate(vendor_name):
./web_server.py:def api_get_token_accumulator():
./web_server.py:def api_get_vendor_comparison():
./web_server.py:def handle_connect():
./web_server.py:def handle_disconnect():
./web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False, verbose=False):
./web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None, verbose=False):
./web_server.py:    def run():
./web_server.py:def stop_server():
./web_server.py:def main():
