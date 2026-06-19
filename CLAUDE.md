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

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:970c3bf2 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` for full context.

### Quick Reference
```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules
- Use `bd` for ALL task tracking — no TodoWrite, TaskCreate, or markdown TODO lists.
- Use `bd remember` for persistent knowledge — no MEMORY.md files.

**Architecture:** Issues live in a local Dolt DB; sync uses `refs/dolt/data` on git remote; `.beads/issues.jsonl` is a passive export.

## Agent Context Profiles

- **Conservative (default)**: Use `bd` for task tracking. No git commits/pushes/sync unless asked. Perform initial review (code completeness, adherence to bead instructions) at handoff. Report changed files, validation, and suggested commands. Worktree merge requires user approval.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`. Same conservative git policy unless active instructions say otherwise. Perform initial review before handoff.
- **Team-maintainer**: Only when repository explicitly opts in. May close beads, run quality gates, commit, and push. "Do not commit/push" instructions still win. Worktree merge requires user approval unless explicitly waived.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, or orchestrator instructions.

### Pre-Handoff Checklist (Your Responsibility)
1. **Code completeness** — Does implementation look complete?
2. **Adherence to bead instructions** — Has work strayed from original requirements?
3. **Quality gates** — Run tests, linters, builds if relevant.

### Handoff Protocol
1. **File issues for remaining work** — Create beads for follow-up items.
2. **Run quality gates** (if code changed) — Tests, linters, builds.
3. **Update issue status** — Mark finished work complete (do NOT close bead yet).
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   bd dolt push
   git push
   git status
   ```
5. **Hand off to user** — Summarize changes, validation, issue status, and any blocked sync/commit/push step.

### User Review & Merge Protocol
- User reviews worktree changes before merge.
- Worktree is NEVER merged without explicit user approval.
- After finishing a bead, worktree remains in place for user review.
- User must explicitly approve merge before any merge operation occurs.

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from active profile or current request.
- If sync/push is blocked, stop and report the exact command and error.
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
