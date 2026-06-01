# Human-Loop: Terminal Interactive QA

## 1. 核心机制

Claude Code 提供了原生工具 `AskUserQuestion`，可以在终端里直接向用户展示选项并收集答案。整个 human-loop 就是：**Claude 调用这个工具 → 用户在终端选择 → Claude 收到答案 → 记录 → 下一个问题**。

不需要 HTML 表单，不需要浏览器。一切在终端对话中完成。

### 1.1 工具签名

```
AskUserQuestion({
  questions: [{
    question: "完整的问题文本（支持多行、markdown）",
    header:  "简短标签（≤12字符）",
    multiSelect: false,       // true = 多选, false = 单选
    options: [
      { label: "选项 A (recommended)", description: "这个选项的具体含义和后果" },
      { label: "选项 B",               description: "这个选项的具体含义和后果" },
    ]
  }]
})
```

一次调用可以包含 **1-4 个问题**，每个问题 **2-4 个选项**。

### 1.2 答案返回格式

```
User has answered your questions:
"问题文本"="用户选中的 label".
You can now continue with the user's answers in mind.
```

### 1.3 终端里的实际效果

用户在终端看到的是：

```
☐ 整体配色是否符合预期？

❯ 1. 满意，不需要调整
    颜色搭配和谐，符合技能定位，无需改动
  2. 基本满意，色调可微调
    整体方向对，但个别颜色需要调整饱和度或明度
  3. 不满意，需要重新设计
    配色方案与预期差距较大，需要重新选择色板
```

用户输入数字或用方向键选择，回车确认。这就是全部交互。

## 2. 交互流程

### 2.1 完整时序

```
技能执行完毕
  │
  ├─ Claude 输出 prose: "本次生成了 X，要不要花 3 分钟做个 QA？"
  │
  ├─ AskUserQuestion #1  进入闸门: 现在评估 / 稍后 / 跳过
  │    用户选择 "现在评估"
  │
  ├─ AskUserQuestion #2  模式选择: 快速 6 题 / 完整 22 题
  │    用户选择 "快速模式"
  │
  ├─ AskUserQuestion #3  A1. 整体配色
  ├─ AskUserQuestion #4  B1. TOC 分类
  ├─ AskUserQuestion #5  C1. 内容截断
  ├─ AskUserQuestion #6  D1. 数据面板
  ├─ AskUserQuestion #7  E1. 缺失功能（多选）
  ├─ AskUserQuestion #8  F1. 整体满意度
  │
  ├─ Claude 输出 prose: 汇总 → 写入 .metaharness/ → 完成
  │
  └─ 结束。答案已归档为 search-set feedback
```

### 2.2 关键规则

- **一个问题一次调用**：不批量，每次 AskUserQuestion 只放一个问题（除非是快速模式下同一节的两个关联题）
- **每次等答案**：不等用户回答绝不继续下一个问题
- **问题文本用中文**：meta-harness 的 QA 对象是技能输出，问题语言保持和现有 qa-survey.html 一致
- **选项 label 包含推荐标记**：如 `"满意，不需要调整 (recommended)"`
- **description 写清楚后果**：不只是 "满意"，要写 "颜色搭配和谐，符合技能定位，无需改动"

## 3. 问题设计

### 3.1 现有 22 题到 AUQ 的映射

从 `qa-survey.html` 的 6 节 22 题中，选出适合终端交互的题目：

**A 节 — 整体视觉（3 题 → 3 AUQ）**

| 题号 | 问题 | 选项数 | 类型 |
|------|------|--------|------|
| A1 | 整体配色是否符合预期？ | 3 | 单选 |
| A2 | 字体搭配是否合适？ | 4 | 单选 |
| A3 | 页面布局是否合理？ | 3 | 单选 |

**B 节 — 导航/TOC（3 题 → 2 AUQ，B3 合并到 C 节）**

| 题号 | 问题 | 选项数 | 类型 |
|------|------|--------|------|
| B1 | TOC 条目分类是否提升了可读性？ | 4 | 单选 |
| B2 | 图标和颜色区分是否清晰？ | 3 | 单选 |

**C 节 — 内容展示（5 题 → 3 AUQ，C1+C3 合并，C5 独立）**

| 题号 | 问题 | 选项数 | 类型 |
|------|------|--------|------|
| C1+3 | 折叠截断策略是否合理？ | 3 | 单选 |
| C2 | 操作标签是否有助理解？ | 4 | 单选 |
| C4 | Tool 调用块信息密度是否合适？ | 4 | 单选 |

**D 节 — 数据与内容（3 题 → 2 AUQ，D1 合并到 C1+3）**

| 题号 | 问题 | 选项数 | 类型 |
|------|------|--------|------|
| D2 | 统计面板指标是否覆盖关键维度？ | 3 | 单选 |
| D3 | Demo 内容是否典型？ | 3 | 单选 |

**E 节 — 缺失功能（2 题 → 1 AUQ + 1 文本）**

| 题号 | 问题 | 选项数 | 类型 |
|------|------|--------|------|
| E1 | 最希望下一版本看到哪些功能？ | 8 | 多选 |
| E2 | 其他改进建议？ | — | prose 收集 |

**F 节 — 总体评分（2 题 → 2 AUQ）**

| 题号 | 问题 | 选项数 | 类型 |
|------|------|--------|------|
| F1 | 整体满意度 | 5 | 单选 |
| F2 | 是否达到预期目标？ | 3 | 单选 |

**快速模式**：每节选 1 题 = 6 AUQ + 1 entry gate + 1 mode = 8 轮
**完整模式**：全部 = 14 AUQ + 1 entry gate + 1 mode = 16 轮

### 3.2 问题编写示例

以 A1 "整体配色" 为例，从 HTML 表单的：

