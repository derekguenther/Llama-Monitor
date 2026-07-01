# Agent Process Map

This document defines the workflow for the beads (bd) issue tracking system.

## Workflow Stages

Follow the process documents in sequence. Read the current process document before starting each stage.

1. **[Start Bead](processes/start-bead.md)** → Claim work, create worktree, begin implementation
2. **[Work Bead](processes/work-bead.md)** → Implement changes, create tests, verify success → pick next bead
3. **[Review Bead](processes/review-bead.md)** → Different agent: scope review, code review, functional review
4. **[Finish Bead](processes/finish-bead.md)** → Different agent: merge, cleanup, close issue

## Critical Guardrails

- **Always** read the current process document before proceeding
- **Never** skip verification steps - they exist for a reason
- **Always** check for -1 guard values in any numeric display
- **If stuck or uncertain** → set Needs_human_input immediately, don't guess

**IMPORTANT: Always start the software using llamamonitor.py**
**Never** run individual Python files (web_server.py, aggregator_daemon.py, etc.) directly. This will result in broken behavior.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work atomically
bd close <id>         # Complete work
bd dolt push          # Push beads data to remote (user's responsibility)
```

## Session Completion

When ending a work session, complete all steps:

1. File issues for remaining work
2. Run quality gates (tests, linters, builds)
3. Update issue status (close finished, update in-progress)
4. **PUSH TO REMOTE** - User is responsible for all remote pushes, agents only perform local commits
5. Clean up (clear stashes, prune branches)
6. Verify all changes committed and pushed
7. Provide context for next session

## Chrome Troubleshooting

See [Troubleshoot Chrome](processes/troubleshoot-chrome.md) for Chrome MCP plugin issues.

