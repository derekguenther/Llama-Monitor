# Repository Map - Project Code
# Files beginning with underscore (_) are user-side supporting tools, not part of the project.
# Test files are in docs/REPO_MAP_TESTS.md
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
web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None, verbose=False):  # Start the web server in a background thread.
web_server.py:    def run():
web_server.py:def stop_server():  # Stop the running web server.
web_server.py:def main():  # Main entry point.
