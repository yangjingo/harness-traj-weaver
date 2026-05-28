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
  traces/       — execution traces from prior runs
  candidates/   — candidate harness outputs
  feedback/     — search-set evaluation results
```

The outer loop stays minimal. No scaffolding, no memory database — just the filesystem.

## Eval

All evaluation artifacts follow versioned layout under `.metaharness/`:

```
.metaharness/
  v0.1.0/
    outputs/
      traj.html       — baseline trajectory
      survey.html     — baseline survey
  v0.2.0/
    outputs/
      traj-79283bb1.html  — session trajectory
```

The human-loop survey covers both skill-level UI/UX and Meta-Harness paradigm assessment. It is archived under `.metaharness/v{version}/outputs/` as a key artifact driving the next iteration.

## Hook Integration

This skill is designed to be triggered by git hooks — not run standalone scripts. Hooks invoke the skill, which then runs the full Observe→Diagnose→Propose→Evaluate loop.

### Commit Hook (`pre-commit`)

```
git commit
    │
    ▼
hook fires → skill triggered → Observe → Diagnose → Propose → Evaluate
    │                                                              │
    │         human-loop.html opened in browser ◄──────────────────┘
    │
    ├── Human clicks "GO"  → commit proceeds
    └── Human clicks "NO-GO" → commit blocked
```

The skill generates the review, but the HUMAN gates the commit. Each commit auto-archives the current session via `$CLAUDE_CODE_SESSION_ID` into `.metaharness/v{version}/inputs/session-{id}.jsonl`. Version is detected from the latest entry in `changelog.md`.

### Push Hook (`pre-push`)

Same human-in-the-loop flow for `git push` — session archived, human-loop generated, human gates.

### Post-Commit Monitoring

After commit lands, `post-commit` hook starts the archive server, opens human-loop in browser, and monitors for human feedback. On GO, it signals readiness for the next harness iteration.

### Installation

The skill ships with an install script. After cloning, run once to set up both the skill and hooks:

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git ~/.claude/skills/harness-traj-weaver
bash ~/.claude/skills/harness-traj-weaver/scripts/install.sh
```

`install.sh` does two things:
1. Registers the skill in `~/.claude/settings.json`
2. Installs `hooks/pre-commit` and `hooks/pre-push` into `.git/hooks/` of the current repo

For manual hook installation in an existing repo:

```bash
cp ~/.claude/skills/harness-traj-weaver/hooks/pre-commit .git/hooks/pre-commit
cp ~/.claude/skills/harness-traj-weaver/hooks/pre-push .git/hooks/pre-push
```
