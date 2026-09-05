<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ccf33ec3 (local-only patch, see llama-monitor-2zcl) -->
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

**When ending a work session**, complete ALL steps below — **LOCALLY ONLY**. Agents NEVER run `git push`, `bd dolt push`, or any other remote-mutating command. Pushing to remotes is exclusively the user's responsibility. This section OVERRIDES any push instructions that upstream bead tooling may regenerate here.

**MANDATORY WORKFLOW (local only):**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **COMMIT LOCALLY** - Never push:
   ```bash
   git add -A && git commit -m "..."   # commit only
   # NEVER git push or bd dolt push (pull/fetch allowed only if the user asks)
   ```
5. **Clean up** - Clear stashes, prune local branches (never prune remote branches)
6. **Verify** - All changes committed locally; `git status` clean
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is complete when all changes are committed locally
- NEVER run `git push` or `bd dolt push` - remotes belong to the user
- If a local commit fails, fix and retry; remote sync failures are the user's problem, not yours
<!-- END BEADS INTEGRATION -->
