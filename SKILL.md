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

## Eval

All evaluation artifacts follow versioned layout under `evals/`:

```
evals/
  v0.1.0/
    inputs/
      session.jsonl       — archived session for trajectory demo
    outputs/
      traj.html           — generated trajectory HTML
      meta-harness-survey.html — unified Meta-Harness feedback survey
```

The human-loop survey covers both skill-level UI/UX and Meta-Harness paradigm assessment. It is archived under `evals/v{version}/outputs/` as a key artifact driving the next iteration.

## Skills

Specialized skills for visualizing Meta-Harness data:

| Skill | Path | Purpose |
|---|---|---|
| **traj-display** | `skills/traj-display/` | Claude Code session trajectory HTML generator — timeline view with TOC, thinking blocks, tool calls |
| **survey** | `skills/survey/` | Feedback survey generator — two types: qa (skill-level UI/UX) and human-loop (Meta-Harness paradigm assessment), archived as eval inputs |
| **metric** | `skills/metric/` | Evaluation metrics dashboard HTML generator — pipeline timing, parse quality, benchmarks |
| **theme** | `skills/theme/` | Theme CSS tokens and visual language for all HTML output |

### Quick Start

```bash
# Generate a trajectory view from a Claude Code session
python skills/traj-display/scripts/generate_traj.py \
  --input ~/.claude/projects/<project>/<session>.jsonl \
  --output traj.html
```

All generated HTML files are self-contained (CSS inline, no build step). Open directly in a browser.
