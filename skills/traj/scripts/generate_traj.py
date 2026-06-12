#!/usr/bin/env python3
"""generate_traj.py — Parse Claude Code JSONL session and produce traj.html.

Usage:
  python generate_traj.py --input session.jsonl [--output traj.html]
"""

import json
import os
from datetime import datetime
from string import Template
from html import escape

SKILL_KEYWORDS = ['skill.md', 'claude.md', 'src/skills/', 'src/prompts/',
                   '.claude/skills/', 'SKILL.md', 'CLAUDE.md']
MODEL_ENV_KEYS = ['MODEL', 'CLAUDE_CODE_MODEL', 'ANTHROPIC_MODEL', 'OPENAI_MODEL']

# TOC action types: (css_class, icon, label)
def _assistant_action(blocks):
    """Determine the primary action type from assistant content blocks.
    Returns (css_class, icon, label, content_snippet)."""
    if not isinstance(blocks, list):
        return ('toc-assistant', '&#9654;', 'Assistant', '')
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if block.get('type') == 'thinking':
            t = (block.get('thinking', '') or '')[:5].replace('\n',' ').strip()
            return ('toc-think', '&#9674;', 'Thinking', t)
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if block.get('type') == 'tool_use':
            name = (block.get('name', '') or '').lower()
            inp = block.get('input', {})
            if isinstance(inp, dict):
                snip = (inp.get('command', inp.get('description', inp.get('file_path', inp.get('path', '')))) or '')[:5].replace('\n',' ').strip()
            else:
                snip = (str(inp) or '')[:5].replace('\n',' ').strip()
            if name == 'bash':
                return ('toc-bash', '&#9655;', 'Bash', snip)
            if name in ('skill', 'agent'):
                return ('toc-skill', '&#9670;', 'Skill', snip)
            if name == 'read':
                return ('toc-read', '&#9671;', 'Read', snip)
            if name in ('edit', 'write'):
                return ('toc-write', '&#9998;', 'Write', snip)
            label = block.get('name', 'Tool')
            return ('toc-tool', '&#9881;', label, snip)
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if block.get('type') == 'text':
            t = (block.get('text', '') or '')[:5].replace('\n',' ').strip()
            return ('toc-text', '&#9654;', 'Text', t)
    return ('toc-assistant', '&#9654;', 'Assistant', '')


