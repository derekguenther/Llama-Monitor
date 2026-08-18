# Documentation Map

Index of notable documentation files in this project. Load the one you need.

## Root Documents

| File | When to Read | Description |
|------|-------------|-------------|
| `AGENTS.md` | **Start here** — every session | Agent process map: beads workflow, critical guardrails, session completion protocol |
| `DESIGN.md` | Understanding architecture | System design: components, data flow, power calculation strategy, SQLite schema |
| `DEVELOPMENT_ENVIRONMENT.md` | Understanding the dev setup | Multi-host Docker environment: WSL2 container + Windows host, connectivity notes |
| `README.md` | First-time project overview | Project overview: installation, usage, configuration, system requirements |
| `REPO_MAP.md` | Finding code locations | Symbol map: classes, functions, and their file locations across the codebase |
| `CLAUDE.md` | Legacy Claude Code setup | Claude Code agent instructions — leave untouched; kept for potential return to Claude Code |

## Workflow Processes

| File | When to Read | Description |
|------|-------------|-------------|
| `processes/start-bead.md` | Claiming a bead | Steps to claim work atomically and create a worktree |
| `processes/work-bead.md` | Implementing a bead | Development workflow: changes, tests, verification |
| `processes/review-bead.md` | Reviewing completed work | Scope review, code review, functional review (Chrome) |
| `processes/finish-bead.md` | Merging and closing | Merge squash, cleanup worktree, close bead |
| `processes/troubleshoot-chrome.md` | Chrome issues | Troubleshooting stale lock files, zombie processes, port conflicts |

## Memory / Notes

| File | When to Read | Description |
|------|-------------|-------------|
| `memory/MEMORY.md` | Session handoff / context recovery | Persistent AI agent memory: decisions, discoveries, context for next session |
| `memory/database-corruption-hypotheses.md` | Database corruption bugs | Root cause hypotheses for llama-monitor.db corruption issues |
| `memory/database-corruption-fixes.md` | Database corruption fixes | Applied fixes for database corruption |

## Technical Specs

| File | When to Read | Description |
|------|-------------|-------------|
| `docs/specs/` | Before implementing a design decision | Draft specs reviewed by the spec-reviewer agent. Each spec documents a feature before code is written, and is verified against by the code-reviewer agent after implementation. |

## Superpowers / Chrome MCP

| File | When to Read | Description |
|------|-------------|-------------|
| `docs/superpowers/chrome-mcp-usage.md` | Using Chrome MCP | Guide for using the Chrome MCP superpower for browser testing |
| `docs/superpowers/chrome-mcp-findings.md` | Chrome MCP observations | Findings and observations from Chrome MCP usage |
| `docs/superpowers/plans/2026-06-17-lancedb-mcp-server.md` | LanceDB MCP planning | Plan for LanceDB MCP server integration |
