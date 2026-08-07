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

### Start Chrome manually to test:
```bash
chromium --remote-debugging-port=9222 --headless=new --no-sandbox --disable-dev-shm-usage --disable-gpu
```

### Verify the MCP server binary exists:
```bash
ls /home/yolo_agent/superpowers-chrome/mcp/dist/index.js
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "profile appears to be in use" | Stale SingletonLock/SingletonSocket | Auto-cleaned by MCP; or `rm -f ~/.cache/superpowers/browser-profiles/*/*/Singleton*` |
| "Chrome did not become ready" | Port conflict or crashed Chrome | Kill stale processes, clear profile, retry |
| Chrome starts but no debug port | Missing `--remote-debugging-port` | Ensure args include `--remote-debugging-port=9222` |
| DBus warnings | No system bus in container | Harmless, ignore |

## Agent Responsibility

- **Always** verify Chrome functional review completed
- If unavailable, follow the steps above
- Document any new troubleshooting steps found
