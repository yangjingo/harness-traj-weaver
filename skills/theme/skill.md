---
name: theme
version: "0.1.0"
description: Theme CSS tokens and visual language for Meta-Harness. Provides the canonical color palette, typography scale, spacing rhythm, and component patterns used across all sub-skills (traj, metric). Inspired by the Anthropic brand aesthetic — warm cream canvas, coral accents, dark sidebar, serif headings.
---

## Overview

This skill defines the **visual language** for all Meta-Harness HTML output. It is not a CSS framework — it is a set of CSS custom properties (design tokens) and composition rules that ensure visual consistency across trajectory views, evaluation dashboards, and any future HTML artifacts.

## Design Philosophy

**"Warm Precision"** — The aesthetic blends:
- **Warmth**: Cream canvas (`#faf9f5`), card surfaces with subtle warmth, coral primary accent
- **Precision**: Dark sidebar for navigation, JetBrains Mono for code, structured tables with hairline borders
- **Breathing room**: Generous spacing (8px–48px scale), Cormorant Garamond headings with negative letter-spacing

## Color Palette

| Token | Hex | Role |
|---|---|---|
| `--canvas` | `#faf9f5` | Page background |
| `--surface-soft` | `#f5f0e8` | Soft surface variant |
| `--surface-card` | `#efe9de` | Card backgrounds |
| `--surface-dark` | `#181715` | Sidebar, dark panels, footer |
| `--hairline` | `#e6dfd8` | Table borders, dividers |
| `--ink` | `#141413` | Primary text, headings |
| `--body` | `#3d3d3a` | Body text |
| `--muted` | `#6c6a64` | Secondary text, labels |
| `--primary` | `#cc785c` | **Coral** — primary accent, CTAs, user emphasis |
| `--accent-teal` | `#5db8a6` | **Teal** — success, assistant, skill calls |
| `--accent-amber` | `#e8a55a` | **Amber** — warnings, tool calls, file reads |
| `--success` | `#5db872` | Green — success states |
| `--error` | `#c64545` | Red — errors, critical issues |

## Typography

| Element | Font | Size | Weight |
|---|---|---|---|
| h1 | Cormorant Garamond | 42px | 400 |
| h2 | Cormorant Garamond | 30px | 400 |
| h3 | Cormorant Garamond | 24px | 400 |
| h4 | Cormorant Garamond | 20px | 500 |
| Body | Inter | 15px | 400 |
| Code | JetBrains Mono | 13px | 400 |
| Labels | Inter | 11–12px | 500, uppercase |

## Spacing Scale

| Token | Value |
|---|---|
| `--sp-xs` | 8px |
| `--sp-sm` | 12px |
| `--sp-md` | 16px |
| `--sp-lg` | 24px |
| `--sp-xl` | 32px |
| `--sp-xxl` | 48px |

## Rhythm Rules

1. **Coral is scarce** — Use `--primary` only for CTAs, user-turn markers, and skill-exec blocks. Never as a background fill or decoration.
2. **Dark sidebar anchors** — Left navigation is always `--surface-dark`. The dark anchor creates visual stability.
3. **Cards alternate** — Surface cards sit on the canvas, dark cards interrupt for emphasis, coral only at the end (CTA).
4. **Tables breathe** — Hairline borders, hover rows to `--surface-soft`, no zebra striping.

## Reference

The canonical CSS token file is at `reference/design-tokens.css`. Sub-skills import these tokens by embedding them in their own CSS (no CSS `@import` — templates are self-contained HTML files).