def load_template(name):
    path = os.path.join(os.path.dirname(__file__), '..', 'reference', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def classify_tool(tool_name, tool_input):
    """Classify a tool call for visual styling."""
    name = (tool_name or '').lower()
    inp = json.dumps(tool_input) if isinstance(tool_input, dict) else str(tool_input)
    if name in ('skill', 'agent'):
        return 'skill'
    if name in ('read',):
        for kw in SKILL_KEYWORDS:
            if kw.lower() in inp.lower():
                return 'skill-read'
        return None
    if name in ('edit', 'write'):
        for kw in SKILL_KEYWORDS:
            if kw.lower() in inp.lower():
                return 'skill-exec'
        return None
    return None


def fmt_time(ts):
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return dt.strftime('%H:%M:%S')
    except Exception:
        return ''


def parse_timestamp(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception:
        return None


def fmt_datetime(ts):
    dt = parse_timestamp(ts)
    if not dt:
        return ''
    return dt.astimezone().strftime('%Y-%m-%d %H:%M:%S')


def fmt_duration(seconds):
    if seconds is None or seconds < 0:
        return 'Unknown'
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f'{hours:02d}:{minutes:02d}:{secs:02d}'
    return f'{minutes:02d}:{secs:02d}'


def derive_model_name(records):
    for key in MODEL_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            return value

    for rec in records:
        msg = rec.get('message', {})
        model = msg.get('model') if isinstance(msg, dict) else None
        if model:
            return str(model)

    return 'Unknown'


def build_session_meta(records):
    timestamps = [rec.get('timestamp') for rec in records if rec.get('timestamp')]
    start_ts = timestamps[0] if timestamps else ''
    end_ts = timestamps[-1] if timestamps else ''
    start_dt = parse_timestamp(start_ts)
    end_dt = parse_timestamp(end_ts)
    duration_seconds = int((end_dt - start_dt).total_seconds()) if start_dt and end_dt else None
    return {
        'model_name': derive_model_name(records),
        'session_start': fmt_datetime(start_ts) or 'Unknown',
        'session_end': fmt_datetime(end_ts) or 'Unknown',
        'session_duration': fmt_duration(duration_seconds),
    }


def load_jsonl(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _has_user_text(rec):
    """Check if a user record has actual text content (not just tool results)."""
    if rec.get('type') != 'user':
        return False
    msg = rec.get('message', {})
    content = msg.get('content', '')
    if isinstance(content, str):
        return bool(content.strip())
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'tool_result':
                    continue
                if item.get('text'):
                    return True
            elif isinstance(item, str) and item.strip():
                return True
    return False


def _get_user_text(rec):
    """Extract user text from a user record."""
    msg = rec.get('message', {})
    content = msg.get('content', '')
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'tool_result':
                    continue
                if item.get('text'):
                    parts.append(str(item['text']))
            elif isinstance(item, str):
                parts.append(item)
        return ' '.join(parts).strip()
    return ''


def _is_empty_block(block):
    """Check if a content block has no meaningful content."""
    if not isinstance(block, dict):
        return True
    bt = block.get('type', '')
    if bt == 'thinking':
        return not (block.get('thinking', '') or '').strip()
    if bt == 'text':
        return not (block.get('text', '') or '').strip()
    if bt == 'tool_use':
        return not block.get('name', '')
    return True


def _render_assistant_block(block, records, rec_idx, stats, block_id=''):
    """Render a single assistant content block to HTML. Updates stats dict."""
    if not isinstance(block, dict):
        return ''
    btype = block.get('type', '')

    if btype == 'thinking':
        text = (block.get('thinking', '') or '').strip()
        if not text:
            return ''  # skip empty thinking blocks
        stats['thinking'] += 1
        inner = (f'<div class="block-label">Thinking</div>'
                 f'<div class="thinking-text">{escape(text[:3000])}</div>')
        if len(text) > 3000:
            inner += (f'<details><summary>Show full thinking ({len(text)} chars)</summary>'
                      f'<div class="thinking-full">{escape(text)}</div></details>')
        return f'<div class="block block-thinking" id="{block_id}">{inner}</div>'

    if btype == 'text':
        text = (block.get('text', '') or '').strip()
        if not text:
            return ''  # skip empty text blocks
        return f'<div class="block block-text" id="{block_id}">{escape(text[:2000])}</div>'

    if btype == 'tool_use':
        tool_name = block.get('name', 'unknown')
        tool_input = block.get('input', {})
        stats['tool_use'] += 1
        if tool_name.lower() in ('skill', 'agent'):
            stats['skill_calls'] += 1
        if tool_name.lower() == 'read':
            stats['read_files'] += 1
        if tool_name.lower() in ('edit', 'write'):
            stats['write_files'] += 1

        classification = classify_tool(tool_name, tool_input)
        block_class = {'skill': 'block-skill', 'skill-read': 'block-skill-read',
                       'skill-exec': 'block-skill-exec'}.get(classification, 'block-tool')

        if isinstance(tool_input, dict):
            desc = tool_input.get('description', tool_input.get('file_path', ''))
            input_summary = (str(desc) if desc else escape(json.dumps(tool_input, ensure_ascii=False)))[:300]
        else:
            input_summary = escape(str(tool_input))[:300]

        file_indicator = ''
        if isinstance(tool_input, dict):
            fp = tool_input.get('file_path', tool_input.get('path', ''))
            if fp:
                file_indicator = f'<span class="tool-files">{escape(str(fp))}</span>'

        # Find tool output (look at next record)
        output_html = ''
        if rec_idx + 1 < len(records) and records[rec_idx + 1].get('type') == 'user':
            next_msg = records[rec_idx + 1].get('message', {})
            next_content = next_msg.get('content', '')
            if isinstance(next_content, list):
                for item in next_content:
                    if isinstance(item, dict) and item.get('type') == 'tool_result':
                        rc = item.get('content', '')
                        if isinstance(rc, list):
                            rt = ''.join(str(r.get('text', '')) for r in rc if isinstance(r, dict))
                        elif isinstance(rc, str):
                            rt = rc
                        else:
                            rt = str(rc)
                        if rt.strip():
                            output_html = (f'<details><summary>Tool output</summary>'
                                           f'<div class="tool-output">{escape(rt[:2000])}</div></details>')

        return (f'<div class="block {block_class}" id="{block_id}">'
                f'<div class="tool-header"><span class="tool-name">{escape(tool_name)}</span>{file_indicator}</div>'
                f'<div class="tool-input">{escape(input_summary)}</div>{output_html}</div>')

    return ''


def build_toc_and_timeline(records):
    """Build TOC entries and timeline HTML, grouped by conversation turn."""
    toc_entries = []
    timeline_blocks = []
    stats = {'user_turns': 0, 'skill_calls': 0, 'user_interventions': 0,
             'read_files': 0, 'write_files': 0, 'tool_use': 0, 'thinking': 0}

    # Group records into turns: (user_rec, [assistant_recs...])
    turns = []
    i = 0
    while i < len(records):
        rec = records[i]
        if _has_user_text(rec):
            user_rec = rec
            i += 1
            assistants = []
            while i < len(records):
                nxt = records[i]
                if _has_user_text(nxt):
                    break
                if nxt.get('type') == 'assistant':
                    assistants.append(nxt)
                i += 1
            turns.append((user_rec, assistants))
        else:
            i += 1

    for turn_idx, (user_rec, assistants) in enumerate(turns):
        turn_id_num = turn_idx + 1
        tid = f'turn-{turn_id_num}'
        ts = user_rec.get('timestamp', '')
        t = fmt_time(ts)
        user_text = _get_user_text(user_rec)

        # --- TOC: user turn entry ---
        label = user_text[:60].replace('\n', ' ')
        toc_entries.append(
            f'<a class="toc-item toc-user" href="#{tid}">'
            f'<span class="toc-icon">&#9679;</span>'
            f'<span class="toc-label">{escape(label)}</span>'
            f'<span class="toc-time">{t}</span></a>')
        stats['user_turns'] += 1
        if turn_idx > 0:
            stats['user_interventions'] += 1

        # --- TOC + Timeline: single pass with block IDs ---
        badges = []
        body_parts = []
        seen_actions = set()
        block_idx = 0

        BADGE_CLS = {'Thinking': 'badge-think', 'Bash': 'badge-bash', 'Skill': 'badge-skill',
                     'Read': 'badge-read', 'Write': 'badge-write', 'Text': 'badge-text'}

        for a_rec in assistants:
            content = a_rec.get('message', {}).get('content', [])
            at = fmt_time(a_rec.get('timestamp', ''))
            cls, icon, alabel, snippet = _assistant_action(content)

            # Badge (deduped)
            if alabel.lower() not in seen_actions:
                seen_actions.add(alabel.lower())
                bcls = BADGE_CLS.get(alabel, 'badge-tool')
                badges.append(f'<span class="tl-action-badge {bcls}">{escape(alabel)}</span>')

            # Find record index for tool output lookup
            try:
                rec_idx = records.index(a_rec)
            except ValueError:
                rec_idx = len(records)

            if isinstance(content, list):
                for block in content:
                    # Skip empty blocks (no TOC entry, no rendered content)
                    if _is_empty_block(block):
                        continue

                    bid = f'b-{turn_id_num}-{block_idx}'
                    block_idx += 1

                    # TOC entry points to specific block
                    display_label = f'{alabel}: {escape(snippet)}' if snippet else alabel
                    toc_entries.append(
                        f'<a class="toc-item {cls}" href="#{bid}">'
                        f'<span class="toc-icon">{icon}</span>'
                        f'<span class="toc-label">{display_label[:50]}</span>'
                        f'<span class="toc-time">{at}</span></a>')

                    rendered = _render_assistant_block(block, records, rec_idx, stats, bid)
                    if rendered:
                        body_parts.append(rendered)

        badge_str = ''.join(badges)
        body_str = '\n'.join(body_parts) if body_parts else '<p style="color:var(--muted);font-size:13px;font-style:italic">No assistant content</p>'
        turn_label = user_text[:80].replace('\n', ' ')

        timeline_blocks.append(
            f'<div class="tl-turn open" id="{tid}">\n'
            f'  <div class="tl-turn-marker"></div>\n'
            f'  <div class="tl-turn-header" onclick="this.parentElement.classList.toggle(\'open\')">\n'
            f'    <span class="tl-chevron">&#9654;</span>\n'
            f'    <span class="tl-role user-role">Turn {turn_id_num}</span>\n'
            f'    <span class="tl-turn-label">{escape(turn_label)}</span>\n'
            f'    <span class="tl-badge-row">{badge_str}</span>\n'
            f'    <span class="tl-time">{t}</span>\n'
            f'  </div>\n'
            f'  <div class="tl-turn-body">\n{body_str}\n  </div>\n'
            f'</div>')

    return toc_entries, timeline_blocks, stats


def validate(records):
    """Scan JSONL records and report empty block statistics."""
    empty_by_type = {}
    total_by_type = {}
    for rec in records:
        if rec.get('type') != 'assistant':
            continue
        content = rec.get('message', {}).get('content', [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            bt = block.get('type', '')
            total_by_type[bt] = total_by_type.get(bt, 0) + 1
            if _is_empty_block(block):
                empty_by_type[bt] = empty_by_type.get(bt, 0) + 1
    return total_by_type, empty_by_type


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate trajectory HTML from Claude Code session JSONL')
    parser.add_argument('--input', '-i', required=True, help='Input JSONL file')
    parser.add_argument('--output', '-o', default='traj.html', help='Output HTML file')
    parser.add_argument('--validate', '-V', action='store_true', default=True,
                        help='Validate and report empty blocks (default: on)')
    args = parser.parse_args()

    records = load_jsonl(args.input)

    # Validate — report empty blocks that will be filtered
    total_by_type, empty_by_type = validate(records)
    filtered = 0
    for bt in sorted(total_by_type):
        n_total = total_by_type[bt]
        n_empty = empty_by_type.get(bt, 0)
        filtered += n_empty
        if n_empty > 0:
            print(f'[validate] {bt}: {n_empty}/{n_total} empty blocks filtered')
        else:
            print(f'[validate] {bt}: {n_total} blocks (0 filtered)')
    if filtered > 0:
        print(f'[validate] Total filtered: {filtered} empty blocks')
    else:
        print(f'[validate] No empty blocks found — all content will be rendered')

    toc_entries, timeline_blocks, stats = build_toc_and_timeline(records)
    session_meta = build_session_meta(records)

    traj_css = load_template('traj.css')
    template = Template(load_template('traj-template.html'))

    session_id = os.path.basename(args.input).replace('.jsonl', '')[:32]
    html = template.substitute(
        session_id=session_id,
        traj_css=traj_css,
        toc_count=len(toc_entries),
        toc_html='\n'.join(toc_entries),
        timeline_html='\n'.join(timeline_blocks),
        n_user_turns=stats['user_turns'],
        n_skill_calls=stats['skill_calls'],
        n_user_interventions=stats['user_interventions'],
        n_read_files=stats['read_files'],
        n_write_files=stats['write_files'],
        n_tool_use=stats['tool_use'],
        n_thinking=stats['thinking'],
        model_name=session_meta['model_name'],
        session_start=session_meta['session_start'],
        session_end=session_meta['session_end'],
        session_duration=session_meta['session_duration'],
        source_file=os.path.abspath(args.input),
        today=datetime.now().strftime('%Y-%m-%d %H:%M'),
    )

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated: {args.output} ({len(records)} records, {stats["user_turns"]} turns)')

    # Integrity check: verify no empty blocks rendered in output
    import re
    empty_thinking = len(re.findall(r'<div class="thinking-text"></div>', html))
    empty_text = len(re.findall(r'<div class="block block-text" id="[^"]*"></div>', html))
    empty_tool = len(re.findall(r'<div class="block block-tool" id="[^"]*">\s*<div class="tool-header">\s*<span class="tool-name">\s*</span>', html))
    if empty_thinking or empty_text or empty_tool:
        print(f'[validate] WARNING: found empty blocks in output — thinking={empty_thinking}, text={empty_text}, tool={empty_tool}')
    else:
        print(f'[validate] Output integrity OK — no empty blocks in generated HTML')


if __name__ == '__main__':
    main()
