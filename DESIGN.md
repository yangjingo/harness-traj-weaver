# DESIGN.md

Design tokens and visual language for all Meta-Harness HTML output. Sub-skills (traj, survey) embed these tokens in their templates — no CSS `@import`, templates are self-contained.

## Philosophy

**"Warm Precision"** — cream canvas, coral accents, dark sidebar, serif headings.

| Principle | Expression |
|-----------|-----------|
| Warmth | Cream canvas (`#faf9f5`), warm card surfaces, coral primary |
| Precision | Dark sidebar, JetBrains Mono for code, hairline borders |
| Breathing room | 8px–48px spacing scale, Cormorant Garamond headings |

## Color Tokens

```
--canvas:       #faf9f5   Page background
--surface-soft: #f5f0e8   Soft surface
--surface-card: #efe9de   Card backgrounds
--surface-dark: #181715   Sidebar, dark panels
--hairline:     #e6dfd8   Borders, dividers
--ink:          #141413   Headings
--body:         #3d3d3a   Body text
--muted:        #6c6a64   Secondary text
--primary:      #cc785c   Coral — CTAs, user turns, skill-exec blocks
--accent-teal:  #5db8a6   Teal — assistant, skill calls
--accent-amber: #e8a55a   Amber — tool calls, warnings
--success:      #5db872   Green
--error:        #c64545   Red
```

## Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| h1 | Cormorant Garamond | 42px | 400 |
| h2 | Cormorant Garamond | 30px | 400 |
| h3 | Cormorant Garamond | 24px | 400 |
| Body | Inter | 15px | 400 |
| Code | JetBrains Mono | 13px | 400 |
| Labels | Inter | 11px, 500 | uppercase |

## Spacing

`--sp-xs: 8px` / `--sp-sm: 12px` / `--sp-md: 16px` / `--sp-lg: 24px` / `--sp-xl: 32px` / `--sp-xxl: 48px`

## Rhythm Rules

1. **Coral is scarce** — `--primary` only for CTAs, user-turn markers, skill-exec blocks. Never as fill.
2. **Dark sidebar anchors** — Left nav always `--surface-dark`.
3. **Cards alternate** — Surface cards on canvas, dark cards for emphasis, coral only at end.
4. **Tables breathe** — Hairline borders, hover to `--surface-soft`, no zebra striping.