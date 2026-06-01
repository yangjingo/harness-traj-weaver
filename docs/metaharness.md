# Meta-Harness: The Self-Improving Loop

## Paradigm

Meta-Harness is a **self-improving outer loop** where an Agent proposes code, a
Harness evaluates it, and results flow back into the filesystem for the next cycle.

| # | Principle | What it means |
|---|---|---|
| 1 | **Filesystem as Memory** | Full history on disk — no vector DB, no persistent memory |
| 2 | **Trace-Level Reasoning** | Diagnose raw execution traces, not compressed summaries |
| 3 | **Search-Set Feedback** | All improvement signals from the search set; never expose test-set |
| 4 | **Self-Improving** | Harness quality rises as the underlying agent improves |

## The Loop

```
  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Observe  │ ──→ │ Diagnose │ ──→ │ Propose  │ ──→ │ Evaluate │ ──→
  └──────────┘     └──────────┘     └──────────┘     └──────────┘
       ↑                                                  │
       │            .metaharness/v{version}/              │
       │        inputs/          outputs/                 │
       │    qa-*.json        traj-*.html                  │
       │    session.jsonl    plan-v{next}.json            │
       └──────────────────────────────────────────────────┘
```

1. **Observe** — Read prior execution traces and QA feedback from `.metaharness/`
2. **Diagnose** — Trace-level reasoning on raw JSONL sessions and code diffs
3. **Propose** — Generate targeted edits based on trace evidence, not aggregate scores
4. **Evaluate** — Human-loop QA in terminal via Claude's AskUserQuestion
5. **Iterate** — Answers archived, plan generated, next cycle begins

## Skill Mapping

### 1. Observe → `traj`

Reads Claude Code session JSONL and generates `traj.html` — interactive timeline with
TOC navigation, turn folding, color-coded blocks, and skill usage highlighting.

```bash
python skills/traj/scripts/generate_traj.py \
  --input ~/.claude/projects/<project>/<session>.jsonl \
  --output traj.html
```

Post-execution triggers human-loop QA to collect feedback on the trajectory output.

### 2. Evaluate → `metric`

Reads a git diff and evaluates every change against four Karpathy principles: Think
Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution. Generates
`dashboard.html` with per-principle scores and issue flags.

```bash
python skills/metric/scripts/generate_dashboard.py --diff HEAD
```

Post-execution triggers human-loop QA.

### 3. Feedback → `survey`

Terminal-interactive QA via Claude's `AskUserQuestion`. After any skill generates
output, Claude proactively starts a structured Q&A session.

- **27 questions** across 7 sections (A-G)
- **Quick mode**: 8 questions, ~3 minutes
- **Full mode**: 27 questions, ~10 minutes
- **Section G**: 9 diff-aware questions driven by `probe-diff.py` state probe
- **Archive**: answers written to `.metaharness/v{version}/inputs/qa-*.json`

```bash
python skills/survey/scripts/probe-diff.py           # state probe
python skills/survey/scripts/archive-auq-answers.py   # archive answers
```

HTML forms (`qa-survey.html`, `human-loop.html`) are retained as async fallback.

### 4. Visual Language → `DESIGN.md` + `UX.md`

Design is split into two layers:

| File | Layer | Contents |
|------|-------|----------|
| `DESIGN.md` | Philosophy | Color palette, typography, spacing, rhythm rules |
| `UX.md` | Implementation | Component patterns, animations, layout conventions |

CSS tokens live in `skills/traj/reference/design-tokens.css`. Templates inline
tokens in `<style>` — no `@import`, self-contained HTML.

See `docs/design-system.md` for the full rationale.

## Human-Loop QA Flow

```
Skill completes → output artifact ready
  │
  ├─ Claude detects output → entry gate AUQ: "现在评估 / 稍后 / 跳过?"
  │
  ├─ Mode: quick (8q / ~3min) or full (27q / ~10min)
  │
  ├─ Section-by-section: A→B→C→D→E→F→G
  │     A-C: output quality (visual, navigation, content)
  │     D:   data & stats
  │     E:   missing features (multi-select)
  │     F:   overall rating
  │     G:   diff-aware code review (9 dynamic questions)
  │
  ├─ Interrupt/resume via .metaharness/qa-state.json
  │
  └─ Archive → .metaharness/v{version}/inputs/
       Plan generated → .metaharness/v{version}/plan-v{next}.json
```

## Filesystem Layout

```
.metaharness/
  v{version}/
    inputs/
      qa-survey-*.json       ← human-loop QA answers
      qa-survey-*.txt        ← human-readable summaries
      session-*.jsonl         ← archived Claude Code sessions
    outputs/
      traj-*.html             ← session trajectory visualizations
      commit-*.json           ← per-commit artifacts
      plan-v{next}.json       ← next-version plan from QA feedback
    plan-trigger.json         ← written by post-commit
    qa-state.json             ← QA interrupt/resume state
```

## Hook Integration

### pre-commit

```
git commit
  │
  ├─ 1. Archive current session JSONL → .metaharness/v{version}/inputs/
  ├─ 2. Generate traj.html from session trace
  ├─ 3. Trigger human-loop QA in terminal (AskUserQuestion)
  │      entry gate → mode → A-G sections → archive
  └─ 4. Write plan trigger for next iteration
```

### post-commit

After commit lands: archives session, writes `.metaharness/plan-trigger.json`.

### pre-push

Same terminal QA flow for `git push`. Session archived, human-loop runs, plan updated.

```bash
# Install hooks
bash scripts/install.sh
```

## Principles in Action

| Principle | Enforced By | How |
|-----------|-------------|-----|
| Filesystem as Memory | `.metaharness/` | Every artifact on disk — no database |
| Trace-Level Reasoning | `traj` | Raw JSONL → interactive HTML, not summaries |
| Search-Set Feedback | `survey` | Terminal AUQ → structured JSON → next iteration |
| Self-Improving | The loop | Each iteration leaves richer traces → better proposals |
