# Repository Map - Test Files
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
test_configuration_link.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_configuration_link.py:def test_configuration_link():  # Verify a link to /settings exists in the dashboard controls.
test_context_limit_path.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_context_limit_path.py:def test_context_limit_data_path():  # Verify the context limit is read from data.props, not data.server.props.
test_cpu_normalization.py:def _build_aggregator():
test_cpu_normalization.py:def _make_system_metrics(cpu_count, process_cpu_values):  # Build a system_metrics dict with the given CPU data.
test_cpu_normalization.py:class TestCpuNormalization(unittest.TestCase):
test_cpu_normalization.py:    def test_clamped_to_100_when_sum_equals_core_capacity(self):
test_cpu_normalization.py:    def test_clamps_and_warns_when_avg_exceeds_100(self):
test_cpu_normalization.py:    def test_no_clamp_when_avg_within_range(self):
test_cpu_normalization.py:    def test_fallback_to_os_cpu_when_no_process_cpu(self):
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
test_database.py:    def tearDown(self):  # Clean up temporary database and restore patches.
test_database.py:    def test_api_monthly_cost_with_data(self):  # Test API returns correct cost data when database has energy data.
test_database.py:    def test_api_monthly_cost_empty_database(self):  # Test API returns empty data when database has no energy data.
test_database.py:    def test_api_monthly_cost_date_format(self):  # Test that API returns dates in correct format.
test_database.py:    def test_api_monthly_cost_error_handling(self):  # Test API error handling for invalid database path.
test_database.py:class TestJavaScriptDateFormatting(unittest.TestCase):  # Tests for JavaScript date formatting logic (MM/dd/yyyy).
test_database.py:    def test_date_formatting_logic(self):  # Test the date formatting algorithm used in JavaScript.
test_database.py:        def format_date_js(date_str):  # Format date as MM/dd/yyyy following JavaScript logic.
test_database.py:    def test_date_padding_logic(self):  # Test that day/month padding works correctly.
test_database.py:        def format_date_with_padding(date_str):  # Format date with proper padding like JavaScript.
test_db_purge.py:def _system_metrics(ts, cpu_percent=50.0, cpu_power_w=65.0, gpu_power_w=220.0,
test_db_purge.py:def _server_metrics(ts):
test_db_purge.py:class TestCompressionPurge(unittest.TestCase):  # Verify compression purges source rows so the DB does not grow unbounded.
test_db_purge.py:    def setUp(self):
test_db_purge.py:    def tearDown(self):
test_db_purge.py:    def _insert_system_raw(self, count=3, start_offset_s=120):  # Insert `count` raw system metrics across ~2 minutes ago.
test_db_purge.py:    def _insert_server_raw(self, count=3, start_offset_s=120):
test_db_purge.py:    def test_compress_to_1m_purges_raw_rows(self):  # After folding into 1m buckets, the source raw rows are deleted.
test_db_purge.py:    def test_compress_to_1h_purges_1m_rows(self):  # After folding 1m into 1h buckets, the source 1m rows are deleted.
test_db_purge.py:    def test_repeated_compression_does_not_reaccumulate(self):  # Running compress_to_1m twice should not purge un-aggregated data or fail.
test_db_purge.py:    def test_compress_if_needed_vacuum_throttled(self):  # compress_if_needed runs a throttled VACUUM (max hourly) after purging.
test_db_purge.py:    def test_vacuum_reclaims_space(self):  # After purging raw rows, VACUUM should reclaim disk space.
test_dollar_sign.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_dollar_sign.py:def test_dollar_sign_placement():  # Verify dollar sign is on Monthly Cost chart, not Tokens/s chart.
test_filtered_power.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_filtered_power.py:def _read_template():
test_filtered_power.py:def test_cpu_normalizes_per_core_scale():  # llama's per-process CPU must be normalized by core count.
test_filtered_power.py:def test_cpu_fraction_clamped_to_1():  # The llama CPU fraction must be clamped to [0,1] to avoid over-attribution.
test_filtered_power.py:def test_gpu_fraction_clamped_to_1():  # The GPU fraction must be clamped to [0,1].
test_filtered_power.py:def test_gpu_requires_process_data():  # Filtered GPU power must gate on per-process GPU data (NVML).
test_filtered_power.py:def test_charts_section_normalizes_cpu():  # updateCharts must apply the same per-core normalization.
test_full_pipeline.py:class TestFullPipeline(unittest.TestCase):  # Test the full data pipeline end-to-end.
test_full_pipeline.py:    def setUp(self):
test_full_pipeline.py:    def tearDown(self):
test_full_pipeline.py:    def _make_fake_system_metrics(self):  # Simulate what SystemMetricsCollector.collect() returns (nested format).
test_full_pipeline.py:    def test_full_pipeline_with_fake_data(self):  # Feed fake data through the pipeline and verify web API output format.
test_full_pipeline.py:    def test_pipeline_without_llama_server(self):  # Test pipeline works even when llama.cpp server is unavailable.
test_full_pipeline.py:    def test_frontend_json_compatible(self):  # Verify the final output is JSON-serializable.
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
test_llama-monitor.py:LLAMA_MONITOR_DIR = os.path.dirname(os.path.abspath(__file__))
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
test_power_width.py:def test_power_item_width():  # Verify power-value is nowrap and power-item has a min-width.
test_redundant_subtitles.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_redundant_subtitles.py:def test_no_redundant_subtitles():  # Verify redundant graph subtitles are removed.
test_repo_map_exclude.py:FINISH_BEAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finish-bead")
test_repo_map_exclude.py:def test_debugtools_excluded():  # Verify 'DebugTools' appears in the finish-bead EXCLUDE_DIRS set.
test_sanitizer_scrub.py:class MediaMarkerScrubberTest(unittest.TestCase):
test_sanitizer_scrub.py:    def test_regex_matches_media_marker(self):
test_sanitizer_scrub.py:    def test_regex_ignores_unrelated_text(self):
test_sanitizer_scrub.py:    def test_scrub_payload_removes_markers(self):
test_sanitizer_scrub.py:    def test_scrub_payload_multiple_markers(self):
test_sanitizer_scrub.py:    def test_scrub_payload_no_marker_unchanged(self):
test_sanitizer_scrub.py:    def test_scrub_payload_non_utf8(self):
test_sanitizer_scrub.py:    def test_get_scrubs_props_response(self):  # do_GET for /props must scrub the response body.
test_sanitizer_scrub.py:    def test_post_body_scrubbed(self):  # POST body scrubbing should be applied (media marker removed).
test_sanitizer_scrub.py:    def test_logging_uses_decoded_body_str(self):  # Logging path must use body_str (already-decoded, scrubbed), not re-decode.
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
test_server_metrics.py:    def test_parse_slots_is_processing_derives_state_and_progress(self):  # Slots with is_processing=true should get state=processing and progress.
test_server_metrics.py:    def test_parse_slots_explicit_state_priority(self):  # An explicit state field should take priority over is_processing.
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
test_slot_chart_width.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_slot_chart_width.py:def test_slot_chart_width():  # Verify slot graphs stretch full width and left padding is reduced.
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
test_toggle_buttons.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_toggle_buttons.py:def test_toggle_buttons():  # Verify toggle-cost-btn is removed and toggle-temps-btn is hidden.
test_tokens_gauge_source.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_tokens_gauge_source.py:def _read_template():
test_tokens_gauge_source.py:def test_uses_authoritative_gauges_not_instant():  # The graph should use predicted/prompt_tokens_seconds, not _instant delta rates.
test_tokens_gauge_source.py:def test_gates_on_activity_for_idle_decay():  # Rates should be gated on requests_processing so idle decays to 0.
test_tokens_gauge_source.py:def test_still_appends_data_for_smooth_decay():  # The graph must still always append data so idle decays smoothly to 0.
test_tokens_idle_reset.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_tokens_idle_reset.py:def test_tokens_graph_no_reset_on_idle():  # Verify Tokens/Sec graph does NOT reset to [0] on idle — appends zeros instead.
test_total_cost_label.py:TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
test_total_cost_label.py:def test_total_cost_label():  # Verify Total Cost label is present above the monthly total.
test_tui_chart_colors.py:TUI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tui.py")
test_tui_chart_colors.py:def read_tui():
test_tui_chart_colors.py:class HistoryChartColorTest(unittest.TestCase):
test_tui_chart_colors.py:    def setUp(self):
test_tui_chart_colors.py:    def test_power_color_is_distinct_from_gpu(self):
test_tui_chart_colors.py:    def test_gpu_and_power_use_different_color_keys(self):
test_tui_chart_colors.py:    def test_power_color_pair_defined(self):
test_tui_chart_colors.py:    def test_legend_reflects_actual_colors(self):
test_tui_chart_colors.py:    def test_cpu_and_power_no_overlap_with_gpu(self):
test_tui_chart_colors.py:    def test_legend_does_not_claim_wrong_colors(self):
test_verbose_gating.py:SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llamamonitor.py")
test_verbose_gating.py:def test_debug_gated_by_verbose():
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
