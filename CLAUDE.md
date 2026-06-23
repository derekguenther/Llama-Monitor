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

## Implementation Process

1) Claim an Open bead → In Progress
2) Review for completeness: If gaps → set Needs_human_input, consolidate questions in description, pick next Open bead
3) Create worktree: `git worktree add .worktrees/<bead-name> -b <bead-name>`
4) Work the bead
   a) Changes ONLY in worktree
   b) Work identified outside scope → create new bead (set to Open, do not claim), continue in-scope work
   c) Complications → set Needs_human_input with questions in description, pick next Open bead
   d) Create appropriate tests and run them — all tests must pass before marking Needs_Review
   e) Success → set Needs_Review
5) Repeat until no Open beads remain → print summary, start Review Process

## Review Process

1) Find a Needs_Review bead
2) Scope review — did work stay within bounds?
3) Code review — correct and complete?
   - First: `git diff --stat main...<bead-name>` for compact file change summary
   - Then show diffs only for changed files (not full diff output)
   - Diff against the version of main the worktree was based off of (not current main)
4) Functional review — start main.py from within worktree, test with chrome superpower
   - **IF CHROME IS NOT AVAILABLE**: set bead to Needs_human_input with question "Chrome unavailable for functional review. Proceed with code review + tests only, or fix Chrome first?" Do NOT skip functional review silently.
5a) Fail → set Open with findings in description
5b) Pass → merge, delete worktree, close bead with findings

### Merge Steps (Review 5b)
Run each step separately — do NOT string together with &&:
1. `git checkout main`
2. `git merge --squash <bead-name>` — if this fails, do NOT close the bead; set Needs_human_input with merge details and questions
3. `git commit -m "Close <bead-name>: <brief description>"`
4. Run tests to verify nothing broke — if they fail, set Needs_human_input
5. Update bead description with merge commit hash
6. `git worktree remove .worktrees/<bead-name>`
7. `bd close <bead-name>`
8. Repeat until no Needs_Review beads remain → print summary, signal idle

### General Rules
- When the process says "repeat", repeat without asking — keep working through the queue
- If uncertainties or questions at any point → update bead with questions, move on, consolidate for user discussion
- Never make changes not directly related to current bead description
- **NEVER silently skip a required process step** — if you can't complete a step (e.g., Chrome unavailable, tests failing), set Needs_human_input and ask
