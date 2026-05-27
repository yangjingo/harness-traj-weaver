# Changelog

All notable changes to this project will be documented in this file.
All intermediate artifacts and eval outputs are archived under `.metaharness/v{version}/`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] — 2026-05-27

### Changed

- **Output isolation**: `evals/` → `.metaharness/v{version}/` — all harness artifacts now hidden, versioned, append-only
- **README standardized**: agent one-click install (`git clone ... ~/.claude/skills/`) at top, usage below
- **Hook integration**: `pre-commit` (trigger skill on commit) + `pre-push` (full Observe→Diagnose→Propose→Evaluate)
- **`server.py` → `archive_feedback.py`**: moved to `skills/survey/scripts/`, auto-detects version from git tag
- **Skills restructured**: `qa-survey` + `human-loop` merged into `survey` with unified `--type` flag
- **Renamed**: `eval-dashboard` → `metric`, `design-system` → `theme`
- **Survey output**: QA and human-loop surveys now self-contained HTML instead of Markdown

### Added

- `scripts/install.sh` — one-command setup: registers skill + installs git hooks
- `skill.md` Hook Integration section with commit/push trigger documentation
- All paths in `skill.md`, `quickstart.md`, `readme.md` updated: `.cache/` → `.metaharness/`

---

## [0.1.0] — 2026-05-25

### Added

- **skills/traj** — Claude Code session trajectory HTML generator (TOC, turn folding, color-coded blocks, stats panel)
- **skills/metric** — Evaluation metrics dashboard HTML generator
- **skills/theme** — Theme CSS tokens and visual language
- **skills/survey** — Feedback survey generator (QA + human-loop)
- `evals/v0.1.0/` — versioned eval structure with demo session
- `skill.md` with principles, workflow, and filesystem layout
- Core Meta-Harness principles documentation
- Architecture diagram + demo video
- `claude.md` with documentation sync rules and commit checklist
