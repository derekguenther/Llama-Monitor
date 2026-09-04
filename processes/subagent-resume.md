# Subagent Session Resume Process

**Goal:** Ensure no subagent work is lost when llama.cpp closes or a subagent is interrupted mid-task (e.g. during spec review or code review).

**Scope:** Applies whenever a subagent is dispatched via the Task tool and may be interrupted by model-load failure, slot contention, or llama.cpp restart. See bead `llama-monitor-19q6` for the originating discussion and design rationale.

## Principles

1. **Session context is the primary source of truth.** A subagent's messages + tool outputs hold the work. Preserve it and resume it; only rebuild when truly lost.
2. **Dependencies are disposable and self-healing.** Chrome and Llama Monitor must never be treated as fatal if lost — a subagent can restart them.
3. **Never lose progress.** Every meaningful milestone is checkpointed so a fresh or resumed session can continue, not restart.

## Four Pillars

### 1. Resume via `task_id` (primary)

- The main agent is **blocked** after dispatching a review subagent, so it reliably knows at most one review subagent is running at any moment it isn't itself executing.
- When the main agent resumes and finds a subagent returned **no result**, it should:
  1. **Verify** the subagent truly stalled (it did not complete; not merely still running).
  2. **Resume** the session by passing the subagent's `task_id` to the Task tool, which continues with its previous messages and tool outputs.
- Resume is **autonomous** — there is nothing user-only in it. Do not prompt the user; continue once the stall is verified.
- Do **not** eagerly tear down Chrome / Llama Monitor on interruption. Keep dependencies alive so a resumed session finds them intact.

### 2. Checkpoint progress (safety net)

Written when session-resume itself is impossible (process death, lost context). The subagent appends a structured checkpoint to a **bead note** at each milestone (end of each review section), not on every tool call.

Checkpoint sections (parseable, so resume is deterministic and idempotent):

```
Status    - what is done / in-progress / not-started per review stage
Findings  - issues found so far, each with a STABLE ID (so resume does not re-report duplicates)
Pending   - explicitly what remains, with any partial reasoning
Artifacts - paths to partial outputs and dependency state (which Chrome/llamamonitor were in play)
Verdict   - running draft conclusion
```

Stable IDs for findings are the key to idempotent resume: a resumed subagent can tell "already found #3, continue from #4".

### 3. Pre-flight dispatch guard

- **Serialize review subagents** (at most one at a time). The blocking model gives a reliable count (≤ 1); parallel dispatch is what caused over-subscription and the "dispatched 2 more" failure mode.
- Before the main agent's own next operation, **poll llama.cpp `/slots`** for free capacity.
- Do **not** attempt to count running subagents via the OS or an OpenCode API — subagents are child sessions (not separate processes), no such API exists, and llamamonitor-instance counting is unreliable (only present late in code review, absent in spec review).

### 4. Self-healing dependencies

- At work-start, a subagent verifies Chrome and Llama Monitor are alive and **restarts them if missing**, rather than treating loss as fatal.
- Each review subagent owns its own Llama Monitor instance (see `review-bead.md` port allocation); no shared state to conflict on.

## Checklist

- [ ] Subagent writes a structured checkpoint bead note at each milestone.
- [ ] Main agent detects a stalled subagent (resumed with no result), verifies, and resumes via `task_id`.
- [ ] Review subagents are dispatched serially (≤ 1 running).
- [ ] llama.cpp `/slots` is polled before the main agent's next operation.
- [ ] Subagent self-heals lost Chrome / Llama Monitor instead of treating loss as fatal.
- [ ] No eager teardown of Chrome / Llama Monitor on interruption.
