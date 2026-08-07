# Finish Bead Process

**Goal:** Merge, cleanup, close issue

## Steps

1. **Run `finish-bead` from inside your worktree**
   - `finish-bead "Brief description of changes"`
   - This script:
     a. Regenerates `docs/REPO_MAP.md` with current code structure (classes, functions, async defs, module-level constants, and docstring summaries)
     b. Commits all changes in the worktree
     c. Runs pre-merge verification (if hook exists)
     d. Merges the worktree into main
     e. Removes the worktree and deletes its branch

2. **Update bead description**
   - Add merge commit hash to bead description

3. **Close the bead**
   - `bd close <bead-name>`

## Critical Rules

- Always use the `finish-bead` script from inside the worktree — do NOT merge manually
- If verification fails → fix issues and retry, or set `SKIP_VERIFICATION=1` to bypass
- If merge fails → set bead to `Needs_human_input` with merge details and questions
- If tests fail after merge → set bead to `Needs_human_input`
- User is responsible for all remote pushes (agents only perform local commits)

## About REPO_MAP.md

`docs/REPO_MAP.md` is a symbol map of the codebase, auto-generated on every bead close. It lists:
- All classes, functions, and async defs with their file locations
- First-line docstring summaries (when available)
- Module-level constants (ALL_CAPS) and important object assignments

Agents should read this file at the start of a bead to understand the codebase structure quickly.
