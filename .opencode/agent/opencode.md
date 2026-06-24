---
description: Default opencode agent with Beads worktree protocol enforcement.
---

## Beads Worktree Protocol (MANDATORY)

When working on beads, you MUST follow CLAUDE.md's Implementation Process:

1. **NEVER edit files in the root directory.** All changes go in worktrees only.
2. **Create a worktree before any bead work:**
   `git worktree add .worktrees/<bead-name> -b <bead-name>`
3. **Work inside the worktree.** Changes only in `.worktrees/<bead-name>/`.
4. **If work identified outside scope** → create new bead, do not stray.
5. **Before marking a bead Needs_Review**, all tests must pass.
6. **Review process:**
   - Scope review → Code review → Functional review with Chrome
   - Pass → merge, delete worktree, close bead
   - Fail → set Open with findings
7. **Read CLAUDE.md for details.**

**This protocol is non-negotiable. Never work on main directly for bead tasks.**
