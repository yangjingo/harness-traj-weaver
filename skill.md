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
.metaharness/
  v{version}/
    inputs/              — QA answers (qa-survey-*.json/txt), session JSONL
    outputs/             — traj-*.html, commit-*.json, plan-v{next}.json
  plan-trigger.json      — written by post-commit to trigger the next iteration cycle
  qa-state.json          — human-loop QA interrupt/resume state
```

The outer loop stays minimal. No scaffolding, no memory database — just the filesystem. Each version directory accumulates all harness artifacts for that release.

## Hook Integration

### Commit Hook (`pre-commit`)

```
git commit
    │
    ▼
pre-commit hook → skill triggered → Observe → Diagnose → Propose → Evaluate
    │
    ├── traj generated (session trajectory HTML)
    ├── human-loop QA starts in terminal (AskUserQuestion)
    │     ├── entry gate: "现在评估 / 稍后 / 跳过?"
    │     ├── mode: quick (8q) / full (27q)
    │     └── section-by-section A→B→C→D→E→F→G
    ├── answers archived → .metaharness/v{version}/inputs/
    └── plan generated → .metaharness/v{version}/plan-v{next}.json
```

Terminal AUQ replaced browser-based gating in v0.3.0. The human answers Claude's
questions directly in the terminal — no browser, no HTML form, no context switch.

### Push Hook (`pre-push`)

Same terminal QA flow for `git push`. Session archived, human-loop runs, plan updated.

### Post-Commit

After commit lands, `post-commit` hook archives the session JSONL to
`.metaharness/v{version}/inputs/` and writes `.metaharness/plan-trigger.json`
to signal readiness for the next iteration.

### Installation

The skill ships with an install script. After cloning, run once to set up both the skill and hooks:

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git ~/.claude/skills/harness-traj-weaver
bash ~/.claude/skills/harness-traj-weaver/scripts/install.sh
```

`install.sh` does two things:
1. Registers the skill in `~/.claude/settings.json`
2. Installs `hooks/pre-commit`, `hooks/post-commit`, and `hooks/pre-push` into `.git/hooks/` of the current repo

For manual hook installation in an existing repo:

```bash
cp ~/.claude/skills/harness-traj-weaver/hooks/pre-commit .git/hooks/pre-commit
cp ~/.claude/skills/harness-traj-weaver/hooks/post-commit .git/hooks/post-commit
cp ~/.claude/skills/harness-traj-weaver/hooks/pre-push .git/hooks/pre-push
```
