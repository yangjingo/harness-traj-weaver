# UX.md

Component patterns, animations, and layout conventions for Meta-Harness HTML output.
Design philosophy and tokens live in `DESIGN.md`.

## Sidebar Navigation (TOC)

Fixed left panel, dark surface, collapsible. Used by traj.

```css
.side-toc {
  position: fixed; left: 0; top: 0; bottom: 0;
  width: 260px; background: var(--surface-dark);
  transition: width 0.25s; z-index: 100;
}
.toc-collapsed .side-toc { width: 40px; overflow: hidden; }
```

- Collapse toggle: 22x22px button, top-right, coral hover
- Items: 12px, gap 6px, coral hover highlight
- Color-coded by type: user=coral, assistant=teal, think=teal with left-border, bash/tool=amber with left-border, write=coral with left-border
- Active item: coral background `rgba(204,120,92,0.2)`
- Mobile: hidden below 860px

## Stats Bar

Horizontal stat cards in a flex row. Used by traj.

```css
.stats {
  display: flex; gap: 20px; flex-wrap: wrap;
  padding: 16px 20px; background: var(--surface-card);
  border-radius: 12px;
}
.stat-num {
  font: 26px 'Cormorant Garamond', serif; color: var(--ink);
}
.stat-label {
  font: 11px 'Inter', sans-serif; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.5px;
}
```

## Timeline (Turn-Based Folding)

Vertical timeline with left rail marker. Turn headers are clickable toggles.

```css
.timeline { position: relative; padding-left: 32px; }
.timeline::before {
  content: ''; position: absolute; left: 11px; top: 0; bottom: 0;
  width: 2px; background: var(--hairline);
}
```

- Turn marker: 22px circle on rail, open state fills with `var(--muted)`
- Turn header: flex row with chevron, role badge, label, time. Hover → `var(--surface-soft)`
- Turn body: hidden by default, `display: block` when `.open`
- Chevron: rotates 90deg on open, `transition: transform 0.2s`
- Click header → toggle `.open` class on `.tl-turn`

## Content Blocks

Each message block within a turn body gets a distinct left-border and background.

| Block | Border | Background |
|-------|--------|------------|
| Thinking | `accent-teal` 3px | `rgba(93,184,166,0.08)` |
| Text | none | `surface-card` |
| Tool/Bash | `accent-amber` 3px | `surface-card` |
| Skill call | `accent-teal` 3px | `rgba(93,184,166,0.06)` |
| Skill read | `accent-amber` 3px | `rgba(232,165,90,0.06)` |
| Skill exec | `primary` 3px | `rgba(204,120,92,0.06)` |

```css
.block {
  margin-bottom: 8px; border-radius: 8px; padding: 10px 14px;
  scroll-margin-top: 80px;
}
```

- Tool name: JetBrains Mono 13px in a colored pill background
- Tool output: dark surface, max-height 400px, scroll overflow
- Thinking text: muted color, pre-wrap, collapsed behind "Show full thinking" details

## Collapsible Details

```css
details summary { cursor: pointer; color: var(--accent-teal); }
details summary::before { content: '\25b8 '; }
details[open] summary::before { content: '\25be '; }
details summary:hover { color: var(--primary); }
```

## Flash Highlight Animation

When navigating to a block via TOC click:

```css
@keyframes block-flash {
  0%   { background: rgba(204,120,92,0.15); box-shadow: 0 0 0 4px rgba(204,120,92,0.25); }
  25%  { background: rgba(204,120,92,0.08); box-shadow: 0 0 0 2px rgba(204,120,92,0.15); }
  100% { background: transparent; box-shadow: none; }
}
.block.flash-highlight { animation: block-flash 1.8s ease-out forwards; }
```

Coral pulse fades over 1.8s. Applied via JS when TOC item clicked:
```js
el.classList.add('flash-highlight');
setTimeout(() => el.classList.remove('flash-highlight'), 1800);
```

## Responsive Breakpoints

```css
@media (max-width: 860px) {
  .side-toc { display: none; }
  body { padding-left: 32px; }
}
```

Single breakpoint: hide sidebar below 860px. No mobile TOC alternative yet.

## Source Footer

```css
.source-path {
  margin-top: 40px; padding: 12px 16px;
  background: var(--surface-dark); border-radius: 8px;
  font: 12px 'JetBrains Mono', monospace; color: #8a8680;
}
```

## Conventions

1. **Self-contained HTML** — No `@import`, no external CSS. Tokens inlined in `<style>`.
2. **Single breakpoint** — 860px. Sidebar hidden, body padding collapses.
3. **No JS framework** — Vanilla JS only. `classList.toggle`, `scrollIntoView`, `setTimeout`.
4. **Transitions over animations** — Prefer `transition: 0.2s` on hover/state changes. Reserve `@keyframes` for one-shot events (flash highlight).
5. **Coral is scarce** — `--primary` only for user turns, skill-exec, and CTA. Never as fill.
