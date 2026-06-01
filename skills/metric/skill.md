---
name: metric
version: "0.3.0"
description: Meta-Harness evaluation skill — code review against Karpathy principles and interactive HTML dashboard generation. Evaluates code changes across four dimensions: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution.
---

## Overview

`scripts/generate_dashboard.py` reads a git diff (or specified files) and evaluates every change against four code-quality principles distilled from Andrej Karpathy's observations on LLM coding failures. It produces a self-contained `dashboard.html` with per-principle scores, issue flags, and a structured review report.

## Evaluation Principles

Adapted from [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md):

### 1. Think Before Coding
- **Does the change state assumptions explicitly?**
- Are multiple interpretations considered before implementation?
- Does the code pause to clarify ambiguity rather than silently assuming?

### 2. Simplicity First
- **No unrequested features, abstractions, or flexibility.**
- If 200 lines can be 50, rewrite.
- No premature generalization — three similar lines is better than a premature abstraction.
- No half-finished implementations.

### 3. Surgical Changes
- **Every changed line must trace back to a user need.**
- No drive-by refactors, no deleted comments, no style-only changes in functional PRs.
- Matches existing code patterns — doesn't impose personal preference.

### 4. Goal-Driven Execution
- **Every task has a verifiable completion criterion.**
- "Write a failing test first, then fix until it passes."
- Completion is measurable, not subjective.

## Review Output

The dashboard evaluates each changed file across four dimensions:

| Dimension | Score | What it checks |
|---|---|---|
| Assumption Clarity | 0-5 | Are assumptions stated? Are alternatives discussed? |
| Simplicity | 0-5 | Is every line necessary? Can it be shorter? |
| Surgical Precision | 0-5 | Do all changes trace to the goal? No tangential edits? |
| Goal Alignment | 0-5 | Is the change verifiably complete? |

Each flagged issue includes the file, line range, principle violated, and a suggested fix.

## Design Tokens

Color palette and typography: see `DESIGN.md`. CSS tokens are inlined in templates.

Key tokens:
| Token | Hex | Usage |
|---|---|---|
| `canvas` | `#faf9f5` | Page background, warm cream |
| `surface-dark` | `#181715` | Sidebar, dark panels |
| `primary` | `#cc785c` | Coral — CTAs, violations, user emphasis |
| `accent-teal` | `#5db8a6` | Success, clean scores |
| `accent-amber` | `#e8a55a` | Warnings, marginal scores |

## Templates

| File | Purpose |
|---|---|
| `reference/dashboard.css` | Full CSS with all component styles |
| `reference/dashboard.js` | Client interactivity: navigation, filtering |
| `reference/dashboard-template.html` | HTML skeleton with `$variable` placeholders |

## Usage

```bash
# Review staged changes
python skills/metric/scripts/generate_dashboard.py --diff HEAD

# Review a specific file
python skills/metric/scripts/generate_dashboard.py --files path/to/file.py

# Review with custom output path
python skills/metric/scripts/generate_dashboard.py --diff HEAD --output review.html
```

## Meta-Harness Integration

This skill embodies Meta-Harness Principle #3 (Search-set feedback). The review dashboard surfaces code quality issues before they reach evaluation, preventing bad patterns from propagating into the search set.

## Post-Execution: Human-Loop QA

After generating a dashboard HTML file, trigger the human-loop QA to collect structured
feedback on the review output quality. Follow the same pattern as `skills/traj/skill.md`:

1. Announce completion: which diff/files were reviewed, output path, scores summary.
2. Invoke the survey skill's human-loop workflow from `skills/survey/skill.md`.
3. Follow: entry gate → mode selection → section-by-section QA → archive.
