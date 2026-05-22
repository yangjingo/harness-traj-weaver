---
name: harness-traj-weaver
description: Meta-Harness skill — minimal outer loop that gives the proposer unrestricted filesystem access to prior experience. Reason over failed examples and execution traces rather than aggregate scores. Search-set feedback only, never test-set. Self-improving as the underlying agent becomes more capable.
---

# harness-traj-weaver

## Principles

1. **Filesystem as memory** — Full history exposed on disk, no persistent memory mechanism, no fixed scaffold, no archive of prior discoveries.
2. **Trace-level reasoning** — Diagnose raw prior code and execution traces directly, not from compressed per-candidate summaries.
3. **Search-set feedback** — Never expose test-set results. All improvement signals come from the search set only.
4. **Self-improving** — The harness improves automatically as coding agents become more capable.

## Workflow

1. **Observe** — Read prior execution traces and failed examples from the filesystem.
2. **Diagnose** — Selectively inspect raw code and trace data to identify root causes.
3. **Propose** — Generate targeted edits based on trace-level reasoning, not aggregate metrics.
4. **Evaluate** — Validate candidate harnesses against the search set.
5. **Iterate** — Feed results back into the filesystem for the next cycle.

## Filesystem Layout

```
.cache/
  traces/       — execution traces from prior runs
  candidates/   — candidate harness outputs
  feedback/     — search-set evaluation results
```

The outer loop stays minimal. No scaffolding, no memory database — just the filesystem.
