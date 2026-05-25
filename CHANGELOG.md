# Changelog

All notable changes to this project will be documented in this file.
All intermediate artifacts and eval outputs are archived under `evals/v{version}/`.
QA surveys and user feedback are archived as eval inputs for the next iteration.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-05-25

### Added

- **skills/traj-display** — Claude Code session trajectory HTML generator
  - TOC with action-type labels (Thinking/Bash/Skill/Read/Write/Text) instead of generic "Assistant"
  - Turn-based folding timeline with action badges on turn headers
  - Color-coded content blocks (teal=thinking, amber=tool calls, coral=skill-exec)
  - Stats panel: user turns, skill calls, interventions, file reads/writes, tool calls, thinking
  - Mobile responsive (TOC hidden below 860px)
  - Self-contained HTML output (inline CSS, no build step)
- **skills/metric** — Evaluation metrics dashboard HTML generator (templates)
- **skills/theme** — Theme CSS tokens and visual language
- **evals/** directory with versioned eval structure:
  - `v0.1.0/inputs/session.jsonl` — demo session archive
  - `v0.1.0/inputs/qa-survey.md` — feedback questionnaire (22 questions)
  - `v0.1.0/outputs/traj.html` — generated trajectory demo
- skill.md updated with Skills section and Quick Start guide

## [Unreleased]

### Changed

- **Skills restructured**: `qa-survey` + `human-loop` merged into `survey` with unified `--type qa|human-loop` script
- **Renamed**: `eval-dashboard` → `metric`, `design-system` → `theme`
- **Survey output**: QA and human-loop surveys now generate self-contained HTML forms instead of Markdown

### Added

- Initial project structure with readme.md, readme-zh.md, and changelog.md
- Core Meta-Harness principles documentation
- Architecture diagram (`docs/icon.png`)
- Demo video (`docs/tutorial.mp4`)
- Eval section placeholder
- `claude.md` with documentation sync rules and commit checklist
- Git `post-commit` hook to remind doc and eval updates on every commit
- Professional README layout: badges, Overview, Why Meta-Harness, Architecture, Demo, Eval, Getting Started, Contributing, License
