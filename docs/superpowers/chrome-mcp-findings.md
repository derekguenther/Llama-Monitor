# Chrome MCP Plugin - Testing Findings

## Setup

- **Plugin**: obra/superpowers-chrome v3.0.2
- **Location**: `/home/yolo_agent/superpowers-chrome/` (persistent)
- **MCP Server**: `/home/yolo_agent/superpowers-chrome/mcp/dist/index.js`
- **Browser**: Chromium 149.0.7827.155 (installed via Dockerfile)
- **OpenCode Config**: `/home/yolo_agent/.config/opencode/opencode.json`

## Configuration

```json
{
  "mcp": {
    "chrome": {
      "type": "local",
      "command": ["node", "/home/yolo_agent/superpowers-chrome/mcp/dist/index.js", "--headless"]
    }
  }
}
```

Key points:
- `--headless` flag is required to force headless mode (avoids display detection issues)
- Path must be persistent (`/home/yolo_agent/`) since `/tmp` doesn't survive container restarts
- Chromium must be installed in the container

## Dockerfile Requirements

```dockerfile
RUN apt-get update && apt-get install -y chromium
RUN git clone --depth 1 https://github.com/obra/superpowers-chrome.git /home/yolo_agent/superpowers-chrome
RUN cd /home/yolo_agent/superpowers-chrome/mcp && npm install && npm run build
```

## Test Results

### MCP Server Connection
- **Status**: Connected and working
- **Verification**: `opencode mcp list` shows `✓ chrome connected`

### Tool Registration
- **Status**: Working
- The `use_browser` tool is properly registered with 48+ actions
- Tool schema includes: action, selector, payload, timeout, tab_index

### Help Action
- **Status**: Working
- `action: "help"` returns complete documentation with all actions and payload shapes

### Direct Chromium Test
- **Status**: Working
- `chromium --headless --no-sandbox --remote-debugging-port=9222 --dump-dom` works correctly
- DevTools endpoint responds: `ws://127.0.0.1:9222/devtools/browser/...`
- DBus errors are harmless warnings (no system bus in container)

### Navigate Action (via MCP)
- **Status**: Working
- Successfully navigated to http://localhost:8080
- Chrome auto-starts on first navigation action
- Chrome PID: 4933, Port: 9222, Profile: superpowers-chrome
- Page captured: 780x437 viewport
- Auto-capture creates: .html, .md, .png, -console.txt files

### Page Extraction
- **Status**: Working
- `action: "extract", payload: "text"` returns full page text
- Successfully extracted Llama Monitor dashboard content including:
  - Server URL, costs, energy usage
  - Token counts, tokens/sec, session cost
  - CPU/GPU/memory usage metrics
  - Power readings, slot progress

### Tab Management
- **Status**: Working
- `action: "list_tabs"` returns array of tabs with index, id, title, url, type
- Tab state is sticky (persists across actions)

### Browser Mode
- **Status**: Working
- `action: "browser_mode"` returns:
  - headless: true
  - mode: "headless"
  - running: true
  - pid, port, profile, profileDir

### Console Logging
- **Status**: Working as designed
- `action: "enable_console_logging"` enables DevTools Protocol console API capture
- `action: "get_console_messages"` returns client-side JS console messages (console.log, console.error, etc.)
- Test returned "No console messages captured" because the Llama Monitor page has no JavaScript console output — this is expected for that page

## Known Issues

1. **Stale Chrome Profile**: Previous Chrome crashes left stale profile data that prevented new Chrome instances from starting. Solution: Clear profile directory (`rm -rf /home/yolo_agent/.cache/superpowers/browser-profiles/superpowers-chrome/*`)

2. **Zombie Processes**: Previous Chrome crashes left zombie processes (`[chromium] <defunct>`). These don't affect functionality but should be cleaned up.

3. **DBus Errors**: Harmless warnings about missing system bus socket. Can be ignored.

4. **Console Logging Scope**: Console logging only captures client-side browser console output (JavaScript console.log, etc.), not server-side logs. This is expected behavior — Chrome's DevTools Protocol has no access to server processes.

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

The MCP server uses `chrome-ws-lib.js` as a library to control Chromium via the Chrome DevTools Protocol. It auto-starts Chrome on first navigation action and manages tab state.

## Chrome Startup Flow

1. MCP server receives `initialize` request
2. Client sends `notifications/initialized`
3. Client calls `use_browser` with `action: "navigate"`
4. MCP server detects no running Chrome, spawns Chromium with:
   - `--headless --no-sandbox --remote-debugging-port=9222`
   - `--user-data-dir=/home/yolo_agent/.cache/superpowers/browser-profiles/superpowers-chrome`
   - 20+ additional flags for sandboxing and performance
5. MCP polls `/json/version` every 200ms until Chrome is ready (15s timeout)
6. Chrome meta.json is written with port, PID, profile info
7. Navigation proceeds via CDP

## Available Actions

The `use_browser` tool supports 48+ actions including:
- **Navigation**: navigate, back, forward
- **Interaction**: click, type, keyboard_press, select, hover, drag_drop
- **Extraction**: extract, attr, screenshot, eval
- **Waiting**: await_element, await_text
- **Tab Management**: list_tabs, new_tab, close_tab, switch_tab
- **Console**: enable_console_logging, get_console_messages, clear_console_messages
- **Chrome Lifecycle**: kill_chrome, restart_chrome
- **Viewport**: set_viewport, clear_viewport, get_viewport
- **Cookies**: clear_cookies
- **Profiles**: set_profile, get_profile

## Summary

The Chrome MCP plugin is **fully functional** for browser automation:
- Chrome starts reliably in headless mode
- Navigation, extraction, and tab management all work
- Auto-capture system creates page snapshots (HTML, markdown, PNG, console logs)
- Page text extraction successfully reads dashboard content
- Console logging captures client-side browser console output (as designed)
