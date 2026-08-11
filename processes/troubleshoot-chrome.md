# Chrome Troubleshooting

The Chrome MCP server (obra/superpowers-chrome v3.0.2) provides headless browser automation. The server auto-starts Chrome and now includes automatic cleanup of stale lock files, but manual troubleshooting may still be needed in some cases.

## Quick Start (Try This First)

1. **Kill any existing Chrome or MCP processes:**
   ```bash
   pkill -f "node.*superpowers-chrome"
   pkill -f chromium
   ```

2. **Clean stale lock files** (if auto-cleanup didn't work):
   ```bash
   rm -f ~/.cache/superpowers/browser-profiles/*/*/SingletonLock
   rm -f ~/.cache/superpowers/browser-profiles/*/*/SingletonSocket
   ```

3. **Clear entire Chrome profile** (if lock files persist):
   ```bash
   rm -rf ~/.cache/superpowers/browser-profiles/superpowers-chrome/
   ```

4. **Restart the MCP server** (via opencode or test script):
   ```bash
   node /tmp/chrome-mcp-test.js http://localhost:8080
   ```

## How Chrome Actually Starts (IMPORTANT)

The `use_browser` tool is provided by a **stdio MCP server** that opencode spawns
as a child process at session start. The server auto-spawns Chrome itself on the
first `navigate` action — you do **NOT** need to start Chrome manually.

The MCP server entry point (configured in `~/.config/opencode/opencode.json` under `mcp.chrome`):
```json
"mcp": {
  "chrome": {
    "type": "local",
    "command": ["node", "/home/yolo_agent/superpowers-chrome/mcp/dist/index.js", "--headless"],
    "env": {"CHROME_WS_PORT": "9222"}
  }
}
```

### Why `use_browser` is NOT in your tool list

This is the #1 confusion. `use_browser` only appears as an MCP tool if opencode
successfully spawned and connected to the chrome MCP server **at session start**.
If it fails silently (most commonly because Chrome cannot spawn due to stale
profile locks), opencode will not expose `use_browser` for the whole session.

**Root cause chain:**
1. Stale `SingletonLock`/`SingletonSocket` in the Chrome profile directory
2. The MCP server's auto-started Chrome refuses to start ("profile in use")
3. Chrome never reaches port 9222 within the 15s timeout
4. opencode drops the tool → `use_browser` absent from the agent's tool list

**To recover in the CURRENT session** (you cannot retroactively expose the tool):
- Verify the server + Chrome start correctly by driving the MCP server directly
  with node (see "Verify end-to-end" below).
- The fix takes effect on the NEXT opencode session after cleaning the profile.

### Verify the MCP server + Chrome end-to-end with node

This drives the MCP server exactly as opencode would, proving the whole flow
works and spawning Chrome with the correct flags (including `--remote-allow-origins`):

```bash
node /tmp/chrome-mcp-test.mjs   # MCP client that calls use_browser navigate + eval
```

A working minimal MCP client script lives at `/tmp/chrome-mcp-test.mjs` (created
2026-08-10). It spawns the server, initializes the MCP handshake, calls
`use_browser` `navigate`, then `eval` to read page values, and prints results.

### Manual Chrome test (use ONLY to isolate Chrome, not for normal use)

```bash
chromium --remote-debugging-port=9222 --headless=new --no-sandbox \
  --disable-dev-shm-usage --disable-gpu --remote-allow-origins=*
```

> NOTE: The `--remote-allow-origins=*` flag is REQUIRED for any manual CDP
> WebSocket client (curl/websocket-client) to connect; without it you get a
> 403 "Rejected an incoming WebSocket connection" error. The MCP server already
> includes this flag, so do not start Chrome manually for normal operation.

## If Chrome Still Won't Start

### Check for zombie processes:
```bash
ps aux | grep chromium
```

### Check if port 9222 is available:
```bash
lsof -i :9222
curl -s http://localhost:9222/json/version
```

### Verify the MCP server binary exists:
```bash
ls /home/yolo_agent/superpowers-chrome/mcp/dist/index.js
```

### Verify opencode sees the MCP server:
```bash
opencode mcp list    # should show "✓ chrome connected"
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "profile appears to be in use" | Stale SingletonLock/SingletonSocket | Auto-cleaned by MCP; or `rm -f ~/.cache/superpowers/browser-profiles/*/*/Singleton*` |
| "Chrome did not become ready" | Port conflict or crashed Chrome | Kill stale processes, clear profile, retry |
| Chrome starts but no debug port | Missing `--remote-debugging-port` | Ensure args include `--remote-debugging-port=9222` |
| 403 "Rejected an incoming WebSocket connection" | Manual Chrome started without `--remote-allow-origins` | Add `--remote-allow-origins=*`; or let the MCP server spawn Chrome |
| `use_browser` not in tool list | Chrome MCP failed to spawn Chrome at session start (stale locks) | Clean profile (`rm -rf ~/.cache/superpowers/browser-profiles/superpowers-chrome`) then restart opencode |
| DBus warnings | No system bus in container | Harmless, ignore |

## Agent Responsibility

- **Always** verify Chrome functional review completed
- If unavailable, follow the steps above
- Document any new troubleshooting steps found
