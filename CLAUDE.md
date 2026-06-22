## Concurrent Worktree Protocol (CRITICAL)
You must never edit files in the root directory.

**To Start a Bead:**
1. Read `REPO_MAP.md` to understand architecture and locate functions.
2. `git worktree add .worktrees/<task-name> -b <task-name>`
3. `cd .worktrees/<task-name>`
4. Code inside this folder only.

**To Finish a Bead:**
1. From inside your worktree: `finish-bead "Brief description of what you did"`
2. Close the bead in the tracker and `/exit`

**CRITICAL: Worktree Merge Protocol**
- Worktrees are NEVER merged automatically.
- User must review and explicitly approve merge before any merge operation.
- Worktree remains in place for user review after finishing.
- Never push to a remote repository.

# Project Instructions for AI Agents

This file provides instructions for AI coding agents working on this project.

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

## Build & Test
```bash
# Example:
# npm install
# npm test
```

## Docker Development Notes

When connecting to services on the Windows host (like Llama Monitor or Chrome for debugging), use `host.docker.internal` instead of `127.0.0.1` or `localhost`.

## Architecture Overview

_Add a brief overview of your project architecture_

## Conventions & Patterns

_Add your project-specific conventions here_

## Git Operations Checklist (CRITICAL)

Before ANY git operation, run this checklist:

### BEFORE ANY GIT OPERATION:
1. What files does this operation affect?
2. What changes exist in those files right now?
3. What does the other branch/commit actually change?
4. Are these changes compatible or conflicting?
5. What is the MINIMUM safe action here?
6. Is it potentially destructive in any way? Get permission from user.

### FOR MERGES SPECIFICALLY:
1. `git diff base..feature -- file` for each modified file.
2. Read actual code changes, not just commit messages.
3. Identify conflicts BEFORE attempting merge.
4. If conflicts exist: decide to stash, rebase, or resolve.

### BEFORE DELETIONS:
1. Is it a completed worktree which has been merged? Safe to delete.
2. Is it a worktree of unknown status? NOT safe to delete — ask user for guidance.
3. All other deletions: Get permission from user.
