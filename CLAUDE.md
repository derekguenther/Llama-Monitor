## Concurrent Worktree Protocol (CRITICAL)
You must never edit files in the root directory.

**To Start a Bead:**
1. Read the `REPO_MAP.md` file in the root directory to understand the project architecture and locate the functions you need.
2. `git worktree add .worktrees/<task-name> -b <task-name>`
3. `cd .worktrees/<task-name>`
4. Do all your coding inside this folder.

**To Finish a Bead:**
1. From inside your worktree, run: `finish-bead "Brief description of what you did"`
2. Close the bead in the tracker and `/exit`

Never leave a completed worktree behind. Never push to a remote repository.


# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this project.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work (open or in_progress)
bd ready --json       # Find available work as JSON
bd show <id>          # View issue details
bd show <id> --json   # View issue details as JSON
bd update <id> --claim  # Claim work (sets status to in_progress)
bd close <id>         # Complete work
```

### Status Labels (How to Track Work State)

Beads has 5 built-in statuses (`open`, `in_progress`, `blocked`, `closed`, `deferred`). To track additional states like "needs review" or "ready to merge", use **labels**:

| Label | Purpose |
|-------|---------|
| `status:needs-review` | Work is complete but needs review before closing |
| `status:ready-to-merge` | Review complete, ready to merge to main |
| `status:in-worktree` | Currently being implemented in a worktree |

**Status + Label Combinations:**

| Status | Labels | Meaning |
|--------|--------|---------|
| `in_progress` | (none) | Actively working on this |
| `in_progress` | `status:needs-review` | Complete, waiting for review |
| `in_progress` | `status:ready-to-merge` | Review complete, ready to merge |
| `in_progress` | `status:in-worktree` | Currently in a worktree |
| `closed` | (none) | Merged to main - truly done |

**Common Workflows:**

1. **Starting work**: 
   ```bash
   bd update <id> --claim  # status becomes in_progress
   ```

2. **Work complete, needs review**: 
   ```bash
   bd update <id> --add-label status:needs-review
   # Keep status as in_progress (do NOT close yet)
   ```

3. **Review complete, ready to merge**:
   ```bash
   bd update <id> --remove-label status:needs-review --add-label status:ready-to-merge
   # Commit and push changes
   ```

4. **Merged to main**:
   ```bash
   bd update <id> --remove-label status:ready-to-merge
   bd close <id> --reason "Merged to main"
   # Verify git status shows "up to date with origin"
   ```

### Closure Protocol (CRITICAL)

**DO NOT close a bead until the following checklist is complete:**

```
[ ] Code is committed with descriptive message
[ ] Changes are pushed to remote (`git push`)
[ ] Quality gates pass (tests, linters)
[ ] Changes verified on main branch
```

**The bead is NOT complete until `git push` succeeds.** Never stop before pushing - that leaves work stranded locally.

**If a bead is ready for review but not yet complete:**
- Keep it `in_progress` status
- Add label: `bd update <id> --add-label status:needs-review`
- Do NOT close until it's merged

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
- **DO NOT close beads that need review** - use labels instead

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files
- Use **labels** to track work state within `open`/`in_progress` statuses
- Only use `closed` status when work is truly merged and complete

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

### Workflow Best Practices (CRITICAL)

**Beads Must Exist Before Work Starts:**
- Run `bd ready` or `bd ready --json` to find available work
- Run `bd show <id>` to verify a bead exists before starting work
- If a bead doesn't exist, create it with `bd create` first
- NEVER work on non-existent bead IDs

**Workflow Structure for Parallel Work:**
```javascript
export const meta = {
  name: 'fix-webpage-issues',
  description: 'Fix multiple webpage issues following beads process',
  phases: [
    { title: 'Validate', detail: 'Verify beads exist and are ready' },
    { title: 'Implement', detail: 'Work in worktrees with proper labels' },
    { title: 'Review', detail: 'Evaluate and merge with labels' },
  ],
}
```

**Agent Instructions for Bead Work:**
1. Validate bead exists: `bd show <id>`
2. Claim work: `bd update <id> --claim`
3. Set label: `bd update <id> --add-label status:in-worktree`
4. Create worktree: `git worktree add .worktrees/<id> -b <id>`
5. Implement fix with tests
6. Set review label: `bd update <id> --add-label status:needs-review`
7. Do NOT close - wait for review agent

**Review Agent Instructions:**
1. Check bead has `status:needs-review` label
2. Run tests: `python3 -m pytest`
3. Merge branch to main: `git merge <branch> --no-ff`
4. Push: `git push`
5. Remove review label: `bd update <id> --remove-label status:needs-review --add-label status:ready-to-merge`
6. Close: `bd close <id> --reason "Merged to main"`
<!-- END BEADS INTEGRATION -->


## Build & Test

_Add your build and test commands here_

```bash
# Example:
# npm install
# npm test
```

## Architecture Overview

_Add a brief overview of your project architecture_

## Conventions & Patterns

_Add your project-specific conventions here_
