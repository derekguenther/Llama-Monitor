# Chrome Troubleshooting

**Important:** This is a living document. The Chrome MCP plugin has been unreliable and requires troubleshooting. Agents should persistently try different combinations of commands until Chrome is running.

## Quick Start (Try This First)

1. **Clean up stale lock files:**
   ```bash
   rm -f /home/yolo_agent/.cache/superpowers/browser-profiles/*/*/SingletonLock
   rm -f /home/yolo_agent/.cache/superpowers/browser-profiles/*/*/SingletonSocket
   ```

2. **Kill any existing Chrome processes:**
   ```bash
   pkill -f chrome
   ```

3. **Start Chrome manually on port 9222:**
   ```bash
   chromium --remote-debugging-port=9222 --no-first-run --no-default-browser-check --disable-gpu --headless=new --no-sandbox --disable-dev-shm-usage --disable-extensions --disable-background-networking --disable-sync --disable-translate --metrics-recording-only --safebrowsing-disable-auto-update
   ```

4. **Verify Chrome is running:**
   ```bash
   curl -s http://localhost:9222/json/version
   ```

## If Chrome Still Won't Start

### Check for zombie processes:
```bash
ps aux | grep chromium
```

### Clear entire Chrome profile:
```bash
rm -rf /home/yolo_agent/.cache/superpowers/browser-profiles/*/
```

### Try different Chrome flags:
```bash
chromium --remote-debugging-port=9222 --no-sandbox --headless --disable-dev-shm-usage
```

### Check if port 9222 is actually available:
```bash
lsof -i :9222
netstat -tlnp | grep 9222
```

## Agent Responsibility

- **Always** verify Chrome functional review completed
- If unavailable, **troubleshoot harder** - try different combinations of commands
- This is a finicky plugin - persistence is required
- Document any new troubleshooting steps that work
