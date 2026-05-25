---
name: survey
version: "0.1.0"
description: Feedback survey generator for Meta-Harness iterations. Two survey types — qa (skill-level UI/UX feedback) and human-loop (Meta-Harness paradigm assessment). Produces structured questionnaires archived as eval inputs for the next development cycle.
---

## Overview

`skills/survey/` generates structured feedback questionnaires for Meta-Harness. Two survey types serve different feedback layers:

| Type | Target | Purpose | Output |
|---|---|---|---|
| `qa` | Individual skill | UI/UX feedback for display skills | `evals/v{version}/inputs/qa-survey.html` |
| `human-loop` | Meta-Harness paradigm | Harness quality & iteration feedback | `evals/v{version}/outputs/meta-harness-survey.html` |

## Design Principles

1. **Mostly structured, always supplementable** — Every question is multiple-choice or true/false with a free-text supplement area.
2. **Targeted scope** — QA surveys target a specific skill version; human-loop surveys target the harness paradigm itself.
3. **Archival** — Survey responses are archived as eval inputs, forming a feedback loop that drives Meta-Harness Principle #3 (Search-set feedback).

## QA Survey

Assesses individual skill output across 6 sections (22 questions):

| Section | Focus | # Questions |
|---|---|---|
| A. Overall Visual | Color palette, typography, layout | 3 |
| B. Navigation/TOC | Label clarity, icon distinction, interaction | 3 |
| C. Content Display | Core feature usability | 5 |
| D. Data & Content | Truncation, stats coverage, demo representativeness | 3 |
| E. Missing Features | Multi-select wishlist + open suggestions | 2 |
| F. Overall Rating | Satisfaction score + Meta-Harness alignment | 2 |

## Human-Loop Survey

Assesses the Meta-Harness paradigm itself across 6 sections:

| Section | Focus |
|---|---|
| A. Filesystem as Memory | `.cache/` layout, trace discoverability |
| B. Trace-Level Reasoning | traj-display granularity, thinking blocks usefulness |
| C. Search-Set Feedback | Signal clarity, overfitting detection |
| D. 5-Step Workflow | Observe → Diagnose → Propose → Evaluate → Iterate |
| E. Self-Improving | Harness improvement trajectory |
| F. Overall | Satisfaction, weakest principle, open feedback |

## Templates

| File | Purpose |
|---|---|
| `reference/qa-survey.html` | QA survey HTML form template with `$SKILL_NAME` and `$VERSION` placeholders |
| `reference/human-loop.html` | Human-loop survey HTML form template with `$VERSION` placeholder |

## Usage

```bash
# Generate a QA survey for a specific skill version
python skills/survey/scripts/generate_survey.py \
  --type qa \
  --skill traj-display \
  --version v0.1.0

# Generate a Meta-Harness human-loop survey
python skills/survey/scripts/generate_survey.py \
  --type human-loop \
  --version v0.1.0
```

## Feedback Loop

```
skills/{name}/v{version} → deployed → survey collected
    → responses archived in evals/v{version}/
    → feedback drives next iteration
```
