# harness-traj-weaver

<p align="center">
  <strong>Meta-Harness — self-improving skill loop for Claude Code</strong>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="./README-ZH.md">中文</a>
</p>

---

## Install

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git ~/.claude/skills/harness-traj-weaver
```

## Skills

| Skill | Purpose |
|-------|---------|
| **traj** | Session trajectory HTML — TOC, turn folding, color-coded blocks |
| **survey** | Human-loop QA — terminal AskUserQuestion (27q / 7 sections) |
| **metric** | Code review dashboard — 4 Karpathy principles |

## Quick Links

| Doc | Content |
|-----|---------|
| [SKILL.md](./SKILL.md) | Entry point — principles, workflow, hook integration |
| [DESIGN.md](./DESIGN.md) | Design philosophy — color, typography, spacing |
| [UX.md](./UX.md) | Implementation — components, animations, layout |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |
| [QUICKSTART.md](./QUICKSTART.md) | AI agent setup |

## Iteration History

All harness artifacts live in `.metaharness/v{version}/`:

```
.metaharness/v0.3.0/
  inputs/     ← QA answers (structured JSON)
  outputs/    ← traj HTML, commit artifacts, plan JSON
```

Each version is a complete audit trail: session traces, human feedback, and the
plan it generated for the next cycle.
