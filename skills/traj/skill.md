---
name: traj
version: "0.1.0"
description: Claude Code session trajectory visualization. Reads JSONL session files and generates interactive HTML timeline views with TOC navigation, thinking blocks, tool call tracking, and skill usage highlighting. Designed for Meta-Harness trace-level reasoning.
---

## Overview

`scripts/generate_traj.py` reads a Claude Code session JSONL file and produces a self-contained `traj.html` with:

- **Side TOC** — fixed left panel with quick-jump navigation by conversation turn
- **Stats bar** — turn count, skill calls, tool calls, thinking blocks, file reads/writes
- **Timeline view** — chronological conversation with color-coded content blocks
- **Skill highlighting** — Skill/Agent calls, skill file reads, and skill file edits each get distinct visual treatment

## Design Philosophy

This skill embodies Meta-Harness Principle #2: **Trace-level reasoning**. Instead of compressed summaries, the trajectory view exposes raw conversation structure — thinking blocks, tool inputs/outputs, and skill interactions — so the proposer can diagnose failures directly from execution traces.

## Templates

| File | Purpose |
|---|---|
| `reference/traj.css` | Full CSS with Anthropic Design System tokens + timeline styles |
| `reference/traj-template.html` | HTML skeleton with `$variable` placeholders for Python `string.Template` |

## Usage

```bash
python skills/traj/scripts/generate_traj.py \
  --input ~/.claude/projects/<project>/<session>.jsonl \
  --output traj.html
```

## Data Format

Input is Claude Code JSONL where each line is a JSON object:

- `type: "user"` → `message.content` (text or tool_result blocks)
- `type: "assistant"` → `message.content[]` with thinking/text/tool_use blocks
- Tool calls are classified: Skill/Agent calls, skill-reads (Read on skill files), skill-execs (Edit/Write on skill files)

## Content Block Rules

| Block | Display Strategy |
|---|---|
| Thinking | First 3000 chars shown, overflow collapsed behind "Show full thinking" |
| Text | Direct display, truncated at 2000 chars |
| Tool Use | Tool name + input summary (300 chars), output in collapsible `<details>` |
| Skill/Agent | Teal left-border, tool name in teal |
| Skill-read | Amber left-border (Read on skill.md/src/skills/) |
| Skill-exec | Coral left-border (Edit/Write on skill.md/src/skills/) |

## Color Tokens

From the theme tokens (see `../theme/reference/design-tokens.css`):

| Token | Hex | Usage |
|---|---|---|
| `canvas` | `#faf9f5` | Page background |
| `surface-dark` | `#181715` | Side TOC, source footer |
| `primary` | `#cc785c` | Coral — user turns, skill-exec blocks |
| `accent-teal` | `#5db8a6` | Assistant turns, skill calls |
| `accent-amber` | `#e8a55a` | Tool calls, skill-reads |
