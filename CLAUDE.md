# CLAUDE.md

## Documentation Sync

`README.md` (English) and `README-ZH.md` (Chinese) must be kept in sync. Any change to one requires the same change in the other.

## Commit Workflow

### Before Every Commit

Run through this checklist and remind the user:

1. **Docs** — Are README.md and README-ZH.md in sync?
2. **CHANGELOG** — Are user-facing changes recorded under `[Unreleased]`?
3. **Eval** — Have benchmark / eval results been updated if applicable?

### On Release (version bump)

When cutting a new version release:

- Move `[Unreleased]` entries to a new dated version section (e.g., `## [0.1.0] — 2026-05-23`)
- Ensure both README.md and README-ZH.md reflect the new version

## Skill Routing

When the user's request matches an available skill, invoke it via the Skill tool.
When in doubt, invoke the skill.

Key routing rules:
- Generate trajectory / visualize session → invoke /traj
- QA / evaluate output / "does this look good" → invoke /survey (human-loop mode)
- Review skill output quality → invoke /survey (human-loop mode)
- Collect feedback after iteration → invoke /survey (human-loop mode)
