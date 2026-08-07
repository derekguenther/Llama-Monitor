# Chrome MCP Superpower — Usage Guide

The Chrome MCP server (obra/superpowers-chrome v3.0.2) provides headless browser automation for functional review, visual inspection, and page content extraction.

## Quick Start

The Chrome MCP server is configured and connected in opencode (`opencode mcp list` shows `✓ chrome connected`). Use the `use_browser` tool with actions like `navigate`, `screenshot`, and `extract`.

If opencode does not expose the MCP tool directly, invoke the server via a Node.js script:

```bash
node /tmp/chrome-mcp-test.js http://example.com
```

This script navigates to the URL, takes a screenshot, extracts page text, and prints results. It also auto-cleans stale lock files before starting.

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

Every DOM action (navigate, click, type, eval) auto-captures to a session directory:

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
