---
name: metric
version: "0.1.0"
description: Meta-Harness evaluation metrics dashboard. Generates interactive HTML dashboard from harness evaluation data — pipeline timing, parse quality, benchmark comparisons, and artifact inspection. Template-driven rendering with Anthropic Design System styling.
---

## Overview

`scripts/generate_dashboard.py` (TBD) reads harness evaluation data and produces a self-contained `dashboard.html` with:

- **Sidebar navigation** — fixed dark sidebar with section quick-jump
- **Overview** — Pipeline flow visualization + stats cards + kanban summary
- **Pipeline Timing** — phase timing table, distribution bars, per-file timing
- **Per-File Results** — filterable file grid with MD preview overlay
- **Benchmark** — side-by-side parser comparison tables
- **Parse Report** — anomaly statistics by severity and type
- **Artifacts** — output file listing with image/caption preview

## Design Tokens

Uses the theme tokens (see `../theme/reference/design-tokens.css`).

Key tokens:
| Token | Hex | Usage |
|---|---|---|
| `canvas` | `#faf9f5` | Page background, warm cream |
| `surface-dark` | `#181715` | Sidebar, dark panels |
| `primary` | `#cc785c` | Coral — CTAs, user emphasis |
| `accent-teal` | `#5db8a6` | Success, code highlights |
| `accent-amber` | `#e8a55a` | Warnings, tool calls |

## Templates

| File | Purpose |
|---|---|
| `reference/dashboard.css` | Full CSS with all component styles |
| `reference/dashboard.js` | Client interactivity: navigation, MD/image preview, filtering |
| `reference/dashboard-template.html` | HTML skeleton with `$variable` placeholders |

## Meta-Harness Integration

This dashboard is the **evaluation surface** for Meta-Harness Principle #3 (Search-set feedback). Harness candidates are evaluated against the search set, and results flow into this dashboard for visual inspection — never exposing test-set data.

## Page Structure

1. **Overview** — Pipeline Flow + Stats + Kanban cards
2. **Pipeline Timing** — Phase/file/type timing tables
3. **Per-File Results** — Filterable results grid with MD preview
4. **Benchmark** — Parser comparison (quality + performance)
5. **Parse Report** — Anomaly statistics + detail list
6. **Changelog** — Version history
7. **Artifacts** — Output file listing with preview overlays
