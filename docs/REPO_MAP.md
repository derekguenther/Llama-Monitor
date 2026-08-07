aggregator.py:class Aggregator:  # Orchestrate all metrics collection and storage.
aggregator.py:    def __init__(
aggregator.py:    def _safe_float(self, value, default=-1.0):  # Convert None or non-numeric values to default.
aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:  # Collect all metrics from all sources.
aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:  # Store raw metrics in the database.
aggregator.py:    def compress_if_needed(self) -> None:  # Compress data if needed based on time intervals.
aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:  # Calculate current session cost.
aggregator.py:    def calculate_today_cost(self) -> Dict[str, Any]:  # Calculate today's energy cost (from midnight).
aggregator.py:    def close(self) -> None:  # Clean up resources.
aggregator.py:    def __enter__(self):  # Context manager enter.
aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):  # Context manager exit.
aggregator_daemon.py:class Aggregator:  # Main aggregator class that orchestrates metrics collection and storage.
aggregator_daemon.py:    def __init__(self, config_path: Optional[str] = None):  # Initialize the aggregator.
aggregator_daemon.py:    def connect(self) -> None:  # Open database connection.
aggregator_daemon.py:    def close(self) -> None:  # Close database connection and cleanup.
aggregator_daemon.py:    def collect_all_metrics(self) -> Dict[str, Any]:  # Collect all metrics from all sources.
aggregator_daemon.py:    def _extract_server_metrics(self, server_data: Dict[str, Any]) -> Dict[str, Any]:  # Extract server metrics from collector data.
aggregator_daemon.py:        def safe_float(value, default=-1.0):  # Convert None or non-numeric values to default.
aggregator_daemon.py:    def _extract_system_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:  # Extract system metrics from collector data.
aggregator_daemon.py:        def safe_float(value, default=-1.0):  # Convert None or non-numeric values to default.
aggregator_daemon.py:    def _extract_process_gpu_metrics(self, system_data: Dict[str, Any]) -> Dict[str, Any]:  # Extract per-process GPU metrics.
aggregator_daemon.py:    def _calculate_cost(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:  # Calculate electricity cost from system metrics.
aggregator_daemon.py:        def _clamp(value, minimum=0):  # Clamp a numeric value to minimum, handling non-numeric types gracefully.
aggregator_daemon.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:  # Store raw metrics in database.
aggregator_daemon.py:    def check_compression(self) -> None:  # Check if data compression is needed based on retention rules.
aggregator_daemon.py:    def _compress_to_minute(self) -> None:  # Compress raw data to 1-minute buckets.
aggregator_daemon.py:    def _compress_to_hour(self) -> None:  # Compress 1-minute data to 1-hour buckets.
aggregator_daemon.py:    def start(self) -> None:  # Start the aggregation loop.
aggregator_daemon.py:        def collection_loop():
aggregator_daemon.py:    def stop(self) -> None:  # Stop the aggregation loop and cleanup.
aggregator_daemon.py:class MetricsHandler(BaseHTTPRequestHandler):  # HTTP request handler for the aggregator API.
aggregator_daemon.py:    def log_message(self, format, *args):  # Suppress default logging.
aggregator_daemon.py:    def send_json_response(self, data: Any, status: int = 200) -> None:  # Send JSON response.
aggregator_daemon.py:    def do_GET(self) -> None:  # Handle GET requests.
aggregator_daemon.py:    def _handle_latest_metrics(self) -> None:  # Handle /api/metrics/latest endpoint.
aggregator_daemon.py:    def _handle_range_metrics(self, query: Dict[str, List[str]]) -> None:  # Handle /api/metrics/range endpoint.
aggregator_daemon.py:    def _handle_metrics_list(self) -> None:  # Handle /api/metrics/list endpoint.
aggregator_daemon.py:    def _handle_status(self) -> None:  # Handle /api/status endpoint.
aggregator_daemon.py:    def _handle_shutdown(self) -> None:  # Handle /api/shutdown endpoint.
aggregator_daemon.py:        def do_shutdown():
aggregator_daemon.py:    def _handle_restart(self) -> None:  # Handle /api/restart endpoint.
aggregator_daemon.py:        def do_restart():
aggregator_daemon.py:class WebSocketHandler:  # WebSocket handler for real-time client updates.
aggregator_daemon.py:    def __init__(self, aggregator: Aggregator):  # Initialize WebSocket handler.
aggregator_daemon.py:    def start(self) -> None:  # Start WebSocket server.
aggregator_daemon.py:        def handle_connect(sid):
aggregator_daemon.py:        def handle_disconnect(sid):
aggregator_daemon.py:    def broadcast_metrics(self, metrics: Dict[str, Any]) -> None:  # Broadcast metrics to all connected clients.
aggregator_daemon.py:def create_app(aggregator: Aggregator) -> HTTPServer:  # Create the HTTP server application.
aggregator_daemon.py:def main() -> int:  # Main entry point for the aggregator daemon.
check_db.py:db = Database('llama_monitor.db')
cli_stats.py:def parse_args():  # Parse command line arguments.
cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:  # Fetch latest metrics from aggregator daemon.
cli_stats.py:def _value_or_zero(val, sentinel=-1.0):  # Return val if not None and not sentinel, else 0.
cli_stats.py:def format_stats(metrics: Dict[str, Any], verbose: bool = False) -> str:  # Format stats for display.
cli_stats.py:def format_stats_json(metrics: Dict[str, Any]) -> str:  # Format stats as JSON.
cli_stats.py:def main():  # Main entry point.
config.py:class Config:  # Configuration manager for llama-monitor.
config.py:    def __init__(self, config_path: Optional[str] = None):  # Initialize configuration.
config.py:    def _load_config(self, config_path: str) -> None:  # Load configuration from YAML file.
config.py:    def _deep_merge(self, base: Dict, update: Dict) -> Dict:  # Deep merge update into base dict.
config.py:    def get(self, key: str, default: Any = None) -> Any:  # Get configuration value by dot-notation key.
config.py:    def set(self, key: str, value: Any) -> None:  # Set a configuration value by dot-notation key.
config.py:    def get_idle_baseline_config(self) -> Dict[str, Any]:  # Get idle baseline configuration.
config.py:    def get_compression_config(self) -> Dict[str, Any]:  # Get compression configuration.
config.py:    def get_server_config(self) -> Dict[str, Any]:  # Get server configuration.
config.py:def find_config(default_path: str = "config.yaml") -> str:  # Find configuration file.
config.py:def load_config(config_path: Optional[str] = None) -> Config:  # Load configuration from file.
config.py:def get_config(config_path: Optional[str] = None) -> Config:  # Get or create global config instance.
config.py:def reload_config(config_path: Optional[str] = None) -> Config:  # Reload configuration from file.
db.py:class Database:  # Manages SQLite database for llama-monitor.
db.py:    def __init__(self, db_path: str):  # Initialize database connection.
db.py:    def _ensure_directory(self) -> None:  # Ensure database directory exists.
db.py:    def connect(self) -> sqlite3.Connection:  # Open database connection if not already open.
db.py:    def close(self) -> None:  # Close database connection.
db.py:    def __enter__(self) -> "Database":  # Context manager entry.
db.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # Context manager exit.
db.py:    def lock(self):  # Context manager for acquiring database lock.
db.py:    def execute(self, sql: str, params: Optional[tuple] = None) -> sqlite3.Cursor:  # Execute a SQL statement with the lock.
db.py:    def execute_query(self, sql: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:  # Execute a SELECT query with the lock.
db.py:    def execute_all(self, sql: str, params: Optional[tuple] = None) -> list:  # Execute a SELECT query and return all results with the lock.
db.py:    def _initialize_schema(self) -> None:  # Initialize database schema if not already initialized.
db.py:    def _migrate_schema(self, cursor: sqlite3.Cursor) -> None:  # Check for and add missing tables (schema migrations).
db.py:    def _create_server_metrics_tables(self, cursor: sqlite3.Cursor) -> None:  # Create server metrics tables.
db.py:    def _create_system_metrics_tables(self, cursor: sqlite3.Cursor) -> None:  # Create system metrics tables.
db.py:    def _create_process_gpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:  # Create per-process GPU metrics tables.
db.py:    def _create_process_cpu_metrics_tables(self, cursor: sqlite3.Cursor) -> None:  # Create per-process CPU metrics tables (from Public Documents schema).
db.py:    def _create_auxiliary_tables(self, cursor: sqlite3.Cursor) -> None:  # Create auxiliary tables.
db.py:    def insert_server_metrics(
db.py:    def insert_system_metrics(
db.py:    def insert_process_gpu_metrics(
db.py:    def insert_idle_baseline(
db.py:    def insert_server_metrics_raw(
db.py:    def insert_system_metrics_raw(
db.py:    def insert_process_gpu_metrics_raw(
db.py:    def insert_process_cpu_metrics_raw(
db.py:    def update_cumulative_energy(
db.py:    def get_cumulative_energy(self) -> Optional[Dict[str, Any]]:  # Get current cumulative energy values.
db.py:    def get_today_energy(self) -> Optional[Dict[str, Any]]:  # Get today's energy consumption from midnight.
db.py:    def get_monthly_energy(self, days: int = 30) -> List[Dict[str, Any]]:  # Get energy consumption for the last N days.
db.py:    def update_today_energy(
db.py:    def update_today_energy_archived(
db.py:    def get_server_metrics(
db.py:    def get_system_metrics(
db.py:    def vacuum(self) -> None:  # Run VACUUM to reclaim space.
db.py:    def get_table_size(self, table: str) -> int:  # Get row count for a table.
db.py:    def get_tables(self) -> List[str]:  # Get list of all user tables.
db.py:    def get_setting(self, key: str, default: Any = None) -> Any:  # Get a setting value.
db.py:    def set_setting(self, key: str, value: Any) -> None:  # Set a setting value.
db.py:    def get_cost_rate(self) -> float:  # Get the cost rate from settings.
db.py:    def set_cost_rate(self, rate: float) -> None:  # Set the cost rate in settings.
db.py:    def get_today_token_tracking(self) -> Optional[Dict[str, Any]]:  # Get today's token tracking from midnight.
db.py:    def update_today_token_tracking(
db.py:    def update_today_token_tracking_archived(
db.py:    def get_all_token_tracking(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:  # Get all token tracking data.
db.py:    def get_all_vendor_rates(self) -> List[Dict[str, Any]]:  # Get all vendor rates.
db.py:    def get_vendor_rate_by_name(self, vendor_name: str) -> Optional[Dict[str, Any]]:  # Get a specific vendor rate by name.
db.py:    def add_vendor_rate(self, vendor_name: str, rate_usd_per_token: float, is_local_server: bool = False) -> bool:  # Add a new vendor rate.
db.py:    def update_vendor_rate(self, vendor_name: str, rate_usd_per_token: Optional[float] = None, is_local_server: Optional[bool] = None) -> bool:  # Update an existing vendor rate.
db.py:    def delete_vendor_rate(self, vendor_name: str) -> bool:  # Delete a vendor rate.
db.py:    def compress_to_1m(self) -> int:  # Compress raw metrics to 1-minute buckets.
db.py:    def compress_to_1h(self) -> int:  # Compress 1-minute metrics to 1-hour buckets.
electricity_cost.py:class ElectricityCostCalculator:  # Calculates electricity cost based on power consumption.
electricity_cost.py:    def __init__(
electricity_cost.py:    def _load_cumulative_energy(self) -> None:  # Load cumulative energy from database if available.
electricity_cost.py:    def _load_today_energy(self) -> None:  # Load today's energy from database if available.
electricity_cost.py:    def start_session(self) -> None:  # Start a new energy tracking session.
electricity_cost.py:    def stop_session(self) -> Dict[str, Any]:  # Stop current session and return final stats.
electricity_cost.py:    def calculate_power_cost(
electricity_cost.py:    def calculate_cost(self, energy_wh: float) -> float:  # Calculate cost for energy consumption.
electricity_cost.py:    def update_power_readings(
electricity_cost.py:    def persist_today_energy(self) -> None:  # Persist today's energy to database.
electricity_cost.py:    def calculate_idle_baseline(
electricity_cost.py:    def format_cost_display(
electricity_cost.py:    def get_today_token_stats(self) -> Optional[Dict[str, Any]]:  # Get today's token tracking statistics.
electricity_cost.py:    def update_token_tracking(
electricity_cost.py:    def calculate_local_server_rate(self) -> float:  # Calculate local server rate based on electricity cost and tokens.
electricity_cost.py:    def get_vendor_comparison(self) -> List[Dict[str, Any]]:  # Get vendor comparison data.
electricity_cost.py:    def get_session_stats(self) -> Optional[Dict[str, Any]]:  # Get current session statistics.
electricity_cost.py:    def get_today_stats(self) -> Optional[Dict[str, Any]]:  # Get today's energy statistics.
electricity_cost.py:    def set_cost_rate(self, rate: float) -> None:  # Update the cost rate in the database.
electricity_cost.py:    def clear_session_energy(self) -> Dict[str, Any]:  # Clear all session energy counters and reset to zero.
idle_baseline.py:class IdleBaselineTracker:  # Track idle baseline power consumption.
idle_baseline.py:    def __init__(
idle_baseline.py:    def check_idle(
idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:  # Store baseline reading in database.
idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:  # Get the average of all stored baseline readings.
idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:  # Get average of most recent baseline readings.
idle_baseline.py:    def clear_baseline_data(self) -> None:  # Clear all baseline data from the database.
idle_baseline.py:    def reset(self) -> None:  # Reset tracker state without clearing database.
lancedb_mcp_server.py:EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
lancedb_mcp_server.py:embedding_model = SentenceTransformer(EMBEDDING_MODEL)
lancedb_mcp_server.py:EMBEDDING_DIMENSIONS = 384  # all-MiniLM-L6-v2 produces 384-dimensional embeddings
lancedb_mcp_server.py:DB_PATH = "/sandbox/.lancedb"
lancedb_mcp_server.py:TABLE_NAME = "project_memory"
lancedb_mcp_server.py:class MemoryItem(BaseModel):  # Schema for a memory item in LanceDB.
lancedb_mcp_server.py:mcp = FastMCP("lancedb-memory-server")
lancedb_mcp_server.py:def save_memory(content: str, tags: List[str] = None) -> str:  # Save a memory item to the LanceDB vector database.
lancedb_mcp_server.py:def search_memory(query: str, n_results: int = 5) -> List[dict]:  # Search memories by semantic similarity.
lancedb_mcp_server.py:def get_unique_tags() -> List[str]:  # Get all unique tags used in the memory database.
llamamonitor.py:def format_significant_digits(value: float, digits: int = 4) -> str:  # Format a value with the specified number of significant digits.
llamamonitor.py:class MetricsCache:  # Thread-safe cache for metrics shared between aggregator and UI.
llamamonitor.py:    def __init__(self):
llamamonitor.py:    def update(self, metrics: Dict[str, Any]):  # Update metrics from aggregator.
llamamonitor.py:    def get(self) -> Dict[str, Any]:  # Get latest metrics.
llamamonitor.py:class Monitor:  # Main monitor orchestrator.
llamamonitor.py:    def __init__(
llamamonitor.py:    def initialize(self):  # Initialize the monitor components.
llamamonitor.py:    def run_aggregator_loop(self):  # Background thread to run the aggregator collection loop.
llamamonitor.py:    def shutdown(self):  # Gracefully shutdown the monitor.
llamamonitor.py:    def run_web_mode(self):  # Run in web server mode.
llamamonitor.py:    def run_tui_mode(self):  # Run in TUI mode.
llamamonitor.py:    def show_statistics(self):  # Show system statistics and exit.
llamamonitor.py:    def run(self):  # Run the monitor in the specified mode(s).
llamamonitor.py:def parse_args() -> argparse.Namespace:  # Parse command line arguments.
llamamonitor.py:def ensure_dependencies(check_tui: bool = False):  # Check for and install missing dependencies from requirements.txt.
llamamonitor.py:def main():  # Main entry point.
llamamonitor.py:    def signal_handler(signum, frame):
server_metrics.py:class ServerMetricsCollector:  # Collects metrics from llama.cpp server endpoints.
server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):  # Initialize the collector.
server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:  # Make HTTP request to server endpoint.
server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:  # Fetch metrics from /metrics endpoint.
server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:  # Fetch slot information from /slots endpoint.
server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:  # Fetch server properties from /props endpoint.
server_metrics.py:    def collect(self) -> Dict[str, Any]:  # Collect all server metrics.
server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:  # Parse Prometheus-format metrics.
server_metrics.py:    def _parse_slots(self, slots: Any) -> list:  # Parse slot data.
server_metrics.py:                    def _v(key, default=0):
server_metrics.py:    def _compute_instant_rates(self, server: Dict[str, Any]) -> None:  # Calculate instantaneous token rates from cumulative delta.
server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:  # Format metrics for display.
system_metrics.py:class SystemMetricsCollector:  # Collects system metrics (CPU, GPU, memory) on Windows and Linux.
system_metrics.py:    def __init__(self, tracked_processes: Optional[List[str]] = None):  # Initialize the collector.
system_metrics.py:    def _init_nvml(self) -> bool:  # Initialize NVML library.
system_metrics.py:    def close(self) -> None:  # Cleanup resources.
system_metrics.py:    def __enter__(self) -> "SystemMetricsCollector":  # Context manager entry.
system_metrics.py:    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # Context manager exit.
system_metrics.py:    def _collect_process_ram(self) -> Dict[str, Any]:  # Collect per-process RAM usage for tracked processes.
system_metrics.py:    def collect(self) -> Dict[str, Any]:  # Collect all system metrics.
system_metrics.py:    def _collect_cpu(self) -> Dict[str, Any]:  # Collect CPU metrics.
system_metrics.py:    def _collect_gpu(self) -> Dict[str, Any]:  # Collect GPU metrics.
system_metrics.py:    def _collect_gpu_nvml(self) -> Dict[str, Any]:  # Collect GPU metrics using NVML.
system_metrics.py:    def _collect_gpu_wmi(self) -> Dict[str, Any]:  # Collect GPU metrics using WMI.
system_metrics.py:    def _collect_memory(self) -> Dict[str, Any]:  # Collect memory metrics.
system_metrics.py:    def _collect_process_gpu(self) -> Dict[str, Any]:  # Collect per-process GPU utilization.
system_metrics.py:    def _get_cpu_power_w(self) -> float:  # Get CPU package power from Energy Meter performance counter.
system_metrics.py:    def _get_linux_cpu_power_w(self) -> float:  # Get CPU package power from RAPL on Linux.
system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:  # Collect system power consumption.
test_active_slots_fix.py:class TestActiveSlotsDisplay(unittest.TestCase):  # Tests for Active Slots display functionality.
test_active_slots_fix.py:    def test_format_metrics_display_with_slots(self):  # Test that format_metrics_display correctly shows active slots.
test_active_slots_fix.py:    def test_format_metrics_display_empty_slots(self):  # Test that empty slots list doesn't show active slots line.
test_active_slots_fix.py:    def test_format_metrics_display_no_slots_key(self):  # Test that missing slots key doesn't cause issues.
test_active_slots_fix.py:    def test_format_metrics_display_single_active_slot(self):  # Test with a single active slot.
test_active_slots_fix.py:    def test_format_metrics_display_all_idle(self):  # Test with all slots idle.
test_active_slots_fix.py:class TestSlotsDataFlow(unittest.TestCase):  # Tests for slots data flow through the system.
test_active_slots_fix.py:    def test_collector_collects_slots(self, mock_get):  # Test that ServerMetricsCollector collects slots data.
test_active_slots_fix.py:    def test_parse_slots_list(self, mock_make_request):  # Test parsing slots from list format.
test_active_slots_fix.py:    def test_parse_slots_none_returns_empty(self, mock_make_request):  # Test that None slots returns empty list.
test_active_slots_fix.py:        def side_effect(endpoint):
test_active_slots_fix.py:    def test_aggregator_daemon_slots_extraction(self):  # Test that aggregator daemon correctly extracts slots.
test_active_slots_fix.py:class TestWebServerSlotsUpdate(unittest.TestCase):  # Tests for web server slots display update.
test_active_slots_fix.py:    def test_html_has_active_slots_element(self):  # Test that the HTML contains the server-active-slots element.
test_active_slots_fix.py:    def test_javascript_updates_active_slots(self):  # Test that JavaScript code updates the active slots element.
test_active_slots_fix.py:    def test_javascript_has_slots_filter_logic(self):  # Test that JavaScript has the slots filtering logic.
test_active_slots_fix.py:    def test_javascript_has_slots_reduce_logic(self):  # Test that JavaScript has the slots progress reduction logic.
test_active_slots_fix.py:class TestRequestsProcessingDisplay(unittest.TestCase):  # Tests for Requests Processing display functionality.
test_active_slots_fix.py:    def test_html_has_server_processing_element(self):  # Test that the HTML contains the server-processing element.
test_active_slots_fix.py:    def test_javascript_updates_server_processing(self):  # Test that JavaScript code updates the server-processing element.
test_aggregator.py:agg = Aggregator(
test_aggregator_integration.py:class TestAggregatorIntegration(unittest.TestCase):  # Integration tests for Aggregator.
test_aggregator_integration.py:    def setUp(self):  # Create a temporary database for testing.
test_aggregator_integration.py:    def tearDown(self):  # Clean up temporary database.
test_aggregator_integration.py:    def test_init_creates_all_components(self):  # Test that Aggregator initializes all components correctly.
test_aggregator_integration.py:    def test_init_with_metrics_disabled(self):  # Test that Aggregator works with metrics collection disabled.
test_aggregator_integration.py:    def test_collect_all_metrics_integration(self):  # Test that collect_all_metrics integrates with real collectors.
test_aggregator_integration.py:    def test_store_raw_metrics_integration(self):  # Test that store_raw_metrics stores data to database.
test_aggregator_integration.py:    def test_full_integration_with_real_components(self):  # Test full integration with real components (no mocks).
test_aggregator_integration.py:    def test_context_manager(self):  # Test that Aggregator works as a context manager.
test_aggregator_integration.py:class TestAggregatorWithDatabase(unittest.TestCase):  # Tests for Aggregator database integration.
test_aggregator_integration.py:    def setUp(self):  # Create a temporary database for testing.
test_aggregator_integration.py:    def tearDown(self):  # Clean up temporary database.
test_aggregator_integration.py:    def test_aggregator_creates_database_schema(self):  # Test that Aggregator creates the database schema.
test_aggregator_integration.py:class TestDependencyChecking(unittest.TestCase):  # Tests for dependency checking functionality.
test_aggregator_integration.py:    def test_ensure_dependencies_no_missing(self):  # Test ensure_dependencies when all deps are installed.
test_aggregator_integration.py:    def test_ensure_dependencies_with_tui_flag(self):  # Test ensure_dependencies with check_tui=True.
test_api_data_integrity.py:def fetch_metrics(base_url):  # Fetch metrics from the API.
test_api_data_integrity.py:def find_negative_one_values(data, path=""):  # Recursively find all -1 values in nested dict.
test_api_data_integrity.py:def is_expected_sentinel(path):  # Check if -1 value is an expected sentinel (not a bug).
test_api_data_integrity.py:def main():
test_bar_labels.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_bar_labels.py:def test_bar_labels_and_k_unit():  # Verify bar labels plugin and k-unit formatting are present.
test_config.py:class TestConfigDefaults(unittest.TestCase):  # Tests for default configuration values.
test_config.py:    def setUp(self):  # Create a fresh config instance.
test_config.py:    def test_database_path_default(self):  # Test default database path.
test_config.py:    def test_server_url_default(self):  # Test default server URL.
test_config.py:    def test_server_metrics_endpoint_default(self):  # Test default server metrics endpoint.
test_config.py:    def test_tracked_processes_default(self):  # Test default tracked processes.
test_config.py:    def test_compression_enabled_default(self):  # Test default compression enabled setting.
test_config.py:    def test_polling_interval_default(self):  # Test default polling interval.
test_config.py:    def test_web_http_port_default(self):  # Test default web HTTP port.
test_config.py:class TestConfigSetMethod(unittest.TestCase):  # Tests for the Config.set() method.
test_config.py:    def setUp(self):  # Create a fresh config instance.
test_config.py:    def test_set_simple_key(self):  # Test setting a simple key.
test_config.py:    def test_set_nested_key(self):  # Test setting a nested key with dot notation.
test_config.py:    def test_set_nested_key_creates_intermediate(self):  # Test that setting a nested key creates intermediate dicts.
test_config.py:    def test_override_existing_value(self):  # Test overriding an existing value.
test_config.py:class TestConfigIntegration(unittest.TestCase):  # Integration tests for config with aggregator_daemon.
test_config.py:    def test_aggregator_config_attributes(self):  # Test that Aggregator can access all required config attributes.
test_context_limit_path.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_context_limit_path.py:def test_context_limit_data_path():  # Verify the context limit is read from data.props, not data.server.props.
test_crosshair.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_crosshair.py:def test_crosshair_implementation():  # Verify crosshair plugin is implemented for the CPU/GPU graph.
test_daily_cost_naming.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_daily_cost_naming.py:def test_daily_cost_naming():  # Verify Daily Cost card is present and Monthly Cost is not.
test_dashboard_mapping.py:DOM_MAP = {
test_dashboard_mapping.py:def get_nested_value(data, path):  # Get a value from nested dict using dot-notation path.
test_dashboard_mapping.py:def transform_value(value, transform, data=None):  # Apply a transform to a value.
test_dashboard_mapping.py:    def safe_value(v):  # Convert None to 0, preserve -1 sentinel.
test_dashboard_mapping.py:def fetch_metrics(base_url):  # Fetch metrics from the API.
test_dashboard_mapping.py:def main():
test_dashboard_transforms.py:class TestDataTransformation(unittest.TestCase):
test_dashboard_transforms.py:    def test_transform_width(self):  # Test width transform converts number to percentage string.
test_dashboard_transforms.py:    def test_transform_count_active(self):  # Test count_active transform counts processing slots.
test_dashboard_transforms.py:    def test_transform_count_active_empty(self):  # Test count_active with no slots.
test_dashboard_transforms.py:    def test_transform_mem_text(self):  # Test mem_text transform formats memory as used/total MB.
test_dashboard_transforms.py:    def test_transform_mem_text_cpu_fallback(self):  # Test mem_text falls back to system.memory paths.
test_dashboard_transforms.py:    def test_transform_mem_bar(self):  # Test mem_bar transform calculates memory percentage.
test_dashboard_transforms.py:    def test_transform_mem_bar_zero_total(self):  # Test mem_bar handles zero total memory.
test_dashboard_transforms.py:    def test_transform_mem_bar_cpu_fallback(self):  # Test mem_bar falls back to system.memory paths.
test_dashboard_transforms.py:    def test_transform_sum_power(self):  # Test sum transform adds GPU and CPU power.
test_dashboard_transforms.py:    def test_transform_sum_with_null(self):  # Test sum transform handles null values.
test_dashboard_transforms.py:    def test_transform_sum_with_minus_one(self):  # Test sum transform handles -1 sentinel values (should add them).
test_dashboard_transforms.py:    def test_transform_noop(self):  # Test that None transform returns value unchanged.
test_dashboard_transforms.py:    def test_get_nested_value_simple(self):  # Test simple nested value retrieval.
test_dashboard_transforms.py:    def test_get_nested_value_missing(self):  # Test missing nested value returns None.
test_dashboard_transforms.py:    def test_get_nested_value_null(self):  # Test null value returns None.
test_dashboard_transforms.py:class TestNegativeOneDetection(unittest.TestCase):  # Test that -1 values are properly detected in data.
test_dashboard_transforms.py:    def test_find_negative_one_in_dict(self):  # Test -1 detection in dictionary.
test_dashboard_transforms.py:    def test_find_negative_one_in_list(self):  # Test -1 detection in list.
test_dashboard_transforms.py:    def test_find_negative_one_nested(self):  # Test -1 detection in deeply nested structure.
test_dashboard_transforms.py:    def test_no_negative_one(self):  # Test that valid data passes.
test_database.py:class TestDatabaseInit(unittest.TestCase):  # Tests for database initialization.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_connect_creates_connection(self):  # Test that connect() creates a valid connection.
test_database.py:    def test_context_manager(self):  # Test database context manager.
test_database.py:    def test_schema_version_created(self):  # Test that schema version table is created.
test_database.py:class TestServerMetrics(unittest.TestCase):  # Tests for server metrics operations.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_insert_server_metrics(self):  # Test inserting server metrics.
test_database.py:    def test_get_server_metrics_with_filter(self):  # Test filtering server metrics by time.
test_database.py:    def test_get_server_metrics_limit(self):  # Test limiting server metrics results.
test_database.py:class TestSystemMetrics(unittest.TestCase):  # Tests for system metrics operations.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_insert_system_metrics(self):  # Test inserting system metrics.
test_database.py:    def test_get_system_metrics(self):  # Test retrieving system metrics.
test_database.py:class TestIdleBaseline(unittest.TestCase):  # Tests for idle baseline operations.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_insert_idle_baseline(self):  # Test inserting idle baseline measurement.
test_database.py:    def test_insert_invalid_idle_baseline(self):  # Test inserting invalid idle baseline.
test_database.py:class TestCumulativeEnergy(unittest.TestCase):  # Tests for cumulative energy operations.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_update_and_get_cumulative_energy(self):  # Test updating and retrieving cumulative energy.
test_database.py:    def test_get_cumulative_energy_empty(self):  # Test getting cumulative energy when not initialized.
test_database.py:class TestSettings(unittest.TestCase):  # Tests for settings operations.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_set_and_get_setting(self):  # Test setting and getting a setting value.
test_database.py:    def test_get_setting_default(self):  # Test getting a non-existent setting with default.
test_database.py:    def test_cost_rate_default(self):  # Test default cost rate.
test_database.py:    def test_set_cost_rate(self):  # Test setting cost rate.
test_database.py:class TestProcessGpuMetrics(unittest.TestCase):  # Tests for per-process GPU metrics operations.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_insert_process_gpu_metrics(self):  # Test inserting per-process GPU metrics.
test_database.py:class TestDatabaseTables(unittest.TestCase):  # Tests for database table structure.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_all_tables_created(self):  # Test that all expected tables are created.
test_database.py:    def test_table_row_counts(self):  # Test row counts for empty tables.
test_database.py:class TestSchemaValidation(unittest.TestCase):  # Tests to validate database schema matches code definitions.
test_database.py:    def test_create_table_columns_match_insert_statements(self):  # Validate that INSERT statements use correct column names from CREATE TABLE.
test_database.py:class TestCompression(unittest.TestCase):  # Tests for metric compression functionality.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_compression_with_data(self):  # Test compression by inserting data and verifying it gets compressed.
test_database.py:class TestMonthlyEnergy(unittest.TestCase):  # Tests for monthly energy tracking and cost calculation.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_get_monthly_energy_empty_database(self):  # Test getting monthly energy when database has no data.
test_database.py:    def test_get_monthly_energy_with_data(self):  # Test getting monthly energy with historical data.
test_database.py:    def test_get_monthly_energy_cost_rate(self):  # Test cost rate retrieval from database.
test_database.py:    def test_get_monthly_energy_with_cost_calculation(self):  # Test monthly energy data with cost calculations.
test_database.py:    def test_get_monthly_energy_different_day_counts(self):  # Test get_monthly_energy with different day counts.
test_database.py:    def test_get_monthly_energy_partial_data(self):  # Test get_monthly_energy when some days are missing.
test_database.py:    def test_get_monthly_energy_data_values(self):  # Test that get_monthly_energy returns correct data values.
test_database.py:class TestApiMonthlyCost(unittest.TestCase):  # Tests for the /api/metrics/monthly-cost endpoint.
test_database.py:    def setUp(self):  # Create a temporary database for testing.
test_database.py:    def tearDown(self):  # Clean up temporary database.
test_database.py:    def test_api_monthly_cost_with_data(self):  # Test API returns correct cost data when database has energy data.
test_database.py:    def test_api_monthly_cost_empty_database(self):  # Test API returns empty data when database has no energy data.
test_database.py:    def test_api_monthly_cost_date_format(self):  # Test that API returns dates in correct format.
test_database.py:    def test_api_monthly_cost_error_handling(self):  # Test API error handling for invalid database path.
test_database.py:class TestJavaScriptDateFormatting(unittest.TestCase):  # Tests for JavaScript date formatting logic (MM/dd/yyyy).
test_database.py:    def test_date_formatting_logic(self):  # Test the date formatting algorithm used in JavaScript.
test_database.py:        def format_date_js(date_str):  # Format date as MM/dd/yyyy following JavaScript logic.
test_database.py:    def test_date_padding_logic(self):  # Test that day/month padding works correctly.
test_database.py:        def format_date_with_padding(date_str):  # Format date with proper padding like JavaScript.
test_dollar_sign.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_dollar_sign.py:def test_dollar_sign_placement():  # Verify dollar sign is on Monthly Cost chart, not Tokens/s chart.
test_header_link.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_header_link.py:def test_no_server_link():  # Verify the server URL is not rendered as a clickable link in the header.
test_historical_viewer.py:class TestHistoricalDataAPI(unittest.TestCase):  # Tests for historical data API endpoints.
test_historical_viewer.py:    def setUp(self):  # Create a temporary database for testing.
test_historical_viewer.py:    def tearDown(self):  # Clean up temporary database.
test_historical_viewer.py:    def test_api_historical_metrics_hour(self):  # Test historical data API with hour timeframe.
test_historical_viewer.py:    def test_api_historical_metrics_day(self):  # Test historical data API with day timeframe.
test_historical_viewer.py:    def test_api_historical_metrics_week(self):  # Test historical data API with week timeframe.
test_historical_viewer.py:    def test_api_historical_metrics_custom_range(self):  # Test historical data API with custom range.
test_historical_viewer.py:    def test_api_historical_metrics_missing_params(self):  # Test historical data API with missing required parameters.
test_historical_viewer.py:    def test_api_historical_metrics_data_structure(self):  # Test that historical data has correct structure.
test_historical_viewer.py:    def test_api_historical_metrics_with_limit(self):  # Test historical data API with limit parameter.
test_historical_viewer.py:class TestHistoricalDataDatabase(unittest.TestCase):  # Tests for historical data database queries.
test_historical_viewer.py:    def setUp(self):  # Create a temporary database for testing.
test_historical_viewer.py:    def tearDown(self):  # Clean up temporary database.
test_historical_viewer.py:    def test_get_system_metrics_with_time_range(self):  # Test getting system metrics within a time range.
test_historical_viewer.py:    def test_get_server_metrics_with_time_range(self):  # Test getting server metrics within a time range.
test_historical_viewer.py:class TestHistoricalDataJavaScript(unittest.TestCase):  # Tests for historical data JavaScript functionality.
test_historical_viewer.py:    def test_timeframe_options(self):  # Test that all timeframe options are available.
test_historical_viewer.py:    def test_historical_chart_datasets(self):  # Test that historical charts have correct datasets.
test_imports.py:def test_imports():  # Test all module imports.
test_k_format.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_k_format.py:def test_k_format_on_context_chart():  # Verify k-unit formatting is applied to Context Used chart.
test_llama-monitor.py:TEST_FILES = [
test_llama-monitor.py:LLAMA_MONITOR_DIR = "C:/Users/ClaudeCode/Documents/llama-monitor"
test_llama-monitor.py:def run_tests():  # Run all test files and summarize results.
test_overflow.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_overflow.py:def test_overflow_prevention():  # Verify grid items have min-width:0 and overflow prevention.
test_power_graph_autoscale.py:class TestPowerChartAutoScale(unittest.TestCase):  # Tests for power chart auto-scaling in web_server.py.
test_power_graph_autoscale.py:    def setUp(self):  # Set up test fixtures.
test_power_graph_autoscale.py:    def test_power_chart_has_separate_options_from_usage_chart(self):  # Test that power chart has separate chart options from GPU/CPU usage chart.
test_power_graph_autoscale.py:    def test_power_chart_datasets_exist(self):  # Test that power chart has GPU Power and CPU Power datasets.
test_power_graph_autoscale.py:    def test_power_values_calculated_from_power_w(self):  # Test that power values are calculated from gpu_power_w and cpu_power_w.
test_power_graph_autoscale.py:    def test_power_chart_uses_powerChartOptions(self):  # Test that power chart uses powerChartOptions instead of chartOptions.
test_power_graph_autoscale.py:    def test_historical_power_chart_uses_powerChartOptions(self):  # Test that historical power chart uses powerChartOptions.
test_power_graph_autoscale.py:class TestTuiPowerChart(unittest.TestCase):  # Tests for TUI power chart rendering.
test_power_graph_autoscale.py:    def setUp(self):  # Set up test fixtures.
test_power_graph_autoscale.py:    def test_tui_calculates_power_values(self):  # Test that TUI calculates power values from gpu_power_w and cpu_power_w.
test_power_graph_autoscale.py:    def test_tui_power_chart_draws_bars(self):  # Test that TUI draws power bars in the chart.
test_power_graph_autoscale.py:class TestPowerScaleCalculation(unittest.TestCase):  # Tests for power scale calculation logic.
test_power_graph_autoscale.py:    def test_max_power_with_high_values(self):  # Test that max_power calculation handles values > 100W.
test_power_graph_autoscale.py:    def test_power_scale_margin(self):  # Test that power scale includes margin above max value.
test_power_graph_autoscale.py:class TestAutoScaleBehavior(unittest.TestCase):  # Tests for auto-scale behavior verification.
test_power_graph_autoscale.py:    def test_auto_scale_with_empty_data(self):  # Test auto-scale behavior with empty data.
test_power_graph_autoscale.py:    def test_auto_scale_with_single_value(self):  # Test auto-scale behavior with single power value.
test_power_graph_autoscale.py:    def test_auto_scale_with_varied_values(self):  # Test auto-scale behavior with varied power values.
test_power_width.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_power_width.py:def test_power_item_width():  # Verify power-item has width constraints for consistent sizing.
test_redundant_subtitles.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_redundant_subtitles.py:def test_no_redundant_subtitles():  # Verify redundant graph subtitles are removed.
test_server_metrics.py:class TestServerMetricsCollector(unittest.TestCase):  # Tests for ServerMetricsCollector.
test_server_metrics.py:    def setUp(self):  # Create a collector for testing.
test_server_metrics.py:    def test_init_strips_trailing_slash(self):  # Test that init strips trailing slash from URL.
test_server_metrics.py:    def test_make_request_success(self, mock_get):  # Test successful HTTP request.
test_server_metrics.py:    def test_make_request_failure(self, mock_get):  # Test failed HTTP request.
test_server_metrics.py:    def test_get_metrics(self, mock_make_request):  # Test getting metrics from /metrics endpoint.
test_server_metrics.py:    def test_get_slots(self, mock_make_request):  # Test getting slots from /slots endpoint.
test_server_metrics.py:    def test_get_props(self, mock_make_request):  # Test getting props from /props endpoint.
test_server_metrics.py:    def test_collect(self, mock_make_request):  # Test collecting all metrics.
test_server_metrics.py:        def mock_side_effect(endpoint):
test_server_metrics.py:    def test_collect_partial_failure(self, mock_make_request):  # Test collecting when some endpoints fail.
test_server_metrics.py:        def mock_side_effect(endpoint):
test_server_metrics.py:class TestParseMetrics(unittest.TestCase):  # Tests for _parse_metrics method.
test_server_metrics.py:    def setUp(self):
test_server_metrics.py:    def test_parse_metrics_dict(self):  # Test parsing dict-format metrics.
test_server_metrics.py:    def test_parse_metrics_string_prometheus(self):  # Test parsing Prometheus-format string metrics.
test_server_metrics.py:    def test_parse_metrics_string_with_comments(self):  # Test parsing metrics with comment lines.
test_server_metrics.py:    def test_parse_metrics_string_invalid_value(self):  # Test parsing metrics with invalid values.
test_server_metrics.py:    def test_parse_metrics_empty_string(self):  # Test parsing empty metrics string.
test_server_metrics.py:    def test_parse_metrics_empty_dict(self):  # Test parsing empty metrics dict.
test_server_metrics.py:    def test_compute_instant_rates_first_call_returns_zero(self):  # Test that first call to _compute_instant_rates returns 0 rates.
test_server_metrics.py:    def test_compute_instant_rates_second_call(self):  # Test that second call computes delta correctly.
test_server_metrics.py:    def test_compute_instant_rates_idle_returns_zero(self):  # Test that idle server returns 0 rates.
test_server_metrics.py:    def test_compute_instant_rates_missing_fields(self):  # Test that missing fields don't crash.
test_server_metrics.py:class TestParseSlots(unittest.TestCase):  # Tests for _parse_slots method.
test_server_metrics.py:    def setUp(self):
test_server_metrics.py:    def test_parse_slots_list(self):  # Test parsing list of slots.
test_server_metrics.py:    def test_parse_slots_dict_single(self):  # Test parsing single slot as dict.
test_server_metrics.py:    def test_parse_slots_empty_list(self):  # Test parsing empty slot list.
test_server_metrics.py:    def test_parse_slots_none(self):  # Test parsing None slots.
test_server_metrics.py:    def test_parse_slots_missing_fields(self):  # Test parsing slots with missing fields.
test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):  # Tests for format_metrics_display function.
test_server_metrics.py:    def test_format_metrics_display_full(self):  # Test formatting metrics with all data.
test_server_metrics.py:    def test_format_metrics_display_empty(self):  # Test formatting empty metrics.
test_server_metrics.py:    def test_format_metrics_display_no_slots(self):  # Test formatting metrics without slots.
test_server_metrics.py:    def test_format_metrics_display_zero_values(self):  # Test formatting metrics with zero values.
test_slot_charts.py:class TestSlotChartsData(unittest.TestCase):  # Tests for slot progress and context remaining data.
test_slot_charts.py:    def setUp(self):  # Set up test fixtures.
test_slot_charts.py:    def test_slot_progress_calculation(self, mock_make_request):  # Test that slot progress is correctly calculated from slot data.
test_slot_charts.py:    def test_props_with_context_limit(self, mock_make_request):  # Test that props data includes context limit (n_ctx).
test_slot_charts.py:    def test_slot_data_structure(self, mock_make_request):  # Test that slot data has the expected structure.
test_slot_charts.py:    def test_empty_slots(self, mock_make_request):  # Test handling of empty slots list.
test_slot_charts.py:    def test_missing_fields_with_defaults(self, mock_make_request):  # Test that missing slot fields get default values.
test_slot_charts.py:class TestAggregatorSlotData(unittest.TestCase):  # Tests for aggregator slot data extraction.
test_slot_charts.py:    def test_aggregator_includes_slots_in_server_metrics(self, mock_collector):  # Test that aggregator includes slots data in server metrics.
test_slot_charts.py:    def test_aggregator_empty_slots(self, mock_collector):  # Test aggregator handles empty slots gracefully.
test_slot_charts.py:class TestSlotChartsJavaScript(unittest.TestCase):  # Tests for JavaScript slot chart rendering logic.
test_slot_charts.py:    def test_slot_progress_percentage_conversion(self):  # Test that progress 0-1 is converted to percentage 0-100.
test_slot_charts.py:        def calculate_progress_percentage(progress):
test_slot_charts.py:        class Math:
test_slot_charts.py:            def round(value):
test_slot_charts.py:            def min(*args):
test_slot_charts.py:    def test_context_remaining_calculation(self):  # Test context remaining calculation.
test_slot_charts.py:class TestSlotChartsIntegration(unittest.TestCase):  # Integration tests for slot charts with full metrics flow.
test_slot_charts.py:    def test_full_metrics_flow_with_slots(self, mock_db, mock_cost_calc, mock_system, mock_server):  # Test full metrics collection flow includes slot data.
test_slot_delta_graph.py:TEMPLATE_PATH = os.path.join(
test_slot_delta_graph.py:def test_previous_slot_tokens_state():  # Verify previousSlotTokens state variable exists.
test_slot_delta_graph.py:def test_crosshair_registered_for_tokens():  # Verify crosshair plugin is registered for tokensChart.
test_slot_delta_graph.py:def test_interaction_mode_index():  # Verify tokensChart has interaction mode: index for crosshair.
test_slot_delta_graph.py:def test_legend_displayed():  # Verify tokensChart shows legend for per-slot labels.
test_slot_delta_graph.py:def test_delta_calculation():  # Verify delta calculation logic exists.
test_slot_delta_graph.py:def test_per_slot_datasets():  # Verify per-slot dataset generation.
test_slot_delta_graph.py:def test_no_tokens_per_sec_usage():  # Verify predicted_tokens_seconds is no longer used for the graph.
test_slot_delta_graph.py:def test_slot_colors():  # Verify per-slot color scheme.
test_slot_height.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_slot_height.py:def test_slot_height_adequate():  # Verify the slot height calculation provides adequate space for labels.
test_system_metrics.py:class TestSystemMetricsCollectorInit(unittest.TestCase):  # Tests for SystemMetricsCollector initialization.
test_system_metrics.py:    def test_init_default_tracked_processes(self):  # Test default tracked processes.
test_system_metrics.py:    def test_init_custom_tracked_processes(self):  # Test custom tracked processes.
test_system_metrics.py:    def test_init_with_wmi(self, mock_wmi):  # Test initialization with WMI available.
test_system_metrics.py:    def test_init_wmi_exception(self, mock_wmi):  # Test initialization when WMI raises exception.
test_system_metrics.py:class TestContextManager(unittest.TestCase):  # Tests for context manager functionality.
test_system_metrics.py:    def test_enter_returns_self(self):  # Test __enter__ returns self.
test_system_metrics.py:    def test_exit_calls_close(self, mock_nvml):  # Test __exit__ calls close.
test_system_metrics.py:class TestCollectCPU(unittest.TestCase):  # Tests for CPU metrics collection.
test_system_metrics.py:    def test_collect_cpu_success(self, mock_psutil):  # Test successful CPU metrics collection.
test_system_metrics.py:    def test_collect_cpu_no_psutil(self, mock_psutil):  # Test CPU collection when psutil is not available.
test_system_metrics.py:    def test_collect_cpu_process_filtering(self):  # Test that only tracked processes are included.
test_system_metrics.py:    def test_collect_cpu_process_exception_handling(self):  # Test handling of process access exceptions.
test_system_metrics.py:class TestCollectGPU(unittest.TestCase):  # Tests for GPU metrics collection.
test_system_metrics.py:    def test_collect_gpu_nvml_success(self, mock_nvml):  # Test GPU metrics collection with NVML.
test_system_metrics.py:    def test_collect_gpu_no_gpus(self, mock_nvml):  # Test GPU collection when no GPUs found.
test_system_metrics.py:    def test_collect_gpu_wmi(self, mock_wmi):  # Test GPU metrics collection with WMI.
test_system_metrics.py:    def test_collect_gpu_no_monitoring_available(self):  # Test GPU collection when no monitoring library is available.
test_system_metrics.py:class TestCollectMemory(unittest.TestCase):  # Tests for memory metrics collection.
test_system_metrics.py:    def test_collect_memory_success(self):  # Test successful memory metrics collection.
test_system_metrics.py:class TestCollectProcessGPU(unittest.TestCase):  # Tests for per-process GPU metrics collection.
test_system_metrics.py:    def test_collect_process_gpu_success(self, mock_nvml, mock_psutil):  # Test successful per-process GPU metrics collection.
test_system_metrics.py:    def test_collect_process_gpu_no_nvml(self, mock_nvml):  # Test per-process GPU collection when NVML is not initialized.
test_system_metrics.py:    def test_collect_process_gpu_fallback_to_v1(self, mock_nvml):  # Test fallback to v1 API when v2 is not available.
test_system_metrics.py:class TestCollectSystemPower(unittest.TestCase):  # Tests for system power metrics collection.
test_system_metrics.py:    def test_collect_system_power_battery(self, mock_wmi):  # Test system power collection with battery data.
test_system_metrics.py:    def test_collect_system_power_no_battery(self, mock_wmi):  # Test system power collection without battery data.
test_system_metrics.py:class TestCollect(unittest.TestCase):  # Tests for main collect method.
test_system_metrics.py:    def test_collect_full(self, mock_system_power, mock_process_gpu, mock_memory, mock_gpu, mock_cpu):  # Test full metrics collection.
test_tokens_idle_reset.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_tokens_idle_reset.py:def test_tokens_graph_no_reset_on_idle():  # Verify Tokens/Sec graph does NOT reset to [0] on idle — appends zeros instead.
test_total_cost_label.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_total_cost_label.py:def test_total_cost_label():  # Verify Total Cost label is present above the monthly total.
test_web_server_settings.py:class TestSettingsEndpoints(unittest.TestCase):  # Tests for settings API endpoints.
test_web_server_settings.py:    def setUp(self):  # Create test client and temp database.
test_web_server_settings.py:    def tearDown(self):  # Clean up.
test_web_server_settings.py:    def test_api_get_settings_returns_default_values(self):  # Test GET /api/settings returns default values when no settings exist.
test_web_server_settings.py:    def test_api_get_settings_returns_stored_values(self):  # Test GET /api/settings returns stored values.
test_web_server_settings.py:    def test_api_set_settings_updates_values(self):  # Test POST /api/settings updates settings.
test_web_server_settings.py:    def test_api_set_cost_rate_updates_value(self):  # Test POST /api/settings/cost_rate updates cost rate.
test_web_server_settings.py:    def test_api_set_cost_rate_validates_negative(self):  # Test POST /api/settings/cost_rate rejects negative values.
test_web_server_settings.py:    def test_api_set_cost_rate_validates_missing(self):  # Test POST /api/settings/cost_rate rejects missing cost_rate.
test_web_server_settings.py:    def test_api_set_cost_rate_validates_invalid(self):  # Test POST /api/settings/cost_rate rejects invalid values.
test_web_server_settings.py:    def test_api_reset_settings_clears_all(self):  # Test POST /api/settings/reset clears all settings.
tui.py:def format_significant_digits(value: float, digits: int = 4) -> str:  # Format a value with the specified number of significant digits.
tui.py:class TUI:  # Terminal UI for llama-monitor.
tui.py:    def __init__(
tui.py:    def _fetch_metrics(self) -> Optional[Dict[str, Any]]:  # Fetch latest metrics from aggregator daemon or shared cache.
tui.py:    def _init_colors(self) -> None:  # Initialize color pairs for curses.
tui.py:    def _draw_header(self, stdscr) -> None:  # Draw the header section.
tui.py:    def _draw_cost_section(self, stdscr, start_row: int) -> int:  # Draw the cost display section.
tui.py:    def _draw_server_section(self, stdscr, start_row: int) -> int:  # Draw the server status section.
tui.py:    def _draw_system_section(self, stdscr, start_row: int) -> int:  # Draw the system resources section.
tui.py:    def _draw_power_section(self, stdscr, start_row: int) -> int:  # Draw the power and energy section.
tui.py:    def _draw_process_gpu_section(self, stdscr, start_row: int) -> int:  # Draw the per-process GPU section.
tui.py:    def _draw_progress_bar(self, stdscr, row: int, col: int, value: float, width: int) -> None:  # Draw a progress bar.
tui.py:    def _draw_history_chart(self, stdscr, start_row: int) -> int:  # Draw the history chart section.
tui.py:    def _draw_footer(self, stdscr) -> None:  # Draw the footer with controls.
tui.py:    def _main_loop(self, stdscr) -> None:  # Main TUI loop.
tui.py:    def run(self) -> None:  # Run the TUI.
tui.py:    def stop(self) -> None:  # Stop the TUI.
tui.py:def main() -> int:  # Main entry point for the TUI.
web_server.py:app = Flask(__name__, static_folder=None, template_folder='templates')
web_server.py:socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")
web_server.py:def get_aggregator() -> Optional[Aggregator]:  # Get aggregator instance if available.
web_server.py:def get_config() -> Any:  # Get configuration.
web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:  # Fetch latest metrics from aggregator daemon via HTTP API.
web_server.py:def transform_system_metrics(data: Dict[str, Any]) -> Dict[str, Any]:  # Transform flat system metrics keys to nested structure for frontend.
web_server.py:    def safe_float(value, default=-1):  # Convert None or non-numeric values to default.
web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:  # Fetch latest metrics from SQLite database.
web_server.py:def index() -> str:  # Serve the main dashboard HTML.
web_server.py:def api_latest_metrics():  # Return latest metrics from metrics_cache, aggregator, or database.
web_server.py:def api_metrics():  # Alias for /api/metrics/latest for backwards compatibility.
web_server.py:def api_latest_metrics_db():  # Return latest metrics from database directly.
web_server.py:def api_range_metrics():  # Return metrics within a time range.
web_server.py:def api_monthly_cost():  # Return monthly cost data for the last 30 days.
web_server.py:def api_metrics_list():  # Return list of available metrics and tables.
web_server.py:def api_historical_metrics():  # Return historical metrics for a specified timeframe.
web_server.py:def api_historical_range():  # Return historical metrics for a custom time range.
web_server.py:def api_status():  # Return aggregator status.
web_server.py:def api_stop_server():  # Stop the web server gracefully.
web_server.py:def api_restart_server():  # Restart the web server by spawning a new process and shutting down the current one.
web_server.py:        def restart_server():
web_server.py:def get_db():  # Get database instance.
web_server.py:def settings_page():  # Serve the settings page HTML.
web_server.py:def cost_comparison_page():  # Serve the cost comparison page HTML.
web_server.py:def api_get_settings():  # Get all settings from the database.
web_server.py:def api_set_settings():  # Set settings in the database.
web_server.py:def api_reset_settings():  # Reset settings to defaults.
web_server.py:def api_set_cost_rate():  # Update the cost rate setting.
web_server.py:def api_get_vendor_rates():  # Get all vendor rates.
web_server.py:def api_add_vendor_rate():  # Add a new vendor rate.
web_server.py:def api_update_vendor_rate(vendor_name):  # Update an existing vendor rate.
web_server.py:def api_delete_vendor_rate(vendor_name):  # Delete a vendor rate.
web_server.py:def api_get_token_accumulator():  # Get today's token tracking statistics.
web_server.py:def api_get_vendor_comparison():  # Get vendor cost comparison based on today's tokens.
web_server.py:def handle_connect():  # Handle WebSocket connection.
web_server.py:def handle_disconnect():  # Handle WebSocket disconnection.
web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False, verbose=False):  # Run the web server.
web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None, verbose=False):  # Start the web server in a background thread.
web_server.py:    def run():
web_server.py:def stop_server():  # Stop the running web server.
web_server.py:def main():  # Main entry point.
_llamacpp_logger.py:LISTEN_PORT = 8000
_llamacpp_logger.py:LLAMA_URL = "http://127.0.0.1:8001"
_llamacpp_logger.py:ENABLE_LOGGING = True
_llamacpp_logger.py:LOG_FILE = "_llamacpp_logger.log"
_llamacpp_logger.py:class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
_llamacpp_logger.py:    def _log(self, text):
_llamacpp_logger.py:    def _forward_and_stream(self, req):
_llamacpp_logger.py:    def do_GET(self):
_llamacpp_logger.py:    def do_POST(self):
_llamacpp_logger.py:class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
_sanitizing_proxy_firewall_and_logger.py:LISTEN_PORT = 8000
_sanitizing_proxy_firewall_and_logger.py:LLAMA_URL = "http://127.0.0.1:8001"
_sanitizing_proxy_firewall_and_logger.py:ENABLE_LOGGING = False  # Toggle to True to save payloads to crash_log.txt
_sanitizing_proxy_firewall_and_logger.py:class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
_sanitizing_proxy_firewall_and_logger.py:    def _forward_and_stream(self, req):  # Helper to forward the request and stream the response back chunk-by-chunk
_sanitizing_proxy_firewall_and_logger.py:    def do_GET(self):
_sanitizing_proxy_firewall_and_logger.py:    def do_POST(self):
_sanitizing_proxy_firewall_and_logger.py:class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
backup/server_metrics.py:class ServerMetricsCollector:  # Collects metrics from llama.cpp server endpoints.
backup/server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):  # Initialize the collector.
backup/server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:  # Make HTTP request to server endpoint.
backup/server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:  # Fetch metrics from /metrics endpoint.
backup/server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:  # Fetch slot information from /slots endpoint.
backup/server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:  # Fetch server properties from /props endpoint.
backup/server_metrics.py:    def collect(self) -> Dict[str, Any]:  # Collect all server metrics.
backup/server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:  # Parse Prometheus-format metrics.
backup/server_metrics.py:    def _parse_slots(self, slots: Any) -> list:  # Parse slot data.
backup/server_metrics.py:                    def _v(key, default=0):
backup/server_metrics.py:    def _compute_instant_rates(self, server: Dict[str, Any]) -> None:  # Calculate instantaneous token rates from cumulative delta.
backup/server_metrics.py:def format_metrics_display(metrics: Dict[str, Any]) -> str:  # Format metrics for display.
backup/_llamacpp_logger.py:LISTEN_PORT = 8000
backup/_llamacpp_logger.py:LLAMA_URL = "http://127.0.0.1:8001"
backup/_llamacpp_logger.py:ENABLE_LOGGING = True
backup/_llamacpp_logger.py:LOG_FILE = "_llamacpp_logger.log"
backup/_llamacpp_logger.py:class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
backup/_llamacpp_logger.py:    def _log(self, text):
backup/_llamacpp_logger.py:    def _forward_and_stream(self, req):
backup/_llamacpp_logger.py:    def do_GET(self):
backup/_llamacpp_logger.py:    def do_POST(self):
backup/_llamacpp_logger.py:class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
