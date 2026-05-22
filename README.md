# harness-traj-weaver

<p align="center">
  <strong>A Skill-based implementation of <a href="https://yoonholee.com/meta-harness/">Meta-Harness</a></strong>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="./README-ZH.md">中文文档</a>
</p>

---

## Overview

`harness-traj-weaver` is a Claude Code skill that implements the Meta-Harness paradigm. Instead of relying on a fixed scaffold, an archive of prior discoveries, or a persistent memory mechanism, it gives the proposer unrestricted filesystem access to prior experience — enabling selective diagnosis of raw code and execution traces.

### Why Meta-Harness?

Traditional harness optimization works from aggregate scores and compressed summaries. Meta-Harness takes a fundamentally different approach:

- **Filesystem as memory** — Full history exposed on disk, not compressed into a vector database
- **Trace-level reasoning** — Reason over failed examples and their execution traces, not just metrics
- **Search-set feedback** — The proposer never sees test-set results; all improvement signals come from the search set
- **Self-improving** — Harness quality improves automatically as the underlying coding agent becomes more capable

---

## Core Principles

> Its outer loop is deliberately minimal: instead of relying on a fixed scaffold, an archive of prior discoveries, or a persistent memory mechanism, it gives the proposer unrestricted filesystem access to prior experience.

> Rather than reacting only to aggregate scores or summaries, the proposer in Meta-Harness can reason over failed examples and their execution traces to propose targeted edits.

> Meta-Harness can improve automatically as coding agents become more capable. The proposer never sees test-set results; its only feedback comes from the search set, the subset of task instances used to evaluate candidate harnesses during search and generate the feedback signal for improvement.

> Its key design choice is to expose full history through a filesystem, enabling selective diagnosis of raw prior code and execution traces rather than optimization from compressed per-candidate summaries.

---

## Architecture

<p align="center">
  <img src="docs/metaharness.png" alt="Meta-Harness Architecture" width="700" />
</p>

The outer loop is deliberately minimal — no fixed scaffold, no archive of discoveries, no persistent memory. The proposer leverages unrestricted filesystem access to reason over prior experience, directly inspecting failed examples and their execution traces to propose targeted edits.

---

## Demo

<p align="center">
  <video src="docs/tutorial.mp4" controls muted width="700" poster="docs/metaharness.png"></video>
</p>

---

## Eval

Benchmark evaluation results will be published here.

| Benchmark | Score | Date |
|-----------|-------|------|
| TBD | — | — |

---

## Getting Started

### Prerequisites

- [Claude Code](https://claude.ai/code) installed

### Install

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git ~/.claude/skills/harness-traj-weaver
```

---

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

---

## License

MIT

---

## See Also

- [中文文档](./README-ZH.md)
- [Meta-Harness](https://yoonholee.com/meta-harness/)
- [QUICKSTART](./QUICKSTART.md)
- [CHANGELOG](./CHANGELOG.md)
