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

## File Reading Rules

- **Always** use an offset when using the "read" command on a file to avoid looping and ensure you're reading the correct section

**IMPORTANT: Always check if Llama Monitor is running before attempting to start it**
**IMPORTANT: Always start the software using llamamonitor.py**
**Never** run individual Python files (web_server.py, aggregator_daemon.py, etc.) directly. This will result in broken behavior.

## Documentation

See [Documentation Map](docs/DOCUMENTATION_MAP.md) for the full index of project documentation files.

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

**IMPORTANT: Always read [Troubleshoot Chrome](processes/troubleshoot-chrome.md) before attempting to use Chrome.** This guide contains essential steps for starting Chrome, including cleaning stale lock files and killing zombie processes. Do not attempt to use Chrome without first reading and following this guide.


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ccf33ec3 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
