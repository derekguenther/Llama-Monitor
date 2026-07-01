# Start Bead Process

**Goal:** Claim work, create worktree, begin implementation

## Steps

1. **Find available work**
   ```bash
   bd ready
   ```

2. **Review the issue**
   ```bash
   bd show <id>
   ```
   Check for completeness. If gaps exist:
   - Set bead to `Needs_human_input`
   - Consolidate questions in description
   - Pick next available bead

3. **Claim the work atomically**
   ```bash
   bd update <id> --claim
   ```

4. **Create worktree**
   ```bash
   git worktree add .worktrees/<bead-name> -b <bead-name>
   cd .worktrees/<bead-name>
   ```



## Next Step

When the bead is properly set up per the above list → begin implementation and proceed to [Work Bead](work-bead.md)
