# harness-traj-weaver

<p align="center">
  <strong>Meta-Harness — Claude Code 的自进化技能循环</strong>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <a href="./README.md">English</a>
</p>

---

## 安装

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git ~/.claude/skills/harness-traj-weaver
```

## 技能

| 技能 | 用途 |
|------|------|
| **traj** | 会话轨迹 HTML — TOC 导航、Turn 折叠、颜色编码 |
| **survey** | Human-loop QA — 终端交互式问答（27 题 / 7 节） |
| **metric** | 代码审查仪表板 — 4 项 Karpathy 原则 |

## 快速跳转

| 文档 | 内容 |
|------|------|
| [SKILL.md](./SKILL.md) | 入口 — 原则、工作流、Hook 集成 |
| [DESIGN.md](./DESIGN.md) | 设计哲学 — 配色、字体、间距 |
| [UX.md](./UX.md) | 实现 — 组件、动画、布局 |
| [CHANGELOG.md](./CHANGELOG.md) | 版本历史 |
| [QUICKSTART.md](./QUICKSTART.md) | AI Agent 配置 |

## 迭代历史

所有 harness 产物存放在 `.metaharness/v{version}/`：

```
.metaharness/v0.3.0/
  inputs/     ← QA 答案（结构化 JSON）
  outputs/    ← 轨迹 HTML、提交产物、计划 JSON
```

每个版本都是一条完整的审计轨迹：会话追踪、人类反馈及其驱动的下一迭代计划。
