# ROADMAP

## [0.1.0] — Skill Standardization

### 1. Standardize SKILL.md
- Fix frontmatter formatting (tabs → spaces)
- Add "When This Skill Activates" section with concrete triggers
- Make workflow steps reference explicit `.metaharness/` paths
- Add a "Rules" section with search-set constraints

### 2. Rewrite QUICKSTART.md for AI Agents
- Terse, one-command install: `git clone ... ~/.claude/skills/`
- Written for agents (Claude Code, Codex, OpenClaw) to copy-paste
- Remove verbose explanations — just install + verify

### 3. Output path: `.cache/` → `.metaharness/`
- All harness artifacts (traces, candidates, feedback) go under `.metaharness/`
- Update paths in SKILL.md, QUICKSTART.md

### 4. Meta-harness self-evolution
- Run Observe → Diagnose → Propose → Evaluate cycle on the repo itself
- Write trace, candidate, and feedback artifacts to `.metaharness/`
- Generate rendered traj-viewer.html and human-loop.html into `.metaharness/`
