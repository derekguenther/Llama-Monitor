# Work Bead Process

**Goal:** Implement changes, create tests, verify success

## Implementation Checklist

### 1. Code Changes
- Work ONLY in worktree directory
- Changes must stay within bead scope
- If work identified outside scope → create new bead (set to Open, do not claim)
- If complications arise → set Needs_human_input with questions in description

### 2. Testing
- Create appropriate tests for changes
- Run all tests
- **All tests must pass** before moving to review

### 3. Verification
- Check for -1 guard values in any numeric display
- **Always** verify Chrome functional review completed
- If unavailable → see [Troubleshoot Chrome](troubleshoot-chrome.md)

### 4. Success Criteria
- Code is correct and complete
- Tests pass
- No -1 guard values
- Chrome functional review completed (see [Troubleshoot Chrome](troubleshoot-chrome.md))

## What to Do

**If successful:**
- Set bead to `Needs_Review`
- Pick next available bead from `bd ready`
- Continue implementation cycle

**If issues arise:**
- Update bead description with findings
- Set appropriate status (Open or Needs_human_input)
- Pick next available bead from `bd ready`


