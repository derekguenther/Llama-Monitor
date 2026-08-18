# Review Bead Process

**Goal:** Scope review, code review, functional review

**Important:** This is performed by a DIFFERENT agent than the implementer. The implementing agent should pick up a new bead and continue working.

## Steps

1. **Find a Needs_Review bead**
   ```bash
   bd ready
   ```
   Look for beads with status `Needs_Review`

2. **Scope review**
   - Did work stay within bounds?
   - Check bead description against actual changes
   - If scope violated → set bead to `Open` with findings

3. **Code review**
   - Review `git diff --stat main...<bead-name>` for compact file change summary
   - Show diffs only for changed files
   - Diff against version of main the worktree was based off (not current main)
   - Check for correctness and completeness
   - If issues found → set bead to `Open` with findings

4. **Functional review**
   - Start main.py from within worktree
   - Test with Chrome superpower
   - If Chrome unavailable → see [Troubleshoot Chrome](troubleshoot-chrome.md)
   - If issues found → set bead to `Open` with findings

### When Chrome functional review is required

Chrome functional review is **always** required when a bead changes the webpage or the data flow that feeds it (HTML/templates, JS, API endpoints, metrics aggregation that reaches the dashboard). For these, do not skip Chrome testing.

Chrome functional review may be **skipped** only for changes with no visible component — e.g. pure logging changes, config files that do not affect data flow, or backend-only fixes with no UI/dashboard impact. When skipping, note the skip reason in the review outcome.

When in doubt, run the Chrome functional review — do not skip it.

## Outcomes

**If review fails:**
- Set bead to `Open` with detailed findings in description
- Implementer will fix and resubmit

**If review passes:**
- Proceed to [Finish Bead](finish-bead.md) process

## Critical Guardrails

- **Always** verify Chrome functional review completed for webpage/data-flow changes - if unavailable, troubleshoot harder (see [Troubleshoot Chrome](troubleshoot-chrome.md))
- Never skip test verification
- **Never silently skip Chrome functional review** (only skip for logging/config changes with no visible component, and note the skip reason)
- Always check for -1 values in numeric displays
- If uncertain → set Needs_human_input, don't guess
