# Chrome MCP Superpower — Usage Guide

The Chrome MCP server (obra/superpowers-chrome) provides headless browser automation for functional review, visual inspection, and page content extraction.

## Important: opencode Does Not Expose MCP Tools to Agents

The Chrome MCP server is configured and connected in opencode (`opencode mcp list` shows `✓ chrome connected`), but opencode does not expose MCP tools (like `use_browser`) to agents in the current session. The tools are added at runtime during session processing, but they are not available in the agent's static tool list.

**Workaround:** Invoke the Chrome MCP server directly via its stdio protocol using a Node.js script. This is fully functional and gives you the same capabilities.

## Quick Start

Run a Node.js script that communicates with the MCP server over stdio:

```bash
node -e "
const { spawn } = require('child_process');
const proc = spawn('node', ['/home/yolo_agent/superpowers-chrome/mcp/dist/index.js', '--headless'], { stdio: ['pipe','pipe','pipe'] });
let id = 1;
const responses = [];
proc.stdout.on('data', d => { for (const line of d.toString().trim().split('\n')) { if (line.trim()) try { responses.push(JSON.parse(line)); } catch {} } });
proc.stderr.on('data', () => {});
proc.on('error', e => console.error(e.message));
function send(m, p, i) { proc.stdin.write(JSON.stringify({jsonrpc:'2.0',id:i??id++,method:m,params:p||{}})+'\n'); }
setTimeout(()=>{ send('initialize',{protocolVersion:'2024-11-05',capabilities:{tools:{}},clientInfo:{name:'invoker',version:'1.0'}},1); },500);
setTimeout(()=>{ send('tools/list',{}); },3000);
setTimeout(()=>{ send('tools/call',{name:'use_browser',arguments:{action:'navigate',selector:null,payload:'http://example.com'}}); },5000);
setTimeout(()=>{ send('tools/call',{name:'use_browser',arguments:{action:'extract',selector:null,payload:{format:'text'}}}); },12000);
setTimeout(()=>{
  for (const r of responses) {
    if (r.result?.content) for (const c of r.result.content) { if (c.type==='text') console.log(c.text); }
  }
  proc.kill('SIGTERM'); process.exit(0);
}, 18000);
"
```

This navigates to the URL, extracts the page text, and prints it to stdout.

## Reusable Template

Save this as a script for repeated use:

```javascript
// chrome-mcp.js — Invoke Chrome MCP server directly
const { spawn } = require('child_process');

const proc = spawn('node', [
  '/home/yolo_agent/superpowers-chrome/mcp/dist/index.js',
  '--headless'
], { stdio: ['pipe', 'pipe', 'pipe'] });

let id = 1;
const responses = [];
proc.stdout.on('data', d => {
  for (const line of d.toString().trim().split('\n')) {
    if (line.trim()) try { responses.push(JSON.parse(line)); } catch {}
  }
});
proc.stderr.on('data', () => {}); // ignore dbus/GPU noise

function send(method, params, messageId) {
  proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: messageId ?? id++, method, params: params || {} }) + '\n');
}

// Initialize
setTimeout(() => send('initialize', { protocolVersion: '2024-11-05', capabilities: { tools: {} }, clientInfo: { name: 'invoker', version: '1.0' } }, 1), 500);

// List tools (optional, for verification)
setTimeout(() => send('tools/list', {}), 3000);

// Navigate
setTimeout(() => send('tools/call', { name: 'use_browser', arguments: { action: 'navigate', selector: null, payload: process.argv[2] || 'http://example.com' } }), 5000);

// Extract page text
setTimeout(() => send('tools/call', { name: 'use_browser', arguments: { action: 'extract', selector: null, payload: { format: 'text' } } }), 12000);

// Print results
setTimeout(() => {
  for (const r of responses) {
    if (r.result?.content) for (const c of r.result.content) { if (c.type === 'text') console.log(c.text); }
  }
  proc.kill('SIGTERM');
  process.exit(0);
}, 18000);
```

Usage: `node chrome-mcp.js http://example.com`

## Key Actions

| Action | Selector | Payload | Description |
|--------|----------|---------|-------------|
| `navigate` | null | URL string | Navigate to a page |
| `extract` | null | `{ format: 'text' }` | Extract page text |
| `extract` | null | `{ format: 'html' }` | Extract raw HTML |
| `extract` | null | `{ format: 'markdown' }` | Extract as markdown |
| `screenshot` | null | `{ path: 'file.png', fullpage: false }` | Take a screenshot |
| `click` | CSS selector | null | Click an element |
| `type` | CSS selector | text string | Type into an input |
| `eval` | null | JS code string | Execute JavaScript |
| `list_tabs` | null | null | List open tabs |
| `browser_mode` | null | null | Get browser status |

## Auto-Captured Files

Every DOM action (navigate, click, type, eval) auto-captures to the session directory:

- `{prefix}.png` — viewport screenshot (780×437)
- `{prefix}.md` — page content as structured markdown
- `{prefix}.html` — full rendered DOM
- `{prefix}-console.txt` — browser console messages

The session directory is printed in the navigate response, e.g.:
```
Session dir: /home/yolo_agent/.cache/superpowers/browser/2026-07-05/session-1783240931426
Files: 001-navigate.html, 001-navigate.md, 001-navigate.png, 001-navigate-console.txt
```

## Troubleshooting

See [Troubleshoot Chrome](../../processes/troubleshoot-chrome.md) for stale lock files, zombie processes, and port conflicts.

See [Chrome MCP Findings](chrome-mcp-findings.md) for detailed architecture, known issues, and debugging procedures.
