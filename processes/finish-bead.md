# Finish Bead Process

**Goal:** Merge, cleanup, close issue

## Steps

1. **Merge the worktree**
   - `git checkout main`
   - `git merge --squash <bead-name>`
   - `git commit -m "Close <bead-name>: <brief description>"`
   - Run tests to verify nothing broke

2. **Update bead description**
   - Add merge commit hash to bead description

3. **Delete worktree**
   - `git worktree remove .worktrees/<bead-name>`

4. **Close the bead**
   - `bd close <bead-name>`

## Critical Rules

- Run merge steps separately (do NOT string together with &&)
- If merge fails → set bead to `Needs_human_input` with merge details and questions
- If tests fail after merge → set bead to `Needs_human_input`
- User is responsible for all remote pushes (agents only perform local commits)
