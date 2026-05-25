# harness-traj-weaver

<p align="center">
  <strong>A Skill-based implementation of <a href="https://yoonholee.com/meta-harness/">Meta-Harness</a></strong>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="./readme-zh.md">中文文档</a>
</p>

---

## Quick Start

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git
cd harness-traj-weaver

# Generate trajectory from any Claude Code session
python skills/traj-display/scripts/generate_traj.py \
  --input ~/.claude/projects/<project>/<session>.jsonl \
  --output traj.html

# Generate survey for the current iteration
python skills/human-loop/scripts/generate_survey.py \
  --version v0.1.0 \
  --output survey.html

# Dev server (with POST feedback endpoint)
python server.py 8767
```

---

## Demo

<video src="docs/tutorial.mp4" controls muted width="100%">
  Your browser does not support embedded video. <a href="docs/tutorial.mp4">Download MP4</a>
</video>

| Trajectory | Survey |
|---|---|
| ![traj](docs/figures/preview-traj.gif) | ![survey](docs/figures/preview-survey.gif) |


---

## Overview

`harness-traj-weaver` is a Claude Code skill that implements the Meta-Harness paradigm — giving the proposer unrestricted filesystem access to prior experience for selective diagnosis of raw code and execution traces.

- **Filesystem as memory** — full history on disk, no vector database
- **Trace-level reasoning** — diagnose from raw traces, not compressed summaries
- **Search-set feedback** — never expose test-set results
- **Self-improving** — harness quality improves as coding agents get more capable

---

## Skills

| Skill | Description |
|---|---|
| **traj-display** | Claude Code session trajectory visualizer — TOC with action labels, turn-based folding, block-level highlight |
| **human-loop** | Meta-Harness feedback survey — 10 questions, 5 min, interactive HTML, POST to filesystem |
| **eval-dashboard** | Evaluation dashboard templates with Anthropic Design System |
| **design-system** | Canonical CSS tokens (colors, typography, spacing) for all HTML output |

---

## Eval — v0.1.0

```
evals/v0.1.0/
  inputs/
    session.jsonl
  outputs/
    meta-harness-66c583c5-traj.html      ← trajectory display
    meta-harness-66c583c5-session.jsonl  ← archived session
    meta-harness-66c583c5-survey.html    ← human-loop survey
    meta-harness-66c583c5-feedback-*.json ← collected feedback
```

---

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

---

## License

MIT

---

## See Also

- [中文文档](./readme-zh.md)
- [Meta-Harness](https://yoonholee.com/meta-harness/)
- [QUICKSTART](./quickstart.md)
- [CHANGELOG](./changelog.md)