```html
<h3>A1. 整体配色是否符合预期？</h3>
<div class="option"><input type="radio" value="A"> A. 满意，不需要调整</div>
<div class="option"><input type="radio" value="B"> B. 基本满意，色调可微调</div>
<div class="option"><input type="radio" value="C"> C. 不满意，需要重新设计</div>
```

转化为 AUQ 调用：

```json
{
  "questions": [{
    "header": "配色",
    "question": "A1. 整体配色是否符合预期？\n\n本次输出的配色方案基于 Cormorant Garamond + Inter + JetBrains Mono 字体组合，暖色系为主（--primary: #cc785c），浅色背景（--canvas: #faf9f5）。",
    "multiSelect": false,
    "options": [
      { "label": "满意，不需要调整 (recommended)", "description": "颜色搭配和谐，符合技能定位，无需改动" },
      { "label": "基本满意，色调可微调", "description": "整体方向对，但个别颜色需要调整饱和度或明度" },
      { "label": "不满意，需要重新设计", "description": "配色方案与预期差距较大，需要重新选择色板" }
    ]
  }]
}
```

## 答案格式

工具返回：

```
User has answered your questions:
"A1. 整体配色是否符合预期？..."="满意，不需要调整 (recommended)".
You can now continue with the user's answers in mind.
```

## 4. 答案归档

每轮 QA 完成后，将所有答案汇总写入 JSON：

```json
{
  "skill": "traj-weaver",
  "version": "v0.2.0",
  "mode": "quick",
  "timestamp": "2026-06-01T10:30:00Z",
  "branch": "main",
  "answers": {
    "entry_gate": "现在评估",
    "mode": "快速模式",
    "a1_color": "满意，不需要调整",
    "b1_toc": "是，明显提升",
    "c1_fold": "合理，满足需求",
    "d2_stats": "基本覆盖，但缺少某些指标",
    "e1_features": ["搜索/过滤内容", "暗色模式"],
    "f1_satisfaction": "4 — 满意，少量细节可优化"
  }
}
```

写入路径：`.metaharness/{version}/inputs/qa-{skill}-{timestamp}.json`

## 5. 中断续接

如果用户在 QA 中途停止（比如选了 "暂停"），保存进度到 `.metaharness/qa-state.json`：

```json
{
  "skill": "traj-weaver",
  "version": "v0.2.0",
  "mode": "quick",
  "current_question": "c1_fold",
  "completed": ["a1_color", "b1_toc"],
  "answers": { "a1_color": "满意，不需要调整", "b1_toc": "是，明显提升" }
}
```

下次 session 的 preamble 检测到此文件，主动询问是否续接。

## 6. 技能文件结构

```
skills/survey/
├── skill.md                        # 技能定义（更新：加入 human-loop 指令）
├── reference/
│   ├── qa-survey.html              # 保留：HTML 表单（异步/多人用）
│   ├── human-loop.html             # 保留：HTML 表单
│   ├── human-loop-design.md        # 本文档
│   └── auq-questions.json          # 新增：题库（22 题 → AUQ 参数）
├── scripts/
│   ├── generate_survey.py          # 保留
│   └── archive-auq-answers.py     # 新增：解析答案 → 写入 evals
```

### 6.1 题库格式（auq-questions.json）

```json
{
  "sections": {
    "A": {
      "title": "整体视觉",
      "questions": {
        "a1_color": {
          "header": "配色",
          "question": "A1. 整体配色是否符合预期？\n\n...",
          "options": [
            { "label": "满意，不需要调整 (recommended)", "description": "..." },
            { "label": "基本满意，色调可微调", "description": "..." },
            { "label": "不满意，需要重新设计", "description": "..." }
          ]
        }
      }
    }
  },
  "quickMode": ["a1_color", "b1_toc", "c1_fold", "d2_stats", "e1_features", "f1_satisfaction"]
}
```

### 6.2 技能 SKILL.md 核心指令（节选）

```markdown
## Human-Loop QA Workflow

### Step 0: Entry Gate

技能执行完成后，如果产生了可评估的输出产物（HTML 文件、display 输出等），
发起 entry gate AUQ。

### Step 1: Mode Selection

### Step 2: Section-by-Section

逐题调用 AskUserQuestion。每道题从 `reference/auq-questions.json` 读取参数。
快速模式走 `quickMode` 列表，完整模式走全量。

规则：
- 每次只发一个问题（一个 AUQ 调用放一个 question）
- 必须等用户回答后才能发下一个
- 每节结束后用 prose 简短小结（1-2 句），不额外提问
- 每 2 节后问一次是否继续

### Step 3: Archive

汇总所有答案，写入 `.metaharness/{version}/inputs/qa-{skill}-{timestamp}.json`
```

## 7. 与 gstack plan 模式的关键区别

| 维度 | gstack plan 模式 | Meta-Harness human-loop |
|------|-----------------|------------------------|
| 问题来源 | 从计划内容**动态推导** | 从题库**加载 + 上下文补充** |
| 决策重量 | 高（影响架构/实现方向） | 中（影响下轮迭代优先级） |
| 问题文本 | 英文 decision brief（ELI10/Stakes/Net） | 中文选择题（简洁直接，不需 decision brief 仪式） |
| AUTO_DECIDE | 支持 | 不支持（反馈必须人为） |
| 归档目标 | TODOS.md / plan file | evals inputs JSON → search-set |
| 频率 | 低频（每 plan 1-2 次） | 高频（每次技能迭代后） |

> **不需要 decision brief 格式**。gstack 的 ELI10/Stakes/Net 是用于**高 stakes 架构决策**的仪式感。meta-harness 的 QA 是**轻量反馈收集**，问题直接、选项清晰即可。过度格式化反而降低完成率。
