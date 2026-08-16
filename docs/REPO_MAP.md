# Repository Map - Project Code
# Files beginning with underscore (_) are user-side supporting tools, not part of the project.
# Test files are in docs/REPO_MAP_TESTS.md
aggregator.py:class Aggregator:  # Orchestrate all metrics collection and storage.
aggregator.py:    def __init__(
aggregator.py:    def _safe_float(self, value, default=0.0):  # Convert None or non-numeric values to default.
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
db.py:    def recover_from_corruption(self) -> bool:  # Rebuild the database if it is corrupt, so the monitor keeps running.
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
db.py:    def get_idle_baseline_w(self) -> float:  # Get idle baseline power from settings.
db.py:    def set_idle_baseline_w(self, power_w: float) -> None:  # Set idle baseline power in settings.
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
server_metrics.py:            def _v(key, default=0):
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
web_server.py:app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')
web_server.py:socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")
web_server.py:def get_aggregator() -> Optional[Aggregator]:  # Get aggregator instance if available.
web_server.py:def get_config() -> Any:  # Get configuration.
web_server.py:def _get_db(db_path: str) -> "Database":  # Return a shared, thread-safe Database instance for reads.
web_server.py:def fetch_metrics_from_aggregator() -> Optional[Dict[str, Any]]:  # Fetch latest metrics from aggregator daemon via HTTP API.
web_server.py:def transform_system_metrics(data: Dict[str, Any]) -> Dict[str, Any]:  # Transform flat system metrics keys to nested structure for frontend.
web_server.py:    def safe_float(value, default=0):  # Convert None or non-numeric values to default.
web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:  # Fetch latest metrics from SQLite database.
web_server.py:def index() -> str:  # Serve the main dashboard HTML.
web_server.py:def _transform_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:  # Transform flat system metrics to nested structure for frontend.
web_server.py:def api_latest_metrics():  # Return latest metrics from metrics_cache, aggregator, or database.
web_server.py:def api_metrics():  # Alias for /api/metrics/latest for backwards compatibility.
web_server.py:def api_latest_metrics_db():  # Return latest metrics from database directly.
web_server.py:def api_range_metrics():  # Return metrics within a time range.
web_server.py:def api_monthly_cost():  # Return monthly cost data for the last 30 days.
web_server.py:def api_historical_metrics():  # Return historical metrics for a specified timeframe.
web_server.py:def api_historical_range():  # Return historical metrics for a custom time range.
web_server.py:def api_status():  # Return aggregator status.
web_server.py:def api_stop_server():  # Stop the web server gracefully.
web_server.py:def api_restart_server():  # Restart the web server by spawning a new process and shutting down the current one.
web_server.py:        def restart_server():
web_server.py:def get_db():  # Get the shared database instance for settings access.
web_server.py:def settings_page():  # Serve the settings page HTML.
web_server.py:def cost_comparison_page():  # Serve the cost comparison page HTML.
web_server.py:def api_get_settings():  # Get all settings from the database.
web_server.py:def api_set_settings():  # Set settings in the database.
web_server.py:def api_reset_settings():  # Reset settings to defaults.
web_server.py:def api_set_cost_rate():  # Update the cost rate setting.
web_server.py:def api_get_graph_preferences():  # Get graph display preferences.
web_server.py:def api_set_graph_preferences():  # Save graph display preferences.
web_server.py:def api_get_vendor_rates():  # Get all vendor rates.
web_server.py:def api_add_vendor_rate():  # Add a new vendor rate.
web_server.py:def api_update_vendor_rate(vendor_name):  # Update an existing vendor rate.
web_server.py:def api_delete_vendor_rate(vendor_name):  # Delete a vendor rate.
web_server.py:def api_get_token_accumulator():  # Get today's token tracking statistics.
web_server.py:def api_get_vendor_comparison():  # Get vendor cost comparison based on today's tokens.
web_server.py:def handle_connect():  # Handle WebSocket connection.
web_server.py:def handle_disconnect():  # Handle WebSocket disconnection.
web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False, verbose=False):  # Run the web server.
web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None, verbose=False, debug=False):  # Start the web server in a background thread.
web_server.py:    def run():
web_server.py:def stop_server():  # Stop the running web server.
web_server.py:def main():  # Main entry point.
DebugTools/llama-raw-capture-tool/capture.py:APPEND_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_APPEND
DebugTools/llama-raw-capture-tool/capture.py:PID_RESOLVE_TIMEOUT_S = 10.0
DebugTools/llama-raw-capture-tool/capture.py:DEFAULT_CONFIG = {
DebugTools/llama-raw-capture-tool/capture.py:IS_WINDOWS = sys.platform == "win32"
DebugTools/llama-raw-capture-tool/capture.py:class CaptureAbort(Exception):  # Raised for a preflight or runtime abort that should stop the session.
DebugTools/llama-raw-capture-tool/capture.py:class Session:  # Holds paths, config, and runtime state for one capture session.
DebugTools/llama-raw-capture-tool/capture.py:def load_config(path: str) -> Dict[str, Any]:  # Load a YAML config, merged over defaults (explicit values win).
DebugTools/llama-raw-capture-tool/capture.py:def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
DebugTools/llama-raw-capture-tool/capture.py:def derived_capture_flags(config: Dict[str, Any], session_dir: Path) -> List[str]:  # Return the full flag list: configured flags + session-derived paths.
DebugTools/llama-raw-capture-tool/capture.py:def quote_flags(flags: List[str]) -> str:  # Join flags into a single command-line string with fully-quoted values.
DebugTools/llama-raw-capture-tool/capture.py:def detect_bat_style(content: str) -> str:  # Detect the structural style of a ``.bat`` launcher.
DebugTools/llama-raw-capture-tool/capture.py:def _extra_args_block() -> str:
DebugTools/llama-raw-capture-tool/capture.py:def _leading_ws(line: str) -> str:
DebugTools/llama-raw-capture-tool/capture.py:def inject_extra_args(content: str, style: str) -> str:  # Inject the ``EXTRA_ARGS`` mechanism into ``.bat`` content.
DebugTools/llama-raw-capture-tool/capture.py:def session_dir_name(now_epoch_s: float) -> str:  # Return ``YYYYMMDD-HHMMSS`` from a Unix epoch (seconds).
DebugTools/llama-raw-capture-tool/capture.py:def create_session_dir(output_dir: Path, now_epoch_s: float) -> Path:  # Create a timestamped session dir, appending ``-<counter>`` if taken.
DebugTools/llama-raw-capture-tool/capture.py:def acquire_session_lock(session_dir: Path) -> None:  # Create the session-lock file; fail if it already exists.
DebugTools/llama-raw-capture-tool/capture.py:def release_session_lock(session_dir: Path) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def _url_to_hostport(url: str) -> Tuple[str, int]:  # Parse ``http://host:port`` into (host, port).
DebugTools/llama-raw-capture-tool/capture.py:def port_in_use(server_url: str) -> bool:  # Return True if the server port is already accepting connections.
DebugTools/llama-raw-capture-tool/capture.py:def preflight(config: Dict[str, Any], session_dir: Path) -> None:  # Run preflight checks: port free + session lock acquired.
DebugTools/llama-raw-capture-tool/capture.py:def stamp_and_append(path: Path, record: Dict[str, Any]) -> None:  # Append a JSON record with canonical wall-clock stamps to ``path``.
DebugTools/llama-raw-capture-tool/capture.py:def _append_text(path: Path, text: str) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def write_text(path: Path, text: str) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def write_json(path: Path, obj: Any) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def http_get_json(url: str, timeout: float = 3.0) -> Optional[Any]:  # GET a URL and return parsed JSON (or None on any failure).
DebugTools/llama-raw-capture-tool/capture.py:def http_get_text(url: str, timeout: float = 3.0) -> Optional[str]:  # GET a URL and return the raw text body (or None on any failure).
DebugTools/llama-raw-capture-tool/capture.py:def log_source_failure(session: Session, source: str, detail: str) -> None:  # Record a source failure to capture.log (deduplicated per source).
DebugTools/llama-raw-capture-tool/capture.py:def log_source_ok(session: Session, source: str) -> None:  # Mark a source as reachable/ok (clears a prior failure state).
DebugTools/llama-raw-capture-tool/capture.py:def _append_capture_log(session: Session, line: str) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def poll_slots(session: Session, stop: threading.Event) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def poll_metrics(session: Session, stop: threading.Event) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def fetch_props(session: Session) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def poll_monitor(session: Session, stop: threading.Event) -> None:
DebugTools/llama-raw-capture-tool/capture.py:def _sleep_interruptible(stop: threading.Event, seconds: float) -> None:  # Sleep for ``seconds`` but wake immediately if ``stop`` is set.
DebugTools/llama-raw-capture-tool/capture.py:LOG_PREFIX_RE = re.compile(r"^\s*(\d+)\.(\d+)\.(\d+)\.(\d+)\s")
DebugTools/llama-raw-capture-tool/capture.py:def parse_relative_timestamp_us(text: str) -> Optional[int]:  # Parse the leading ``M.s.ms.µs`` prefix into microseconds since start.
DebugTools/llama-raw-capture-tool/capture.py:def _file_creation_time(path: Path) -> Tuple[Optional[str], Optional[int]]:  # Return (iso, epoch_us) of the file's creation time, if available.
DebugTools/llama-raw-capture-tool/capture.py:def tail_log(session: Session, stop: threading.Event) -> None:  # Tail llama-server.log, stamping each line with capture-side wall-clock.
DebugTools/llama-raw-capture-tool/capture.py:def nvml_available() -> bool:
DebugTools/llama-raw-capture-tool/capture.py:def _sample_process(psutil_mod: Any, pid: Optional[int]) -> Optional[Dict[str, Any]]:
DebugTools/llama-raw-capture-tool/capture.py:def _sample_nvml(llama_pid: Optional[int]) -> Optional[Dict[str, Any]]:
DebugTools/llama-raw-capture-tool/capture.py:def sample_nvml_psutil(session: Session, llama_pid: Optional[int]) -> Dict[str, Any]:  # Sample NVML (if available) + psutil into a single raw JSON record.
DebugTools/llama-raw-capture-tool/capture.py:def poll_nvml_psutil(session: Session, stop: threading.Event) -> None:
DebugTools/llama-raw-capture-tool/capture.py:TYPEPERF_OBJECTS = ["Processor", "GPU Engine", "Memory", "Process", "Energy Meter"]
DebugTools/llama-raw-capture-tool/capture.py:def build_typeperf_counters() -> List[str]:  # Discover installed counters at runtime via ``typeperf -qx``.
DebugTools/llama-raw-capture-tool/capture.py:def _fallback_counters() -> List[str]:  # A conservative minimal counter set when discovery is unavailable.
DebugTools/llama-raw-capture-tool/capture.py:def _select_counter_paths(qx_output: str) -> List[str]:  # Parse ``typeperf -qx`` output into a list of counter paths.
DebugTools/llama-raw-capture-tool/capture.py:def run_typeperf(session: Session, stop: threading.Event) -> None:  # Run typeperf writing CSV into the session dir; stop on Ctrl+C.
DebugTools/llama-raw-capture-tool/capture.py:def resolve_launch_script(launch_script: str) -> Path:  # Resolve the configured ``.bat`` relative to the tool directory.
DebugTools/llama-raw-capture-tool/capture.py:def write_wrapper_bat(session: Session, content: str) -> Path:  # Write the injected ``.bat`` into the session dir as ``launcher.bat``.
DebugTools/llama-raw-capture-tool/capture.py:def install_windows_ctrl_handler(session: "Session") -> None:  # Install a Windows console ctrl handler so console exit signals stop capture.
DebugTools/llama-raw-capture-tool/capture.py:        def handler(ctrl_type: int) -> bool:
DebugTools/llama-raw-capture-tool/capture.py:def spawn_launcher(
DebugTools/llama-raw-capture-tool/capture.py:def resolve_llama_pid(session: Session) -> Optional[int]:  # Resolve the spawned ``llama-server.exe`` PID via parent-child lookup.
DebugTools/llama-raw-capture-tool/capture.py:def teardown_process_tree(session: Session) -> None:  # Terminate the entire spawned process tree (cmd + llama-server.exe).
DebugTools/llama-raw-capture-tool/capture.py:def _terminate_linux_tree(pid: int) -> None:
DebugTools/llama-raw-capture-tool/capture.py:_BANNER_MODEL_RE = re.compile(r"loading model '(?P<model_path>[^']*)'")
DebugTools/llama-raw-capture-tool/capture.py:def consistency_check(session: Session) -> bool:  # Verify the API server on ``server_url`` is the one writing this session's
DebugTools/llama-raw-capture-tool/capture.py:def _host_info(session: Session) -> Dict[str, Any]:
DebugTools/llama-raw-capture-tool/capture.py:def _persist_anchor(session: Session) -> None:  # Write the anchor to an early, standalone file (survives hard kills).
DebugTools/llama-raw-capture-tool/capture.py:def write_manifest(session: Session, end_wallclock: str) -> None:
DebugTools/llama-raw-capture-tool/capture.py:DEFAULT_FILES = {
DebugTools/llama-raw-capture-tool/capture.py:def resolve_output_dir(config: Dict[str, Any]) -> Path:  # Resolve the configured output_dir to an absolute path.
DebugTools/llama-raw-capture-tool/capture.py:def run_capture(config: Dict[str, Any], duration: Optional[float] = None) -> Session:  # Run one capture session end-to-end and return the populated Session.
DebugTools/llama-raw-capture-tool/capture.py:def _config_source_path() -> Optional[str]:  # Return the path to the config.yaml next to this file.
DebugTools/llama-raw-capture-tool/capture.py:def main(argv: Optional[List[str]] = None) -> int:
DebugTools/llama-raw-capture-tool/common.py:def wallclock_stamp() -> Dict[str, Any]:  # Return a dict with the canonical capture-side wall-clock stamps.
DebugTools/llama-raw-capture-tool/common.py:def iso_from_epoch_us(epoch_us: int) -> str:  # Convert a Unix-epoch microsecond value to an ISO 8601 local + TZ string.
DebugTools/llama-raw-capture-tool/common.py:def iso_from_epoch_s(epoch_s: float) -> str:  # Convert a Unix-epoch (seconds, may be fractional) to ISO 8601 string.
DebugTools/llama-raw-capture-tool/postprocess.py:SESSION_LAYOUT = {
DebugTools/llama-raw-capture-tool/postprocess.py:FILE_CREATION_SKEW_TOLERANCE_S = 15.0
DebugTools/llama-raw-capture-tool/postprocess.py:PROMPT_CLOCK_TOLERANCE_MS = 5_000
DebugTools/llama-raw-capture-tool/postprocess.py:CONSOLE_PATTERNS = {
DebugTools/llama-raw-capture-tool/postprocess.py:SLOT_HEADER_RE = re.compile(r"id\s+(\d+)\s*\|\s*task\s+(\d+)\s*\|")
DebugTools/llama-raw-capture-tool/postprocess.py:def extract_slot_task(text: str) -> Dict[str, Any]:  # Extract ``id``/``task`` from a slot line's header, if present.
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_console_event(line: str, wallclock_iso: str) -> Optional[Dict[str, Any]]:  # Parse one stamped console line into a typed event dict, or None.
DebugTools/llama-raw-capture-tool/postprocess.py:def _coerce(value: str):  # Best-effort numeric coercion of a captured string group.
DebugTools/llama-raw-capture-tool/postprocess.py:def read_jsonl_tolerant(path: Path) -> List[Dict[str, Any]]:  # Read JSONL, skipping malformed/truncated lines; returns list of dicts.
DebugTools/llama-raw-capture-tool/postprocess.py:def load_anchor(session_dir: Path) -> Dict[str, Any]:  # Load the anchor from manifest.json; return {} if missing/invalid.
DebugTools/llama-raw-capture-tool/postprocess.py:def _derive_anchor_from_console(session_dir: Path) -> Dict[str, Any]:  # Recover ``log_epoch_us`` from the first stamped console record.
DebugTools/llama-raw-capture-tool/postprocess.py:def _write_anchor_uncertain(session_dir: Path, uncertain: bool) -> None:  # Set ``anchor_uncertain`` on manifest.json, preserving all other fields.
DebugTools/llama-raw-capture-tool/postprocess.py:def convert_relative_to_wallclock(anchor: Dict[str, Any], R_us) -> Optional[str]:  # Convert a relative log time ``R`` (µs) to wall-clock ISO using anchor.
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_slots(session_dir: Path) -> List[Dict[str, Any]]:  # Expand raw /slots arrays into per-slot events with wall-clock stamps.
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_metrics(session_dir: Path) -> List[Dict[str, Any]]:  # Parse raw Prometheus text bodies into per-metric events (global).
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_prometheus_text(text: str) -> Dict[str, Any]:  # Parse Prometheus text format into {metric_name: {labels, value}}.
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_props(session_dir: Path) -> Dict[str, Any]:  # Read props.json; return {} if missing.
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_nvml_psutil(session_dir: Path) -> List[Dict[str, Any]]:  # Read nvml-psutil.jsonl into typed events.
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_monitor(session_dir: Path) -> List[Dict[str, Any]]:  # Read monitor-api.jsonl into typed events.
DebugTools/llama-raw-capture-tool/postprocess.py:TYPEPERF_TS_RE = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2}):(\d{2}):(\d{2})\.(\d{6})")
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_typeperf_csv(session_dir: Path) -> List[Dict[str, Any]]:  # Parse typeperf CSV into per-row events with an ISO timestamp.
DebugTools/llama-raw-capture-tool/postprocess.py:def _typeperf_header(path: Path) -> List[str]:  # Read the counter-path header line (2nd line of the CSV).
DebugTools/llama-raw-capture-tool/postprocess.py:def _csv_timestamp_to_iso(y, mo, d, h, mi, s, us) -> str:  # Convert parsed typeperf timestamp components to an ISO 8601 string.
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_prompts(session_dir: Path, anchor: Dict[str, Any]) -> List[Dict[str, Any]]:  # Emit a ``new_prompt`` event per prompt file in the ``--log-prompts-dir``.
DebugTools/llama-raw-capture-tool/postprocess.py:def _iso_from_epoch_us(epoch_us: int) -> str:
DebugTools/llama-raw-capture-tool/postprocess.py:def parse_console(session_dir: Path) -> List[Dict[str, Any]]:  # Read stamped console.jsonl and emit typed console events.
DebugTools/llama-raw-capture-tool/postprocess.py:def build_event_stream(session_dir: Path) -> Dict[str, Any]:  # Assemble the unified timestamp-aligned event stream.
DebugTools/llama-raw-capture-tool/postprocess.py:    def _note_if_missing(name, path):
DebugTools/llama-raw-capture-tool/postprocess.py:def _summarize(events: List[Dict[str, Any]]) -> Dict[str, int]:
DebugTools/llama-raw-capture-tool/postprocess.py:def _anchor_self_checks(anchor: Dict[str, Any], events: List[Dict[str, Any]],
DebugTools/llama-raw-capture-tool/postprocess.py:        def _iso_to_us(s):
DebugTools/llama-raw-capture-tool/postprocess.py:def build_divergence_report(
DebugTools/llama-raw-capture-tool/postprocess.py:def _correlate_gen_rate(console, metrics, findings) -> None:  # Compare console ``slot_gen_rate`` tg vs /metrics bucket-average tokens/s.
DebugTools/llama-raw-capture-tool/postprocess.py:def _correlate_activity(console, slots, nvml, findings) -> None:  # Check that /slots and NVML/psutil activity windows overlap console spans.
DebugTools/llama-raw-capture-tool/postprocess.py:def _correlate_monitor_latency(monitor, console, findings) -> None:  # Account for monitor latency: /api/metrics/latest lags raw sources.
DebugTools/llama-raw-capture-tool/postprocess.py:def _is_number(value) -> bool:
DebugTools/llama-raw-capture-tool/postprocess.py:MONITOR_REPLAY_IMPORTS = {
DebugTools/llama-raw-capture-tool/postprocess.py:def replay_through_monitor(session_dir: Path, stream: Dict[str, Any]) -> List[Dict[str, Any]]:  # Feed raw data through Llama Monitor's parsing functions (optional).
DebugTools/llama-raw-capture-tool/postprocess.py:def _try_import(module_name: str, attr: str):  # Import ``attr`` from ``module_name`` if possible; return None on failure.
DebugTools/llama-raw-capture-tool/postprocess.py:def _monitor_pin() -> Optional[Dict[str, Any]]:  # Pin the monitor source so replay drift is detectable across runs.
DebugTools/llama-raw-capture-tool/postprocess.py:def render_report_md(stream: Dict[str, Any], findings: List[Dict[str, Any]],
DebugTools/llama-raw-capture-tool/postprocess.py:def write_outputs(session_dir: Path) -> Dict[str, str]:  # Run post-processing and write events.jsonl, report, and replay output.
DebugTools/llama-raw-capture-tool/postprocess.py:def main(argv: Optional[List[str]] = None) -> int:
