# Meta-Harness: The Self-Improving Loop

## Paradigm

Meta-Harness is a **self-improving outer loop** where an Agent proposes code, a Harness evaluates it, and results flow back into the filesystem for the next cycle. Four principles govern every iteration:

| # | Principle | What it means |
|---|---|---|
| 1 | **Filesystem as Memory** | Full history on disk — no vector DB, no persistent memory |
| 2 | **Trace-Level Reasoning** | Diagnose raw execution traces, not compressed summaries |
| 3 | **Search-Set Feedback** | All improvement signals from the search set; never expose test-set |
| 4 | **Self-Improving** | Harness quality rises as the underlying agent improves |

## The Loop

```
                         +-------------------+
                         |   Filesystem      |
                         |   (.cache/evals)  |<-----------------------------+
                         +--------+----------+                              |
                                  |                                         |
                         (3) Store all Logs                                 |
                       (traces, candidates,                                 |
                        feedback, reviews)                                  |
                                  |                                         |
                                  v                                         |
    +-----------------------------+-----------------------------------+     |
    |                             |                                   |     |
    |  +------------------+  +------------------+  +----------------+ |     |
    |  | Proposed Code    |  | Reasoning Traces |  | Eval Scores    | |     |
    |  | (diffs, commits) |  | (JSONL sessions) |  | (review dash)  | |     |
    |  +--------+---------+  +--------+---------+  +-------+--------+ |     |
    |           |                     |                    |          |     |
    +-----------+---------------------+--------------------+----------+     |
                |                     |                    |                |
                | (1) Propose         | Read               | Feedback       |
                v                     v                    |                |
    +-----------+----------+  +-------+--------+          |                |
    | Harness + LLM        |  | traj           |          |                |
    | (Claude Code)        |  | Trace Visualize|<---------+                |
    +-----------+----------+  +----------------+                           |
                |                                                          |
                v                                                          |
    +-----------+----------+                                               |
    | Tasks DB             |                                               |
    | (Eval benchmarks)   |                                               |
    +-----------+----------+                                               |
                |                                                          |
                | (2) Evaluate                                             |
                v                                                          |
    +-----------+----------+                                               |
    | metric               |                                               |
    | Code Review Dashboard|                                               |
    | (Karpathy 4 Principles)                                              |
    +-----------+----------+                                               |
                |                                                          |
                v                                                          |
    +-----------+----------+                                               |
    | survey               |                                               |
    | Human Feedback Loop  |----------------------------------------------+
    | (QA + Human-Loop)    |
    +----------------------+
```

## Skill Mapping

Each step of the loop is powered by a dedicated skill under `skills/`:

### 1. Observe → `traj`

Reads Claude Code session JSONL and generates a self-contained `traj.html` — an interactive timeline view with TOC navigation, thinking blocks, tool call tracking, and skill usage highlighting.

```
python skills/traj/scripts/generate_traj.py \
  --input ~/.claude/projects/<project>/<session>.jsonl \
  --output meta-harness-traj.html
```

**Supports Principle #2 (Trace-Level Reasoning):** Instead of compressed summaries, the trajectory view exposes raw conversation structure — thinking blocks, tool inputs/outputs, and skill interactions — so failures can be diagnosed directly from execution traces.

### 2. Evaluate → `metric`

Reads a git diff and evaluates every change against the four **Karpathy Principles**:

| P# | Principle | Checks |
|---|---|---|
| P1 | Think Before Coding | Assumptions stated? Alternatives considered? |
| P2 | Simplicity First | No over-engineering? Can it be shorter? |
| P3 | Surgical Changes | Every line traces to the goal? No drive-by edits? |
| P4 | Goal-Driven Execution | Verifiable completion criteria? |

```
python skills/metric/scripts/generate_dashboard.py \
  --diff HEAD --goal "Add user auth" --output review.html
```

Generates a self-contained `dashboard.html` with per-principle scores, per-file breakdowns, and auto-detected issues with suggested fixes.

**Supports Principle #3 (Search-Set Feedback):** The review dashboard surfaces code quality issues before they reach evaluation, preventing bad patterns from propagating.

### 3. Feedback → `survey`

Generates structured HTML-form questionnaires with embedded git history, CHANGELOG, and ROADMAP context. Two types:

| Type | Target | Questions |
|---|---|---|
| `qa` | Individual skill UI/UX | 22 questions across 6 sections |
| `human-loop` | Meta-Harness paradigm | 19 questions across 4 parts |

