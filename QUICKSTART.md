# Quickstart for AI Agents

Install the `harness-traj-weaver` skill in any Claude Code or Codex environment.

## Install

```bash
git clone https://github.com/yangjing/harness-traj-weaver.git ~/.claude/skills/harness-traj-weaver
```

## Verify

```bash
cat ~/.claude/skills/harness-traj-weaver/SKILL.md
```

## What This Skill Does

Grants the agent a meta-harness loop:

1. **Observe** — Read prior traces and failures from the filesystem
2. **Diagnose** — Inspect raw code and trace data, not summaries
3. **Propose** — Edit based on traces, not aggregate scores
4. **Evaluate** — Validate against the search set
5. **Iterate** — Write results back to filesystem, repeat

No persistent memory. No fixed scaffold. Just the filesystem.

## Filesystem Layout

The skill creates and reads from this structure:

```
.metaharness/
  v{version}/
    inputs/       — archived session JSONL files
    outputs/      — generated artifacts
  plan-trigger.json — trigger for next iteration cycle
```

## Usage in Conversation

Once installed, the skill auto-loads. The agent can be directed with:

> Run the harness over the last 3 failed examples, diagnose them from their traces, and propose targeted edits.

The agent reads `.metaharness/`, diagnoses failures, edits candidate files, evaluates against the search set, and writes feedback back to disk.
