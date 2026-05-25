# harness-traj-weaver

<p align="center">
  <strong><a href="https://yoonholee.com/meta-harness/">Meta-Harness</a> 的 Skill 化工程实现</strong>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="./readme.md">English README</a>
</p>

---

## 快速开始

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git
cd harness-traj-weaver

# 从 Claude Code 会话生成轨迹
python skills/traj-display/scripts/generate_traj.py \
  --input ~/.claude/projects/<project>/<session>.jsonl \
  --output traj.html

# 生成当前迭代的反馈问卷
python skills/human-loop/scripts/generate_survey.py \
  --version v0.1.0 \
  --output survey.html

# 开发服务器（支持 POST 提交反馈）
python server.py 8767
```

---

## 演示

<video src="docs/tutorial.mp4" controls muted width="100%">
  你的浏览器不支持嵌入式视频。<a href="docs/tutorial.mp4">下载 MP4</a>
</video>

| 轨迹展示 | 反馈问卷 |
|---|---|
| ![traj](docs/figures/preview-traj.gif) | ![survey](docs/figures/preview-survey.gif) |
---

## 概述

`harness-traj-weaver` 是一个 Claude Code skill，实现了 Meta-Harness 范式——赋予 proposer 无限制的文件系统访问权限来利用先前的经验，对原始代码和执行轨迹进行选择性诊断。

- **文件系统即记忆** — 完整历史在磁盘上，无需向量数据库
- **轨迹级推理** — 从原始 trace 诊断，而非压缩摘要
- **搜索集反馈** — 永远不暴露测试集结果
- **自我进化** — harness 随 coding agent 能力提升而自动改进

---

## Skills

| Skill | 描述 |
|---|---|
| **traj-display** | Claude Code 会话轨迹可视化 — TOC 操作标签、Turn 折叠、Block 级高亮 |
| **human-loop** | Meta-Harness 人机反馈问卷 — 10 题、5 分钟、交互式 HTML、POST 写入文件系统 |
| **eval-dashboard** | 评估仪表板模板，使用 Anthropic Design System |
| **design-system** | 规范 CSS 令牌（颜色、字体、间距），统一所有 HTML 输出 |

---

## 评估 — v0.1.0

```
evals/v0.1.0/
  inputs/
    session.jsonl
  outputs/
    meta-harness-66c583c5-traj.html      ← 轨迹展示
    meta-harness-66c583c5-session.jsonl  ← 存档会话
    meta-harness-66c583c5-survey.html    ← 人机反馈问卷
    meta-harness-66c583c5-feedback-*.json ← 收集到的反馈
```

---

## 参与贡献

欢迎提交 issue 和 pull request。

---

## 许可证

MIT

---

## 另见

- [English README](./readme.md)
- [Meta-Harness](https://yoonholee.com/meta-harness/)
- [QUICKSTART](./quickstart.md)
- [CHANGELOG](./changelog.md)