```
python skills/survey/scripts/generate_survey.py --type qa --skill traj --version v0.1.0
python skills/survey/scripts/generate_survey.py --type human-loop --version v0.1.0
```

Each survey auto-injects:
- `git log --oneline -15` — recent commits
- `git log -5` — detailed commit messages
- `CHANGELOG.md` — project version history
- `ROADMAP.md` — future direction

**Supports Principle #3 & #4:** Human feedback collected via surveys drives the next iteration's priorities, closing the loop from evaluation back to proposal.

### 4. Visual Language → `theme`

Canonical CSS design tokens (`reference/design-tokens.css`) — color palette, typography scale, spacing rhythm — used by all skills to produce visually consistent, self-contained HTML output. Inspired by the Anthropic brand: warm cream canvas, coral accents, dark sidebar, serif headings.

## The Complete Cycle

```
Iteration N:
  1. Agent proposes changes via Claude Code
  2. Session JSONL is captured → traj visualizes execution traces
  3. git diff is reviewed → metric scores against Karpathy principles
  4. survey collects human feedback (with git log + CHANGELOG context)
  5. Results stored in evals/v{N}/outputs/
  6. Agent reads feedback, CHANGELOG, and traces from filesystem
  7. Iteration N+1 begins, informed by the full history
```

## Filesystem Layout

```
.cache/
  traces/       — execution traces (JSONL sessions)
  candidates/   — candidate harness outputs
  feedback/     — search-set evaluation results

evals/
  v0.1.0/
    inputs/
      session.jsonl                 — archived session for traj demo
    outputs/
      meta-harness-traj.html        — generated trajectory HTML
      meta-harness-survey.html      — human feedback survey
      dashboard.html                — code review results

CHANGELOG.md    — project version history
ROADMAP.md      — future direction (optional, surfaced in surveys)
```

## Principles in Action

The four Meta-Harness principles aren't just abstract — they're enforced by the skills:

| Principle | Enforced By | How |
|---|---|---|
| Filesystem as Memory | All skills | Every artifact lands in `.cache/` or `evals/` — nothing in a database |
| Trace-Level Reasoning | `traj` | Raw JSONL → interactive HTML, not compressed summaries |
| Search-Set Feedback | `metric` + `survey` | Review dashboards + human surveys feed the loop, never test-set data |
| Self-Improving | The loop itself | Each iteration leaves richer traces → better diagnosis → better proposals |

## Hook: Pre-Commit Gate

The `pre-commit` hook closes the loop automatically — it fires before every `git commit` and links each commit back to the Claude Code session that produced it.

### What it does

```
git commit
  │
  ├─ 1. Find current Claude Code session JSONL
  │     (~/.claude/projects/<project>/<latest>.jsonl)
  │
  ├─ 2. Generate traj.html from the session trace
  │     → .cache/feedback/traj-<session-id>.html
  │
  ├─ 3. Run metric review (Karpathy 4 principles) on staged changes
  │     → .cache/feedback/review-<timestamp>.html
  │
  ├─ 4. Show terminal summary: score, issues, file paths
  │
  └─ 5. Block commit if score < threshold (strict mode)
```

### Install

```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Configure

```bash
# Set minimum score to allow commit (default: 2.5)
git config metaharness.threshold 3.0

# Block commits below threshold (default: false)
git config metaharness.strict true

# Skip hook for one commit
git config metaharness.skip true
git commit -m "emergency fix"
git config --unset metaharness.skip
```

### What the developer sees

```
=== Meta-Harness Pre-Commit Review ===
  Files reviewed: 3
  Issues found:   4
  Overall score:  3.8/5 (NEEDS WORK)

  P1 Think Before Coding  ████████░░ 4/5
  P2 Simplicity First      ██████░░░░ 3/5
  P3 Surgical Changes      ████████░░ 4/5
  P4 Goal-Driven Execution ████████░░ 4/5

  traj:    .cache/feedback/traj-f615685c.html
  metric:  .cache/feedback/review-20260525-184100.html
  session: f615685c-0a69-4354-90db-b2fbb68c038b.jsonl
```

### Why session matters

Every commit is the output of a Claude Code session. By linking the session JSONL, the hook ensures:

- **Traceability**: Any commit can be traced back to the exact conversation that produced it
- **Diagnosis**: If a commit introduces a bug, replay the session trace to see what the agent was thinking
- **Feedback**: The session ID becomes part of the review artifact, closing the loop from proposal → trace → review → feedback
