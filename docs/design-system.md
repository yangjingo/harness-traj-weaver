# Design System: DESIGN.md + UX.md

Meta-Harness separates design into two layers: philosophy and implementation.

## Why Two Files

Most projects either have a monolithic design doc (everything in one place) or no
design doc at all. The split addresses a real tension: design decisions and
implementation patterns evolve at different speeds.

| Layer | File | Cadence | Audience |
|-------|------|---------|----------|
| Philosophy | `DESIGN.md` | Rarely changes (per major version) | Anyone contributing to any skill |
| Implementation | `UX.md` | Changes with each skill iteration | Skill developers writing HTML/CSS |

A color palette change is a design decision — it goes in DESIGN.md and affects every
skill. A new animation pattern for block highlighting is an implementation detail —
it goes in UX.md and may only apply to traj.

## DESIGN.md — Design Philosophy

Purpose: answer "what does Meta-Harness look and feel like?"

Contents:
- **Philosophy** — "Warm Precision": cream canvas, coral accents, dark sidebar
- **Color Tokens** — 14 CSS custom properties with semantic roles
- **Typography** — font stack, sizes, weights for each element role
- **Spacing** — 6-step scale (8px–48px)
- **Rhythm Rules** — 4 constraints on how tokens are used (e.g., "Coral is scarce")

What DESIGN.md does NOT contain:
- CSS code or file paths
- Component markup
- Animation keyframes
- Responsive breakpoints
- JavaScript patterns

## UX.md — Implementation Patterns

Purpose: answer "how do I build a Meta-Harness UI component?"

Contents:
- **Sidebar Navigation** — fixed dark panel, collapse animation, color-coded items
- **Stats Bar** — horizontal flex row with serif numbers
- **Timeline** — vertical rail, turn folding, chevron rotation
- **Content Blocks** — 6 block types with distinct left-borders
- **Collapsible Details** — `<details>` styling with triangle icons
- **Flash Highlight** — coral pulse animation for TOC navigation
- **Responsive** — single 860px breakpoint
- **Conventions** — self-contained HTML, no frameworks, transitions over animations

Each pattern includes the actual CSS. A developer can copy from UX.md directly into
a template.

## Relationship

```
DESIGN.md          UX.md               Template CSS
──────────         ──────              ────────────
Philosophy    →    Component     →     Inlined in
Colors              Patterns            <style> tags
Typography          Animations          of each HTML
Spacing             Layout              output file
Rules               Conventions
```

DESIGN.md defines the tokens. UX.md shows how to use them. Templates consume both.

When a new skill needs HTML output:
1. Read DESIGN.md for the color palette and typography
2. Read UX.md for component patterns that match your needs
3. Copy patterns and tokens into a self-contained `<style>` block
4. No `@import`, no external CSS files

## Evolution

| Change Type | Goes In | Example |
|-------------|---------|---------|
| New color added | DESIGN.md | Add `--accent-purple` |
| Spacing scale adjusted | DESIGN.md | `--sp-xl` from 32px to 36px |
| New component pattern | UX.md | Add "Modal Dialog" section |
| Animation timing tweak | UX.md | Flash highlight from 1.8s to 2.0s |
| Token used in a template | Neither | Just use `var(--primary)` in CSS |
| Breaking layout change | Both | DESIGN.md rhythm rules + UX.md component update |
