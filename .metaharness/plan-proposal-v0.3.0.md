# Plan Proposal — v0.3.0

Generated from `.metaharness/plan-trigger.json` (v0.2.0, commit e69da76).

## State Snapshot (v0.2.0)

**Done:**
- Output isolation: `evals/` → `.metaharness/v{version}/`
- Agent one-click install in README
- pre-commit hook: metric + human-loop generation
- post-commit hook: session archive + plan trigger
- pre-push hook: written, not yet tested
- install.sh: skill registration + hook setup
- Session auto-archive via `$CLAUDE_CODE_SESSION_ID`
- Version detection from `changelog.md`

**Gaps:**
- No `.gitignore` — `.metaharness/` visible in git status
- Pre-push hook untested
- ROADMAP.md not committed
- CHANGELOG v0.2.0 missing post-v0.2.0 work (hooks, QA, plan trigger)
- Human-loop feedback collected but not closing the loop (plan should read it)
- No CI / self-check integration

## Proposed v0.3.0

### P0 — Complete the review loop
- **Read feedback** from `.metaharness/v0.2.0/outputs/meta-harness-feedback-*.json`
- **Act on it**: Q1=d (大面积改动) → split future work into smaller commits
- **Act on it**: Q3=c (部分遗漏) → sync docs before next release

### P1 — Hygiene
- Add `.gitignore` with `.metaharness/`
- Commit `ROADMAP.md`
- Update `CHANGELOG.md` with all v0.2.0 work

### P2 — Close the loop
- `post-commit` → plan trigger → plan proposal (this file)
- Plan should be reviewed by human before v0.3.0 branch starts
- Consider: `scripts/plan.sh` that reads trigger + feedback → generates proposal

### P2 — Pre-push validation
- Test `hooks/pre-push` on actual push
- Ensure it generates human-loop + traj for the push range

## Questions for Human Review

1. v0.3.0 优先做 P0（闭环）还是 P1（卫生）？
2. ROADMAP.md 的内容需要更新吗？
3. 是否需要把 plan 模式从 hook 里独立出来成为 `scripts/plan.sh`？
