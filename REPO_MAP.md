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
./aggregator.py:    def _safe_float(self, value, default=0.0):
./aggregator.py:    def collect_all_metrics(self) -> Dict[str, Any]:
./aggregator.py:    def store_raw_metrics(self, metrics: Dict[str, Any]) -> None:
./aggregator.py:    def compress_if_needed(self) -> None:
./aggregator.py:    def _vacuum_throttled(self) -> None:
./aggregator.py:    def calculate_cost(self) -> Dict[str, Any]:
./aggregator.py:    def calculate_today_cost(self) -> Dict[str, Any]:
./aggregator.py:    def close(self) -> None:
./aggregator.py:    def __enter__(self):
./aggregator.py:    def __exit__(self, exc_type, exc_val, exc_tb):
./cli_stats.py:def parse_args():
./cli_stats.py:def fetch_metrics(host: str, port: int) -> Optional[Dict[str, Any]]:
./cli_stats.py:def _value_or_zero(val, sentinel=-1.0):
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
./db.py:    def recover_from_corruption(self) -> bool:
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
./db.py:    def get_monthly_energy(self, days: int = 30) -> List[Dict[str, Any]]:
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
./db.py:    def get_idle_baseline_w(self) -> float:
./db.py:    def set_idle_baseline_w(self, power_w: float) -> None:
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
./DebugTools/llama-raw-capture-tool/capture.py:class CaptureAbort(Exception):
./DebugTools/llama-raw-capture-tool/capture.py:class Session:
./DebugTools/llama-raw-capture-tool/capture.py:def load_config(path: str) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/capture.py:def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/capture.py:def derived_capture_flags(config: Dict[str, Any], session_dir: Path) -> List[str]:
./DebugTools/llama-raw-capture-tool/capture.py:def quote_flags(flags: List[str]) -> str:
./DebugTools/llama-raw-capture-tool/capture.py:def detect_bat_style(content: str) -> str:
./DebugTools/llama-raw-capture-tool/capture.py:def _extra_args_block() -> str:
./DebugTools/llama-raw-capture-tool/capture.py:def _leading_ws(line: str) -> str:
./DebugTools/llama-raw-capture-tool/capture.py:def inject_extra_args(content: str, style: str) -> str:
./DebugTools/llama-raw-capture-tool/capture.py:def session_dir_name(now_epoch_s: float) -> str:
./DebugTools/llama-raw-capture-tool/capture.py:def create_session_dir(output_dir: Path, now_epoch_s: float) -> Path:
./DebugTools/llama-raw-capture-tool/capture.py:def acquire_session_lock(session_dir: Path) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def release_session_lock(session_dir: Path) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def _url_to_hostport(url: str) -> Tuple[str, int]:
./DebugTools/llama-raw-capture-tool/capture.py:def port_in_use(server_url: str) -> bool:
./DebugTools/llama-raw-capture-tool/capture.py:def preflight(config: Dict[str, Any], session_dir: Path) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def stamp_and_append(path: Path, record: Dict[str, Any]) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def _append_text(path: Path, text: str) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def write_text(path: Path, text: str) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def write_json(path: Path, obj: Any) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def http_get_json(url: str, timeout: float = 3.0) -> Optional[Any]:
./DebugTools/llama-raw-capture-tool/capture.py:def http_get_text(url: str, timeout: float = 3.0) -> Optional[str]:
./DebugTools/llama-raw-capture-tool/capture.py:def log_source_failure(session: Session, source: str, detail: str) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def log_source_ok(session: Session, source: str) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def _append_capture_log(session: Session, line: str) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def poll_slots(session: Session, stop: threading.Event) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def poll_metrics(session: Session, stop: threading.Event) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def fetch_props(session: Session) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def poll_monitor(session: Session, stop: threading.Event) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def _sleep_interruptible(stop: threading.Event, seconds: float) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def parse_relative_timestamp_us(text: str) -> Optional[int]:
./DebugTools/llama-raw-capture-tool/capture.py:def _file_creation_time(path: Path) -> Tuple[Optional[str], Optional[int]]:
./DebugTools/llama-raw-capture-tool/capture.py:def tail_log(session: Session, stop: threading.Event) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def nvml_available() -> bool:
./DebugTools/llama-raw-capture-tool/capture.py:def _sample_process(psutil_mod: Any, pid: Optional[int]) -> Optional[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/capture.py:def _sample_nvml(llama_pid: Optional[int]) -> Optional[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/capture.py:def sample_nvml_psutil(session: Session, llama_pid: Optional[int]) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/capture.py:def poll_nvml_psutil(session: Session, stop: threading.Event) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def build_typeperf_counters() -> List[str]:
./DebugTools/llama-raw-capture-tool/capture.py:def _fallback_counters() -> List[str]:
./DebugTools/llama-raw-capture-tool/capture.py:def _select_counter_paths(qx_output: str) -> List[str]:
./DebugTools/llama-raw-capture-tool/capture.py:def run_typeperf(session: Session, stop: threading.Event) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def resolve_launch_script(launch_script: str) -> Path:
./DebugTools/llama-raw-capture-tool/capture.py:def write_wrapper_bat(session: Session, content: str) -> Path:
./DebugTools/llama-raw-capture-tool/capture.py:def install_windows_ctrl_handler(session: "Session") -> None:
./DebugTools/llama-raw-capture-tool/capture.py:        def handler(ctrl_type: int) -> bool:
./DebugTools/llama-raw-capture-tool/capture.py:def spawn_launcher(
./DebugTools/llama-raw-capture-tool/capture.py:def resolve_llama_pid(session: Session) -> Optional[int]:
./DebugTools/llama-raw-capture-tool/capture.py:def teardown_process_tree(session: Session) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def _terminate_linux_tree(pid: int) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def consistency_check(session: Session) -> bool:
./DebugTools/llama-raw-capture-tool/capture.py:def _host_info(session: Session) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/capture.py:def _persist_anchor(session: Session) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def write_manifest(session: Session, end_wallclock: str) -> None:
./DebugTools/llama-raw-capture-tool/capture.py:def resolve_output_dir(config: Dict[str, Any]) -> Path:
./DebugTools/llama-raw-capture-tool/capture.py:def run_capture(config: Dict[str, Any], duration: Optional[float] = None) -> Session:
./DebugTools/llama-raw-capture-tool/capture.py:def _config_source_path() -> Optional[str]:
./DebugTools/llama-raw-capture-tool/capture.py:def main(argv: Optional[List[str]] = None) -> int:
./DebugTools/llama-raw-capture-tool/common.py:def wallclock_stamp() -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/common.py:def iso_from_epoch_us(epoch_us: int) -> str:
./DebugTools/llama-raw-capture-tool/common.py:def iso_from_epoch_s(epoch_s: float) -> str:
./DebugTools/llama-raw-capture-tool/postprocess.py:def extract_slot_task(text: str) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_console_event(line: str, wallclock_iso: str) -> Optional[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _coerce(value: str):
./DebugTools/llama-raw-capture-tool/postprocess.py:def read_jsonl_tolerant(path: Path) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def load_anchor(session_dir: Path) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _derive_anchor_from_console(session_dir: Path) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _write_anchor_uncertain(session_dir: Path, uncertain: bool) -> None:
./DebugTools/llama-raw-capture-tool/postprocess.py:def convert_relative_to_wallclock(anchor: Dict[str, Any], R_us) -> Optional[str]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_slots(session_dir: Path) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_metrics(session_dir: Path) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_prometheus_text(text: str) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_props(session_dir: Path) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_nvml_psutil(session_dir: Path) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_monitor(session_dir: Path) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_typeperf_csv(session_dir: Path) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _typeperf_header(path: Path) -> List[str]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _csv_timestamp_to_iso(y, mo, d, h, mi, s, us) -> str:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_prompts(session_dir: Path, anchor: Dict[str, Any]) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _iso_from_epoch_us(epoch_us: int) -> str:
./DebugTools/llama-raw-capture-tool/postprocess.py:def parse_console(session_dir: Path) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def build_event_stream(session_dir: Path) -> Dict[str, Any]:
./DebugTools/llama-raw-capture-tool/postprocess.py:    def _note_if_missing(name, path):
./DebugTools/llama-raw-capture-tool/postprocess.py:def _summarize(events: List[Dict[str, Any]]) -> Dict[str, int]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _anchor_self_checks(anchor: Dict[str, Any], events: List[Dict[str, Any]],
./DebugTools/llama-raw-capture-tool/postprocess.py:        def _iso_to_us(s):
./DebugTools/llama-raw-capture-tool/postprocess.py:def build_divergence_report(
./DebugTools/llama-raw-capture-tool/postprocess.py:def _correlate_gen_rate(console, metrics, findings) -> None:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _correlate_activity(console, slots, nvml, findings) -> None:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _correlate_monitor_latency(monitor, console, findings) -> None:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _is_number(value) -> bool:
./DebugTools/llama-raw-capture-tool/postprocess.py:def replay_through_monitor(session_dir: Path, stream: Dict[str, Any]) -> List[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def _try_import(module_name: str, attr: str):
./DebugTools/llama-raw-capture-tool/postprocess.py:def _monitor_pin() -> Optional[Dict[str, Any]]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def render_report_md(stream: Dict[str, Any], findings: List[Dict[str, Any]],
./DebugTools/llama-raw-capture-tool/postprocess.py:def write_outputs(session_dir: Path) -> Dict[str, str]:
./DebugTools/llama-raw-capture-tool/postprocess.py:def main(argv: Optional[List[str]] = None) -> int:
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_wallclock_stamp_has_both_fields():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_iso_from_epoch_us_known_epoch():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_detect_bat_style_multiline():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_detect_bat_style_singleline():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_detect_bat_style_unknown():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_inject_extra_args_multiline():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_inject_extra_args_singleline():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_inject_extra_args_unknown_unchanged():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_inject_preserves_direct_run_semantics():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_derived_capture_flags(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_quote_flags_quotes_every_token():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_relative_timestamp_us():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_relative_timestamp_us_none():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_session_dir_name_format():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_create_session_dir_and_counter(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_stamp_and_append(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_load_config_merges_defaults(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_port_in_use_false_for_unbound():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_preflight_when_port_free(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_preflight_port_in_use_aborts(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def _stamp_line(line):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_console_slot_gen_rate():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_console_server_listening():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_console_prompt_process():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_console_returns_none_for_unmatched():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_prometheus_text_keeps_labels():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_typeperf_csv_skips_headers(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_typeperf_csv_missing_file(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_prompts(tmp_path, anchor_factory):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_build_event_stream_and_report(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_write_outputs(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_resolve_llama_pid_non_windows_uses_spawned_pid(monkeypatch):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_ctrl_handler_handles_close_break_and_ctrl_c(monkeypatch):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:    class FakeWINFUNCTYPE:
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:        def __init__(self, *a, **k):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:        def __call__(self, fn):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:    def fake_set_console_ctrl_handler(callback, add):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_persist_anchor_writes_anchor_json(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_persist_anchor_noop_without_anchor(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_load_anchor_recovers_from_console_when_no_manifest(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_load_anchor_prefers_manifest_when_present(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_load_anchor_recovers_from_anchor_json(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_load_anchor_empty_when_nothing_available(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_anchor_self_checks_file_creation_skew_flags(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_anchor_self_checks_file_creation_ok(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_anchor_self_checks_prompt_clock_misalignment():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_anchor_self_checks_prompt_clock_aligned_no_flag():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_anchor_self_checks_prompt_clock_uses_session_dir_fallback(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_anchor_self_checks_activity_window_disjoint():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_write_anchor_uncertain_writes_manifest(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_slots_task_id_uses_id_task(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def test_parse_slots_maps_is_processing_to_state(tmp_path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def _write_minimal_session(session_dir: Path):
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:def anchor_factory():
./DebugTools/llama-raw-capture-tool/test_capture_tool.py:    def make(log_epoch_us: int) -> dict:
./electricity_cost.py:class ElectricityCostCalculator:
./electricity_cost.py:    def __init__(
./electricity_cost.py:    def _load_cumulative_energy(self) -> None:
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
./electricity_cost.py:    def clear_session_energy(self) -> Dict[str, Any]:
./idle_baseline.py:class IdleBaselineTracker:
./idle_baseline.py:    def __init__(
./idle_baseline.py:    def check_idle(
./idle_baseline.py:    def _store_baseline(self, baseline_w: float) -> None:
./idle_baseline.py:    def get_baseline_average(self) -> Optional[float]:
./idle_baseline.py:    def get_recent_baseline(self, count: int = 10) -> Optional[float]:
./idle_baseline.py:    def clear_baseline_data(self) -> None:
./idle_baseline.py:    def reset(self) -> None:
./lancedb_mcp_server.py:class MemoryItem(BaseModel):
./lancedb_mcp_server.py:def save_memory(content: str, tags: List[str] = None) -> str:
./lancedb_mcp_server.py:def search_memory(query: str, n_results: int = 5) -> List[dict]:
./lancedb_mcp_server.py:def get_unique_tags() -> List[str]:
./llamamonitor.py:def format_significant_digits(value: float, digits: int = 4) -> str:
./llamamonitor.py:class MetricsCache:
./llamamonitor.py:    def __init__(self):
./llamamonitor.py:    def update(self, metrics: Dict[str, Any]):
./llamamonitor.py:    def get(self) -> Dict[str, Any]:
./llamamonitor.py:class Monitor:
./llamamonitor.py:    def __init__(
./llamamonitor.py:    def initialize(self):
./llamamonitor.py:    def run_aggregator_loop(self):
./llamamonitor.py:    def shutdown(self):
./llamamonitor.py:    def run_web_mode(self):
./llamamonitor.py:    def run_tui_mode(self):
./llamamonitor.py:    def show_statistics(self):
./llamamonitor.py:    def run(self):
./llamamonitor.py:def parse_args() -> argparse.Namespace:
./llamamonitor.py:def ensure_dependencies(check_tui: bool = False):
./llamamonitor.py:def main():
./llamamonitor.py:    def signal_handler(signum, frame):
./server_metrics.py:class ServerMetricsCollector:
./server_metrics.py:    def __init__(self, server_url: str, metrics_endpoint: str = "/metrics", collect_metrics: bool = True):
./server_metrics.py:    def _make_request(self, endpoint: str) -> Optional[Any]:
./server_metrics.py:    def get_metrics(self) -> Optional[Dict[str, Any]]:
./server_metrics.py:    def get_slots(self) -> Optional[Dict[str, Any]]:
./server_metrics.py:    def get_props(self) -> Optional[Dict[str, Any]]:
./server_metrics.py:    def collect(self) -> Dict[str, Any]:
./server_metrics.py:    def _parse_metrics(self, metrics: Any) -> Dict[str, Any]:
./server_metrics.py:    def _parse_slots(self, slots: Any) -> list:
./server_metrics.py:            def _v(key, default=0):
./server_metrics.py:    def _compute_instant_rates(self, server: Dict[str, Any]) -> None:
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
./system_metrics.py:    def _get_linux_cpu_power_w(self) -> float:
./system_metrics.py:    def _collect_system_power(self) -> Dict[str, Any]:
./test_active_slots_fix.py:class TestActiveSlotsDisplay(unittest.TestCase):
./test_active_slots_fix.py:    def test_format_metrics_display_with_slots(self):
./test_active_slots_fix.py:    def test_format_metrics_display_empty_slots(self):
./test_active_slots_fix.py:    def test_format_metrics_display_no_slots_key(self):
./test_active_slots_fix.py:    def test_format_metrics_display_single_active_slot(self):
./test_active_slots_fix.py:    def test_format_metrics_display_all_idle(self):
./test_active_slots_fix.py:class TestSlotsDataFlow(unittest.TestCase):
./test_active_slots_fix.py:    def test_collector_collects_slots(self, mock_get):
./test_active_slots_fix.py:    def test_parse_slots_list(self, mock_make_request):
./test_active_slots_fix.py:    def test_parse_slots_none_returns_empty(self, mock_make_request):
./test_active_slots_fix.py:        def side_effect(endpoint):
./test_active_slots_fix.py:    def test_aggregator_slots_extraction(self, mock_db, mock_idle, mock_cost_calc, mock_system, mock_server):
./test_active_slots_fix.py:class TestWebServerSlotsUpdate(unittest.TestCase):
./test_active_slots_fix.py:    def test_html_has_active_slots_element(self):
./test_active_slots_fix.py:    def test_javascript_updates_active_slots(self):
./test_active_slots_fix.py:    def test_javascript_has_slots_filter_logic(self):
./test_active_slots_fix.py:    def test_javascript_has_slots_reduce_logic(self):
./test_active_slots_fix.py:class TestRequestsProcessingDisplay(unittest.TestCase):
./test_active_slots_fix.py:    def test_html_has_server_processing_element(self):
./test_active_slots_fix.py:    def test_javascript_updates_server_processing(self):
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
./test_api_data_integrity.py:def fetch_metrics(base_url):
./test_api_data_integrity.py:def find_negative_one_values(data, path=""):
./test_api_data_integrity.py:def is_expected_sentinel(path):
./test_api_data_integrity.py:def main():
./test_bar_labels.py:def test_bar_labels_and_k_unit():
./test_bp3_backports.py:def _make_system_metrics(cpu_percent=50.0, gpu_usage=80.0, power_w=300.0):
./test_bp3_backports.py:class TestIdleTrackingBackport(unittest.TestCase):
./test_bp3_backports.py:    def setUp(self):
./test_bp3_backports.py:    def tearDown(self):
./test_bp3_backports.py:    def test_check_idle_called_when_values_meaningful(self, mock_req, mock_idle):
./test_bp3_backports.py:    def test_check_idle_not_called_when_all_zero(self, mock_req, mock_idle):
./test_bp3_backports.py:class TestLastMetricsBackport(unittest.TestCase):
./test_bp3_backports.py:    def setUp(self):
./test_bp3_backports.py:    def tearDown(self):
./test_bp3_backports.py:    def test_last_metrics_set_on_collect(self, mock_req):
./test_bp3_backports.py:class TestRealDurationBackport(unittest.TestCase):
./test_bp3_backports.py:    def setUp(self):
./test_bp3_backports.py:    def tearDown(self):
./test_bp3_backports.py:    def test_store_uses_real_duration_not_hardcoded(self):
./test_bp3_backports.py:class TestCumulativeEnergyBackport(unittest.TestCase):
./test_bp3_backports.py:    def setUp(self):
./test_bp3_backports.py:    def tearDown(self):
./test_bp3_backports.py:    def test_store_persists_cumulative_energy(self):
./test_bp3_backports.py:class TestApiStatusRework(unittest.TestCase):
./test_bp3_backports.py:    def test_api_status_returns_standalone(self):
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
./test_config.py:    def test_config_attribute_access(self):
./test_configuration_link.py:def test_configuration_link():
./test_context_limit_path.py:def test_context_limit_data_path():
./test_cpu_normalization.py:def _build_aggregator():
./test_cpu_normalization.py:def _make_system_metrics(cpu_count, process_cpu_values):
./test_cpu_normalization.py:class TestCpuNormalization(unittest.TestCase):
./test_cpu_normalization.py:    def test_clamped_to_100_when_sum_equals_core_capacity(self):
./test_cpu_normalization.py:    def test_clamps_and_warns_when_avg_exceeds_100(self):
./test_cpu_normalization.py:    def test_no_clamp_when_avg_within_range(self):
./test_cpu_normalization.py:    def test_fallback_to_os_cpu_when_no_process_cpu(self):
./test_crosshair.py:def test_crosshair_implementation():
./test_daily_cost_naming.py:def test_daily_cost_naming():
./test_dashboard_mapping.py:def get_nested_value(data, path):
./test_dashboard_mapping.py:def transform_value(value, transform, data=None):
./test_dashboard_mapping.py:    def safe_value(v):
./test_dashboard_mapping.py:def fetch_metrics(base_url):
./test_dashboard_mapping.py:def main():
./test_dashboard_transforms.py:class TestDataTransformation(unittest.TestCase):
./test_dashboard_transforms.py:    def test_transform_width(self):
./test_dashboard_transforms.py:    def test_transform_count_active(self):
./test_dashboard_transforms.py:    def test_transform_count_active_empty(self):
./test_dashboard_transforms.py:    def test_transform_mem_text(self):
./test_dashboard_transforms.py:    def test_transform_mem_text_cpu_fallback(self):
./test_dashboard_transforms.py:    def test_transform_mem_bar(self):
./test_dashboard_transforms.py:    def test_transform_mem_bar_zero_total(self):
./test_dashboard_transforms.py:    def test_transform_mem_bar_cpu_fallback(self):
./test_dashboard_transforms.py:    def test_transform_sum_power(self):
./test_dashboard_transforms.py:    def test_transform_sum_with_null(self):
./test_dashboard_transforms.py:    def test_transform_sum_with_minus_one(self):
./test_dashboard_transforms.py:    def test_transform_noop(self):
./test_dashboard_transforms.py:    def test_get_nested_value_simple(self):
./test_dashboard_transforms.py:    def test_get_nested_value_missing(self):
./test_dashboard_transforms.py:    def test_get_nested_value_null(self):
./test_dashboard_transforms.py:class TestNegativeOneDetection(unittest.TestCase):
./test_dashboard_transforms.py:    def test_find_negative_one_in_dict(self):
./test_dashboard_transforms.py:    def test_find_negative_one_in_list(self):
./test_dashboard_transforms.py:    def test_find_negative_one_nested(self):
./test_dashboard_transforms.py:    def test_no_negative_one(self):
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
./test_database.py:class TestMonthlyEnergy(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_get_monthly_energy_empty_database(self):
./test_database.py:    def test_get_monthly_energy_with_data(self):
./test_database.py:    def test_get_monthly_energy_cost_rate(self):
./test_database.py:    def test_get_monthly_energy_with_cost_calculation(self):
./test_database.py:    def test_get_monthly_energy_different_day_counts(self):
./test_database.py:    def test_get_monthly_energy_partial_data(self):
./test_database.py:    def test_get_monthly_energy_data_values(self):
./test_database.py:class TestApiMonthlyCost(unittest.TestCase):
./test_database.py:    def setUp(self):
./test_database.py:    def tearDown(self):
./test_database.py:    def test_api_monthly_cost_with_data(self):
./test_database.py:    def test_api_monthly_cost_empty_database(self):
./test_database.py:    def test_api_monthly_cost_date_format(self):
./test_database.py:    def test_api_monthly_cost_error_handling(self):
./test_database.py:class TestJavaScriptDateFormatting(unittest.TestCase):
./test_database.py:    def test_date_formatting_logic(self):
./test_database.py:        def format_date_js(date_str):
./test_database.py:    def test_date_padding_logic(self):
./test_database.py:        def format_date_with_padding(date_str):
./test_db_purge.py:def _system_metrics(ts, cpu_percent=50.0, cpu_power_w=65.0, gpu_power_w=220.0,
./test_db_purge.py:def _server_metrics(ts):
./test_db_purge.py:class TestCompressionPurge(unittest.TestCase):
./test_db_purge.py:    def setUp(self):
./test_db_purge.py:    def tearDown(self):
./test_db_purge.py:    def _insert_system_raw(self, count=3, start_offset_s=120):
./test_db_purge.py:    def _insert_server_raw(self, count=3, start_offset_s=120):
./test_db_purge.py:    def test_compress_to_1m_purges_raw_rows(self):
./test_db_purge.py:    def test_compress_to_1h_purges_1m_rows(self):
./test_db_purge.py:    def test_repeated_compression_does_not_reaccumulate(self):
./test_db_purge.py:    def test_compress_if_needed_vacuum_throttled(self):
./test_db_purge.py:    def test_vacuum_reclaims_space(self):
./test_dollar_sign.py:def test_dollar_sign_placement():
./test_energy_deltas.py:class PerIntervalDeltaTest(unittest.TestCase):
./test_energy_deltas.py:    def setUp(self):
./test_energy_deltas.py:    def tearDown(self):
./test_energy_deltas.py:    def test_update_power_readings_returns_deltas(self):
./test_energy_deltas.py:    def test_combined_metrics_store_delta_fields(self):
./test_energy_deltas.py:    def test_delta_and_cumulative_both_present(self):
./test_filtered_power.py:def _read_template():
./test_filtered_power.py:def test_cpu_normalizes_per_core_scale():
./test_filtered_power.py:def test_cpu_fraction_clamped_to_1():
./test_filtered_power.py:def test_gpu_fraction_clamped_to_1():
./test_filtered_power.py:def test_gpu_requires_process_data():
./test_filtered_power.py:def test_charts_section_normalizes_cpu():
./test_full_pipeline.py:class TestFullPipeline(unittest.TestCase):
./test_full_pipeline.py:    def setUp(self):
./test_full_pipeline.py:    def tearDown(self):
./test_full_pipeline.py:    def _make_fake_system_metrics(self):
./test_full_pipeline.py:    def test_full_pipeline_with_fake_data(self):
./test_full_pipeline.py:    def test_pipeline_without_llama_server(self):
./test_full_pipeline.py:    def test_frontend_json_compatible(self):
./test_header_link.py:def test_no_server_link():
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
./test_k_format.py:def test_k_format_on_context_chart():
./test_llama-monitor.py:def run_tests():
./test_overflow.py:def test_overflow_prevention():
./test_power_graph_autoscale.py:class TestPowerChartAutoScale(unittest.TestCase):
./test_power_graph_autoscale.py:    def setUp(self):
./test_power_graph_autoscale.py:    def test_power_chart_has_separate_options_from_usage_chart(self):
./test_power_graph_autoscale.py:    def test_power_chart_datasets_exist(self):
./test_power_graph_autoscale.py:    def test_power_values_calculated_from_power_w(self):
./test_power_graph_autoscale.py:    def test_power_chart_uses_powerChartOptions(self):
./test_power_graph_autoscale.py:    def test_historical_power_chart_uses_powerChartOptions(self):
./test_power_graph_autoscale.py:class TestTuiPowerChart(unittest.TestCase):
./test_power_graph_autoscale.py:    def setUp(self):
./test_power_graph_autoscale.py:    def test_tui_calculates_power_values(self):
./test_power_graph_autoscale.py:    def test_tui_power_chart_draws_bars(self):
./test_power_graph_autoscale.py:class TestPowerScaleCalculation(unittest.TestCase):
./test_power_graph_autoscale.py:    def test_max_power_with_high_values(self):
./test_power_graph_autoscale.py:    def test_power_scale_margin(self):
./test_power_graph_autoscale.py:class TestAutoScaleBehavior(unittest.TestCase):
./test_power_graph_autoscale.py:    def test_auto_scale_with_empty_data(self):
./test_power_graph_autoscale.py:    def test_auto_scale_with_single_value(self):
./test_power_graph_autoscale.py:    def test_auto_scale_with_varied_values(self):
./test_power_width.py:def test_power_item_width():
./test_redundant_subtitles.py:def test_no_redundant_subtitles():
./test_repo_map_exclude.py:def test_debugtools_excluded():
./test_sanitizer_scrub.py:class MediaMarkerScrubberTest(unittest.TestCase):
./test_sanitizer_scrub.py:    def test_regex_matches_media_marker(self):
./test_sanitizer_scrub.py:    def test_regex_ignores_unrelated_text(self):
./test_sanitizer_scrub.py:    def test_scrub_payload_removes_markers(self):
./test_sanitizer_scrub.py:    def test_scrub_payload_multiple_markers(self):
./test_sanitizer_scrub.py:    def test_scrub_payload_no_marker_unchanged(self):
./test_sanitizer_scrub.py:    def test_scrub_payload_non_utf8(self):
./test_sanitizer_scrub.py:    def test_get_scrubs_props_response(self):
./test_sanitizer_scrub.py:    def test_post_body_scrubbed(self):
./test_sanitizer_scrub.py:    def test_logging_uses_decoded_body_str(self):
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
./test_server_metrics.py:    def test_compute_instant_rates_first_call_returns_zero(self):
./test_server_metrics.py:    def test_compute_instant_rates_second_call(self):
./test_server_metrics.py:    def test_compute_instant_rates_idle_returns_zero(self):
./test_server_metrics.py:    def test_compute_instant_rates_missing_fields(self):
./test_server_metrics.py:class TestParseSlots(unittest.TestCase):
./test_server_metrics.py:    def setUp(self):
./test_server_metrics.py:    def test_parse_slots_list(self):
./test_server_metrics.py:    def test_parse_slots_dict_single(self):
./test_server_metrics.py:    def test_parse_slots_empty_list(self):
./test_server_metrics.py:    def test_parse_slots_none(self):
./test_server_metrics.py:    def test_parse_slots_missing_fields(self):
./test_server_metrics.py:    def test_parse_slots_is_processing_derives_state_and_progress(self):
./test_server_metrics.py:    def test_parse_slots_explicit_state_priority(self):
./test_server_metrics.py:class TestFormatMetricsDisplay(unittest.TestCase):
./test_server_metrics.py:    def test_format_metrics_display_full(self):
./test_server_metrics.py:    def test_format_metrics_display_empty(self):
./test_server_metrics.py:    def test_format_metrics_display_no_slots(self):
./test_server_metrics.py:    def test_format_metrics_display_zero_values(self):
./test_slot_charts.py:class TestSlotChartsData(unittest.TestCase):
./test_slot_charts.py:    def setUp(self):
./test_slot_charts.py:    def test_slot_progress_calculation(self, mock_make_request):
./test_slot_charts.py:    def test_props_with_context_limit(self, mock_make_request):
./test_slot_charts.py:    def test_slot_data_structure(self, mock_make_request):
./test_slot_charts.py:    def test_empty_slots(self, mock_make_request):
./test_slot_charts.py:    def test_missing_fields_with_defaults(self, mock_make_request):
./test_slot_charts.py:class TestAggregatorSlotData(unittest.TestCase):
./test_slot_charts.py:    def test_aggregator_includes_slots_in_server_metrics(self, mock_idle, mock_collector):
./test_slot_charts.py:    def test_aggregator_empty_slots(self, mock_idle, mock_collector):
./test_slot_charts.py:class TestSlotChartsJavaScript(unittest.TestCase):
./test_slot_charts.py:    def test_slot_progress_percentage_conversion(self):
./test_slot_charts.py:        def calculate_progress_percentage(progress):
./test_slot_charts.py:        class Math:
./test_slot_charts.py:            def round(value):
./test_slot_charts.py:            def min(*args):
./test_slot_charts.py:    def test_context_remaining_calculation(self):
./test_slot_charts.py:class TestSlotChartsIntegration(unittest.TestCase):
./test_slot_charts.py:    def test_full_metrics_flow_with_slots(self, mock_db, mock_idle, mock_cost_calc, mock_system, mock_server):
./test_slot_chart_width.py:def test_slot_chart_width():
./test_slot_delta_graph.py:def test_previous_slot_tokens_state():
./test_slot_delta_graph.py:def test_crosshair_registered_for_tokens():
./test_slot_delta_graph.py:def test_interaction_mode_index():
./test_slot_delta_graph.py:def test_legend_displayed():
./test_slot_delta_graph.py:def test_delta_calculation():
./test_slot_delta_graph.py:def test_per_slot_datasets():
./test_slot_delta_graph.py:def test_no_tokens_per_sec_usage():
./test_slot_delta_graph.py:def test_slot_colors():
./test_slot_height.py:def test_slot_height_adequate():
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
./test_toggle_buttons.py:def test_toggle_buttons():
./test_tokens_gauge_source.py:def _read_template():
./test_tokens_gauge_source.py:def test_uses_authoritative_gauges_not_instant():
./test_tokens_gauge_source.py:def test_gates_on_activity_for_idle_decay():
./test_tokens_gauge_source.py:def test_still_appends_data_for_smooth_decay():
./test_tokens_idle_reset.py:def test_tokens_graph_no_reset_on_idle():
./test_total_cost_label.py:def test_total_cost_label():
./test_tui_chart_colors.py:def read_tui():
./test_tui_chart_colors.py:class HistoryChartColorTest(unittest.TestCase):
./test_tui_chart_colors.py:    def setUp(self):
./test_tui_chart_colors.py:    def test_power_color_is_distinct_from_gpu(self):
./test_tui_chart_colors.py:    def test_gpu_and_power_use_different_color_keys(self):
./test_tui_chart_colors.py:    def test_power_color_pair_defined(self):
./test_tui_chart_colors.py:    def test_legend_reflects_actual_colors(self):
./test_tui_chart_colors.py:    def test_cpu_and_power_no_overlap_with_gpu(self):
./test_tui_chart_colors.py:    def test_legend_does_not_claim_wrong_colors(self):
./test_verbose_gating.py:def test_debug_gated_by_verbose():
./test_web_server_settings.py:class TestSettingsEndpoints(unittest.TestCase):
./test_web_server_settings.py:    def setUp(self):
./test_web_server_settings.py:    def tearDown(self):
./test_web_server_settings.py:    def test_api_get_settings_returns_default_values(self):
./test_web_server_settings.py:    def test_api_get_settings_returns_stored_values(self):
./test_web_server_settings.py:    def test_api_set_settings_updates_values(self):
./test_web_server_settings.py:    def test_api_set_cost_rate_updates_value(self):
./test_web_server_settings.py:    def test_api_set_cost_rate_validates_negative(self):
./test_web_server_settings.py:    def test_api_set_cost_rate_validates_missing(self):
./test_web_server_settings.py:    def test_api_set_cost_rate_validates_invalid(self):
./test_web_server_settings.py:    def test_api_reset_settings_clears_all(self):
./tui.py:def format_significant_digits(value: float, digits: int = 4) -> str:
./tui.py:class TUI:
./tui.py:    def __init__(
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
./web_server.py:def get_config() -> Any:
./web_server.py:def _get_db(db_path: str) -> "Database":
./web_server.py:def transform_system_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
./web_server.py:    def safe_float(value, default=0):
./web_server.py:def fetch_metrics_from_database(db_path: str) -> Optional[Dict[str, Any]]:
./web_server.py:def index() -> str:
./web_server.py:def _transform_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
./web_server.py:def api_latest_metrics():
./web_server.py:def api_metrics():
./web_server.py:def api_latest_metrics_db():
./web_server.py:def api_range_metrics():
./web_server.py:def api_monthly_cost():
./web_server.py:def api_historical_metrics():
./web_server.py:def api_historical_range():
./web_server.py:def api_status():
./web_server.py:def api_stop_server():
./web_server.py:        func = request.environ.get('werkzeug.server.shutdown')
./web_server.py:def api_restart_server():
./web_server.py:        def restart_server():
./web_server.py:def get_db():
./web_server.py:def settings_page():
./web_server.py:def cost_comparison_page():
./web_server.py:def api_get_settings():
./web_server.py:def api_set_settings():
./web_server.py:def api_reset_settings():
./web_server.py:def api_set_cost_rate():
./web_server.py:def api_get_graph_preferences():
./web_server.py:def api_set_graph_preferences():
./web_server.py:def api_get_vendor_rates():
./web_server.py:def api_add_vendor_rate():
./web_server.py:def api_update_vendor_rate(vendor_name):
./web_server.py:def api_delete_vendor_rate(vendor_name):
./web_server.py:def api_get_token_accumulator():
./web_server.py:def api_get_vendor_comparison():
./web_server.py:def handle_connect():
./web_server.py:def handle_disconnect():
./web_server.py:def run_server(host="0.0.0.0", port=8080, debug=False, verbose=False):
./web_server.py:def start_server(host="0.0.0.0", port=8080, metrics_cache=None, verbose=False, debug=False):
./web_server.py:    def run():
./web_server.py:def stop_server():
./web_server.py:def main():
./_llamacpp_logger.py:class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
./_llamacpp_logger.py:    def _log(self, text):
./_llamacpp_logger.py:    def _forward_and_stream(self, req):
./_llamacpp_logger.py:    def do_GET(self):
./_llamacpp_logger.py:    def do_POST(self):
./_llamacpp_logger.py:class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
./_sanitizing_proxy_firewall_and_logger.py:class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
./_sanitizing_proxy_firewall_and_logger.py:    def scrub_payload(body: bytes) -> bytes:
./_sanitizing_proxy_firewall_and_logger.py:    def _forward_and_stream(self, req, scrub=False):
./_sanitizing_proxy_firewall_and_logger.py:    def do_GET(self):
./_sanitizing_proxy_firewall_and_logger.py:    def do_POST(self):
./_sanitizing_proxy_firewall_and_logger.py:class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
