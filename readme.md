# harness-traj-weaver

<p align="center">
  <strong>A Skill-based implementation of <a href="https://yoonholee.com/meta-harness/">Meta-Harness</a></strong>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="./readme-zh.md">中文文档</a>
</p>

---

## Install

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git ~/.claude/skills/harness-traj-weaver
```

The skill auto-loads on next session start. No further configuration needed.

## Usage

```bash
cd ~/.claude/skills/harness-traj-weaver

# Generate trajectory from any Claude Code session
python skills/traj/scripts/generate_traj.py \
  --input ~/.claude/projects/<project>/<session>.jsonl \
  --output traj.html

# Run terminal-interactive QA (primary feedback path)
python skills/survey/scripts/probe-diff.py          # state probe for diff-aware questions
python skills/survey/scripts/archive-auq-answers.py  # archive QA answers to .metaharness/

# Generate HTML survey (async fallback)
python skills/survey/scripts/generate_survey.py \
  --type qa \
  --output survey.html

# Dev server (POST feedback endpoint)
python skills/survey/scripts/archive_feedback.py 8767
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
| **traj** | Claude Code session trajectory visualizer — TOC, turn folding, color-coded blocks, skill usage highlighting |
| **survey** | Human-loop QA — terminal-interactive via Claude's AskUserQuestion (27 questions, 7 sections), HTML forms as async fallback |
| **metric** | Evaluation metrics dashboard templates |

---

## Eval — v0.3.0

```
.metaharness/v0.3.0/
  inputs/
    qa-survey-*.json        ← 27-question full-mode QA (human-loop terminal AUQ)
  outputs/
    traj-378bb48b.html      ← release session trajectory (12 turns, 906 records)
  plan-v0.4.0.json          ← next-version plan from QA feedback
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
