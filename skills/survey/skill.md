---
name: survey
version: "0.3.0"
description: |
  Feedback survey generator for Meta-Harness iterations. Two survey types:
  - qa: skill-level UI/UX feedback (HTML form for async use)
  - human-loop: terminal-interactive QA using Claude's AskUserQuestion tool

  Human-loop is the primary feedback path. After a skill generates output,
  Claude proactively starts an interactive Q&A in the terminal to evaluate
  the output quality. Answers are archived as structured JSON for the next
  development cycle.

  Proactively suggest when a skill iteration completes and output artifacts
  are ready, or when the user says "review the output", "evaluate this",
  "how does it look", "run QA", or "给个反馈".
  Voice triggers (speech-to-text aliases): "review the output", "run QA",
  "evaluate the result", "quality check", "给反馈".
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
triggers:
  - review the output
  - evaluate this skill
  - run qa
  - quality check
  - 给反馈
  - human loop
---

## Overview

`skills/survey/` collects structured feedback on Meta-Harness skill outputs. Two modes serve different feedback loops:

| Mode | Target | Method | Output |
|------|--------|--------|--------|
| `human-loop` | Skill output (per iteration) | Terminal-interactive AUQ | `.metaharness/v{version}/inputs/qa-{skill}-{ts}.json` |
| `qa` (HTML) | Skill output (async / multi-reviewer) | Static HTML form | `.metaharness/v{version}/inputs/qa-survey.html` |

## Human-Loop Workflow (Primary)

This workflow runs in the terminal via Claude's `AskUserQuestion` tool. The skill
drives a structured Q&A session: entry gate → mode selection → section-by-section
questions → archive.

### Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
_SKILL_NAME="${1:-unknown}"
echo "SKILL: $_SKILL_NAME"
_VERSION="${2:-unknown}"
echo "VERSION: $_VERSION"
_STATE_FILE=".metaharness/qa-state.json"
[ -f "$_STATE_FILE" ] && echo "HAS_STATE: yes" || echo "HAS_STATE: no"
```

### Step 0: Detect pending state

If `HAS_STATE` is `yes`, read `.metaharness/qa-state.json`. If it contains an
incomplete QA session, propose resumption via AskUserQuestion:

```
Header: 续接
Q: 检测到未完成的 QA — {skill} v{version}，已完成 {n}/{total} 题。是否续接？
Options:
- A) 继续上次的 QA (recommended)
- B) 放弃进度，开始新的 QA
- C) 清除状态，暂不 QA
```

If user chooses A, load state and jump to the saved question. If B, delete state
and proceed to Step 1. If C, delete state and exit.

### Step 1: Entry gate

After any Meta-Harness skill completes and produces output, propose QA:

```
Header: QA
Q: 是否现在评估本次技能输出？现在做只需 3-5 分钟，反馈会直接驱动下一轮迭代。
Options:
- A) 现在评估 (recommended) — 记忆新鲜，反馈最准确，3-5 分钟完成
- B) 稍后评估 — 生成 HTML 表单，下次方便时填写
- C) 跳过本轮 — 零时间成本，但失去本轮反馈数据
```

If B: run `python skills/survey/scripts/generate_survey.py --type qa` and exit.
If C: exit.
If A: continue to Step 2.

### Step 2: Mode selection

```
Header: 评估深度
Q: 快速模式（6 题核心）还是完整模式（22 题全覆盖）？
Options:
- A) 快速模式 — 每节核心题，共 8 题 (recommended) — 完成率高，适合日常迭代
- B) 完整模式 — 全部 24 题 — 覆盖全面，适合版本发布前
```

Store mode choice. Load `skills/survey/reference/auq-questions.json`.

**AUQ constraints**: `AskUserQuestion` allows max 4 options per question and max 4
questions per call. The question bank respects this — questions with more than 4
choices (like the E section wishlist) are split into sub-questions (e1, e1b).

**Brand prefix**: Every AUQ `header` field MUST start with `mh:` (meta-harness).
This makes the survey skill visible as the source during terminal QA. Examples:
`mh: QA Entry`, `mh: 配色`, `mh: 功能愿望单`. Max header length is 12 chars,
so keep the prefix concise — `mh: ` takes 4 chars, leaving 8 for the topic.

### Step 3: Section-by-section QA

Iterate through sections in order: A → B → C → D → E → F → G.

Sections A-F use fixed questions from the bank. Section G is dynamic — see below.

For each section:

1. **Section intro** (prose, 1 line): `── A. 整体视觉 ──`

2. **Ask questions**: For each question in the section (quick mode: only the first
   question per section), call `AskUserQuestion` with the question parameters from
   `auq-questions.json`.

   Read each question's `header`, `question`, `multiSelect`, and `options` directly
   from the JSON. Use them as the AskUserQuestion tool parameters. Add brief context
   about the current skill output before the question text when helpful.

3. **Record answer**: Parse the tool_result. Extract the selected label(s). Store
   in a running answers dict keyed by question ID.

4. **Save progress** after each answer:
   ```bash
   # Write current state to .metaharness/qa-state.json
   ```

**Pause check** (after sections C and E):

```
Header: 继续?
Q: 已完成 {n}/7 节。继续还是暂停？
Options:
- A) 继续 (recommended) — 一口气完成
- B) 暂停 — 保存进度，稍后继续
```

If pause: save state, say "进度已保存。下次运行 /survey 或说 '继续 QA' 来续接。" and exit.

**Section E special handling**: E1 is split into e1 and e1b (max 4 options per AUQ).
Both are `multiSelect: true`. After collecting both, ask as prose: "E2. 是否有其他改进建议？（直接输入，或说'跳过'）"

**Section F special handling**: After collecting F1 and F2, do NOT ask "continue
or pause" — proceed to Section G.

**Section G: Diff-Aware Review** — driven by the actual git diff. Full workflow
(probe → placeholders → 9 question patterns → remediation hooks) lives in
`skills/survey/reference/diff-aware-workflow.md`. Quick mode asks g4 (constraint
discovery). Full mode asks all 9.

Before Section G, run: `python skills/survey/scripts/probe-diff.py` — parses the
JSON output to populate placeholders. Skip G7/G8/G9 silently when their
respective file counts are 0 (no signal).

### Step 4: Archive

1. Summarize all answers as prose (2-3 lines highlighting key findings).

2. Write answers to JSON:
   ```bash
   python skills/survey/scripts/archive-auq-answers.py \
     --skill "{skill_name}" \
     --version "{version}" \
     --mode "{quick|full}" \
     --answers '{...JSON...}'
   ```

3. Delete `.metaharness/qa-state.json`.

4. Report: "反馈已归档到 .metaharness/{version}/inputs/qa-{skill}-{timestamp}.json"

### Step 5: Close the loop

```
Header: 下一步
Q: QA 完成。反馈已归档。接下来？
Options:
- A) 基于反馈启动下一轮迭代 (recommended) — 运行 proposer 改进技能
- B) 先查看反馈摘要 — 我想仔细看看结果再决定
- C) 结束 — 稍后手动处理
```

## HTML QA Survey (Async Fallback)

The static HTML form (`reference/qa-survey.html`) is preserved for:
- Async feedback (developer offline)
- Multi-reviewer collection
- Formal release QA with audit trail

Generate via:
```bash
python skills/survey/scripts/generate_survey.py --type qa --skill {name} --version {ver}
```

## Human-Loop Survey (HTML, Async Fallback)

The static HTML form (`reference/human-loop.html`) surveys the Meta-Harness
paradigm itself (not individual skills). Preserved for the same async scenarios.

## Design Principles

1. **Terminal-first** — Primary feedback path is the live AUQ dialogue. HTML is fallback.
2. **Lightweight** — Quick mode: 6 questions, ~3 minutes. No decision-brief ceremony.
3. **Mostly structured, always supplementable** — Every question is multiple-choice. Section E provides the open-text escape hatch.
4. **Search-set feedback** — All answers archived as `.metaharness/v{version}/inputs/`, feeding Meta-Harness Principle #3.

## Files

| File | Purpose |
|------|---------|
| `skill.md` | This file — skill definition with human-loop workflow |
| `reference/qa-survey.html` | Static HTML form — async QA |
| `reference/human-loop.html` | Static HTML form — paradigm survey |
| `reference/human-loop-design.md` | Design rationale document |
| `reference/auq-questions.json` | Question bank — 22 questions as AUQ parameters |
| `scripts/generate_survey.py` | HTML form generator |
| `scripts/archive-auq-answers.py` | AUQ answer → JSON archiver |

## Feedback Loop

```
skills/{name}/v{version} → deployed → human-loop AUQ (terminal, ~3 min)
    → answers archived in .metaharness/v{version}/inputs/
    → search-set signal drives next iteration
    → proposer reads feedback → improves skill
```
