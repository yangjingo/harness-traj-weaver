# Diff-Aware QA Workflow (Section G)

Drives code-change-aware evaluation questions from the actual git diff. Borrows
patterns from gbrain's state-probe → remediate approach. No fixed checklist can
capture "was this rename correct?" or "should we have deleted that file?" as
precisely as reading the actual changes.

## G.0 State Probe

```bash
python skills/survey/scripts/probe-diff.py
```

Outputs JSON with all placeholder values: file counts by change type, shortstat,
test/dep/security file detection, branch, design doc existence.

Key principle from gbrain: **detect state first, then ask questions shaped by
that state.** If `del_count > 0`, G1 surfaces deletion risk. If `test_count == 0`,
G7 asks whether that's intentional. If `dep_count > 0`, G8 flags dependency review.

## G.1 Placeholder Table

Values from `probe-diff.sh` JSON populate these placeholders in Section G questions:

| Placeholder | JSON Field | Example |
|-------------|-----------|---------|
| `{new_count}` | `.new_count` | "5" |
| `{mod_count}` | `.mod_count` | "4" |
| `{del_count}` | `.del_count` | "0" |
| `{shortstat}` | `.shortstat` | "4 files changed, +368/-59" |
| `{test_count}` | `.test_count` | "0" |
| `{test_files_changed}` | `.test_files_changed` | "(none)" |
| `{dep_count}` | `.dep_count` | "0" |
| `{dep_files_changed}` | `.dep_files_changed` | "(none)" |
| `{sec_count}` | `.sec_count` | "0" |
| `{sec_files_changed}` | `.sec_files_changed` | "(none)" |
| `{new_files}` | `.new_files` | "archive.py, probe.sh" |
| `{modified_files}` | `.modified_files` | "skill.md, changelog.md" |
| `{key_decisions_summary}` | (from conversation) | "AUQ over HTML; 4-option cap; dynamic G-section" |
| `{integration_points}` | (from diff analysis) | "traj/skill.md, CLAUDE.md" |
| `{discovered_constraints}` | (from implementation) | "AUQ max 4 opts; no free-text input" |
| `{new_interfaces}` | `.new_files` + `.modified_files` | "probe-diff.sh, archive-auq-answers.py --qbv" |
| `{implemented}` | (from design doc vs diff) | "Terminal AUQ, 27-question bank, probe script" |
| `{not_implemented}` | (from design doc vs diff) | "AUTO_DECIDE, trend dashboard" |

## G.2 Question Patterns (9 types)

Each G-section question uses a specific pattern borrowed from gbrain's state-aware
interrogation. Nine lenses on the diff, each surfacing a different dimension of
code change quality.

---

### G1 — Add/Modify/Delete Ratio
**Pattern**: *state-probe → ratio-check → remediate*

Before asking: run the probe, count files by change type. If `{del_count}` > 0:
offer an option about deletion risk. If `{new_count}` is 0: rephrase the question
to focus on modification-only changes.

Key framing: "You added X files and changed Y lines. Did you add the right amount
of surface area?" Same instinct as gbrain's "which engine do you need?" — match
evaluation to actual state, not a hypothetical.

---

### G2 — Design Decision Validation
**Pattern**: *decision-recall → implementation-check*

Before asking: list 2-3 key design choices from the iteration. Present concretely:
- Good: "AUQ terminal-first, HTML as fallback"
- Bad: "we chose an architecture"

If design doc exists, cross-reference: did implementation follow the design? If
not, flag the divergence as a separate option.

---

### G3 — Integration Surface Health
**Pattern**: *touch-point audit*

Before asking: trace every file that bridges new and old code. List concrete paths.
Ask: are these the right touch points? Would fewer be better?

If integration surface is 0 (purely additive), skip and ask: "This iteration is
purely additive — is that correct, or should it have replaced existing code?"

---

### G4 — Constraint Discovery Log
**Pattern**: *surprise capture*

Before asking: list every platform limit, edge case, or "I didn't expect that"
moment. For gbrain: "PgBouncer transaction-mode pooling breaks prepared statements."
For us: "AskUserQuestion has a 4-option cap."

Purpose: **capture discoveries before they evaporate from working memory.**
If no constraints discovered, use option D: "还没发现约束."

---

### G5 — Naming & Interface Ergonomics
**Pattern**: *fresh-eyes naming check*

Before asking: list every new public name — file names, function signatures, CLI
flags, JSON keys. Ask: would a developer who didn't write this understand these
names on first encounter?

Cheapest time to rename. Once other code depends on these interfaces, renames
become breaking changes.

---

### G6 — Design-to-Implementation Gap
**Pattern**: *intent-vs-reality diff*

Before asking: compare design doc against actual build. List `{implemented}` and
`{not_implemented}` side by side. If no design doc, compare against stated intent
from the conversation.

"Did we ship what we said we'd ship?" For gbrain: comparing `/setup-gbrain`
Step 2's promised paths against what the installer actually handles.

---

### G7 — Test Coverage Delta
**Pattern**: *test-gap detection*

Before asking: check `{test_count}` from probe. If 0 and code changed: ask whether
that's intentional or an oversight. If >0: ask whether the right tests were updated.
Heuristic: files matching `test`, `spec`, `__tests__`, `eval` in path.

---

### G8 — Dependency Surface Change
**Pattern**: *dep-expansion check*

Before asking: check `{dep_count}` from probe. If >0: flag for review. Heuristic:
files matching `package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`,
`Gemfile`, `Dockerfile`, `Makefile`.

---

### G9 — Security Surface Change
**Pattern**: *attack-surface audit*

Before asking: check `{sec_count}` from probe. If >0: ask whether the change
introduces new attack surface. Heuristic: files matching `auth`, `token`, `secret`,
`credential`, `.env`, `config.yaml`, `settings.json`, `cert`, `key.pem`.

---

## G.3 Question Flow

After state probe, ask G-section questions in order. Quick mode picks g4
(constraint discovery — highest leverage, captures perishable info). Full mode
asks all 9.

**Remediation hook**: after each G-section answer that indicates a problem (e.g.,
G2 = "needs reconsideration", G3 = "coupling too tight"), offer a one-line
remediation before moving to the next question. Don't implement — just name what
would fix it. Pattern from gbrain Step 1.5: detect → classify → offer concrete
next action.

**One-way door warning**: for G2 (design decision reversal) and G6 (scope gap),
if the user indicates a significant problem, label the remediation's blast radius:
- "This is a one-way door — renaming `{new_interfaces}` will break nothing yet,
  but once integrated it's forever."
- "This is two-way — we can always add `{not_implemented}` in the next iteration."

**Silent skip**: if `{test_count}` is 0 AND `{dep_count}` is 0 AND `{sec_count}`
is 0, skip G7/G8/G9 entirely — they add no signal when there's nothing to review.
