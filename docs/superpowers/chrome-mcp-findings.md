# Chrome MCP Plugin — Testing Findings

## Setup

- **Plugin**: obra/superpowers-chrome v3.0.2
- **Location**: `/home/yolo_agent/superpowers-chrome/`
- **MCP Server**: `/home/yolo_agent/superpowers-chrome/mcp/dist/index.js`
- **Browser**: Chromium 149.0.7827.155
- **Config**: `/home/yolo_agent/.config/opencode/opencode.json` (under `mcp.chrome`)

## Architecture

```
OpenCode (MCP Client)
    |
    v
Chrome MCP Server (stdio)
    |
    v
chrome-ws-lib.js (library)
    |
    v
Chromium Browser (CDP on port 9222)
```

The MCP server uses `chrome-ws-lib.js` to control Chromium via the Chrome DevTools Protocol. It auto-starts Chrome on first navigation action and manages tab state persistently.

## Chrome Startup Flow

1. MCP server receives `initialize` request
2. Client sends `notifications/initialized`
3. Client calls `use_browser` with `action: "navigate"`
4. MCP server detects no running Chrome, spawns Chromium with:
   - `--headless --no-sandbox --remote-debugging-port=9222`
   - `--user-data-dir=~/.cache/superpowers/browser-profiles/superpowers-chrome`
   - 20+ additional flags for sandboxing and performance
5. MCP polls `/json/version` every 200ms until Chrome is ready (15s timeout)
6. Chrome meta.json is written with port, PID, profile info
7. Navigation proceeds via CDP

## Available Actions (48+)

| Category | Actions |
|----------|---------|
| Navigation | navigate, back, forward |
| Interaction | click, type, keyboard_press, select, hover, drag_drop, double_click, right_click, file_upload |
| Extraction | extract, attr, screenshot, eval |
| Waiting | await_element, await_text |
| Tab Management | list_tabs, new_tab, close_tab, switch_tab |
| Console | enable_console_logging, get_console_messages, clear_console_messages |
| Chrome Lifecycle | kill_chrome, restart_chrome |
| Viewport | set_viewport, clear_viewport, get_viewport |
| Cookies | clear_cookies |
| Profiles | set_profile, get_profile |

## Test Results

### MCP Server Connection — ✅ Working
- `opencode mcp list` shows `✓ chrome connected`

### Tool Registration — ✅ Working
- `use_browser` registered with 48+ actions

### Help Action — ✅ Working
- `action: "help"` returns complete documentation

### Direct Chromium Test — ✅ Working
- `chromium --headless --no-sandbox --remote-debugging-port=9222 --dump-dom` works
- DevTools endpoint responds on `ws://127.0.0.1:9222/devtools/browser/...`
- DBus errors are harmless warnings (no system bus in container)

### Navigate Action — ✅ Working
- Chrome auto-starts on first navigation action
- Page captured at 780×437 viewport
- Auto-capture creates .html, .md, .png, -console.txt files

### Page Extraction — ✅ Working
- `action: "extract", payload: { format: 'text' }` returns full page text

### Tab Management — ✅ Working
- `action: "list_tabs"` returns tabs with index, id, title, url, type
- Tab state is sticky across actions

### Browser Mode — ✅ Working
- Reports headless mode, PID, port, profile, running status

### Console Logging — ✅ Working as designed
- Captures client-side JS console output (console.log, console.error, etc.)
- Server-side logs are not accessible via CDP

### Screenshots — ✅ Working
- `action: "screenshot"` saves PNG to specified path
- Full-page and viewport screenshots supported

## Known Issues (Resolved)

### Stale Singleton Lock Files (Fixed 2026-08-07)
**Problem**: Chrome crashed on startup with "The profile appears to be in use by another Chromium process" due to stale `SingletonLock` and `SingletonSocket` files in the profile directory.

**Root cause**: When Chrome crashes or is killed unexpectedly, it leaves lock files in the profile directory. The MCP server's auto-started Chrome sees these and refuses to start.

**Fix applied in `chrome-process.js:172-177`**: The MCP server now auto-cleans stale singleton lock files before spawning Chrome. No manual cleanup needed.

**If still needed, manual cleanup**:
```bash
rm -f ~/.cache/superpowers/browser-profiles/*/*/SingletonLock
rm -f ~/.cache/superpowers/browser-profiles/*/*/SingletonSocket
```

### Silent Chrome Crashes (Fixed 2026-06-24)
**Problem**: Chrome stderr was discarded via `stdio: 'ignore'`, making crashes invisible.

**Fix**: stderr is now piped to log files at `~/.cache/superpowers/browser-profiles/{profile}/logs/chrome-*.log` and printed to MCP server stderr.

## Test Script

```bash
node /tmp/chrome-mcp-test.js [url]
```

The test script starts the MCP server, navigates to the URL, takes a screenshot, extracts text, and prints results. It includes auto-cleanup of stale lock files.
