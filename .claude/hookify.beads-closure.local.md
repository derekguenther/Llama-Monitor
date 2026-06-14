---
name: remind-bead-closure-protocol
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: \bbd\s+close\b
---

**⚠️ Bead Closure Protocol Reminder**

Before closing a bead, please verify the following checklist is complete:

```
[ ] Code is committed with descriptive message
[ ] Changes are pushed to remote (`git push`)
[ ] Quality gates pass (tests, linters)
[ ] Changes verified on main branch
```

**If this bead is NOT ready to be closed (still in progress):**
- Keep it `in_progress` and continue working
- Or use `bd defer <id> --until="date"` to defer work

**If this bead IS complete but needs review:**
- Add label: `bd update <id> --add-label status:needs-review`
- **DO NOT close yet** - keep status as `in_progress`
- After review and merge, then close with `bd close <id> --reason "Merged to main"`

**If this bead is ready to merge (review complete):**
- Add label: `bd update <id> --add-label status:ready-to-merge`
- Commit and push changes
- After merge, close with `bd close <id> --reason "Merged to main"`

**Only close a bead when:**
- All work is complete and verified
- Code has been committed and pushed
- Tests have passed
- The change is merged to main

**DO NOT close a bead until `git push` succeeds.**

**Remember:**
- `in_progress` + `status:needs-review` = complete, waiting for review (keep open)
- `in_progress` + `status:ready-to-merge` = review done, ready to merge (keep open)
- `closed` = truly done, merged to main
