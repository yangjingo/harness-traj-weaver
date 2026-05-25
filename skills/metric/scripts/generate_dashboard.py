#!/usr/bin/env python3
"""generate_dashboard.py — Code review dashboard against Karpathy principles.

Reads a git diff and evaluates every change across four dimensions:
  1. Think Before Coding  — assumptions stated, alternatives considered
  2. Simplicity First      — no over-engineering, minimal lines
  3. Surgical Changes      — every line traces to the goal
  4. Goal-Driven Execution — verifiable completion criteria

Usage:
  python generate_dashboard.py --diff HEAD
  python generate_dashboard.py --diff main..HEAD
  python generate_dashboard.py --files app.py utils.py
  python generate_dashboard.py --diff HEAD --goal "Add user auth"
"""

import os
import re
import subprocess
from datetime import datetime
from string import Template


def load_template(name):
    path = os.path.join(os.path.dirname(__file__), '..', 'reference', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_diff_files(ref):
    """Return list of changed files from a git diff reference."""
    cmd = ['git', 'diff', '--name-only', ref]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode != 0:
        print(f"Warning: git diff failed — {result.stderr.strip()}")
        return []
    return [f for f in result.stdout.strip().split('\n') if f]


def get_diff_content(ref, filepath=None):
    """Get unified diff content for a ref, optionally scoped to a file."""
    cmd = ['git', 'diff', ref, '--']
    if filepath:
        cmd.append(filepath)
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.stdout or ""


def count_added_lines(diff_text):
    """Count lines starting with + (but not ++)."""
    return len([l for l in diff_text.split('\n') if l.startswith('+') and not l.startswith('+++')])


def count_removed_lines(diff_text):
    """Count lines starting with - (but not --)."""
    return len([l for l in diff_text.split('\n') if l.startswith('-') and not l.startswith('---')])


def has_docstring_changes(diff_text):
    """Check if diff touches docstrings or comments."""
    comment_lines = 0
    for line in diff_text.split('\n'):
        stripped = line[1:] if line.startswith(('+', '-')) else ''
        if stripped.strip().startswith(('#', '//', '/*', '*', '"""', "'''")):
            comment_lines += 1
    return comment_lines


def has_new_functions(diff_text):
    """Count new function/class definitions."""
    patterns = [r'^\+.*\bdef\s+\w+', r'^\+.*\bclass\s+\w+', r'^\+.*\bfn\s+\w+',
                r'^\+.*\bfunction\s+\w+', r'^\+.*\bconst\s+\w+\s*=']
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, diff_text, re.MULTILINE))
    return count


def has_import_changes(diff_text):
    """Check for new import/additions that seem unrelated."""
    return len(re.findall(r'^\+.*\b(import|from|require)\b', diff_text, re.MULTILINE))


def has_config_changes(diff_text):
    """Check for config/env/hardcoded-value changes."""
    patterns = [r'\.env', r'\.config', r'\.json', r'\.ya?ml', r'CONFIG', r'SETTINGS',
                r'hardcode', r'TODO', r'FIXME', r'HACK']
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, diff_text, re.IGNORECASE))
    return count


def should_ignore_file(filepath):
    """Skip generated files, lockfiles, binaries, etc."""
    ignore_patterns = [
        r'package-lock\.json$', r'yarn\.lock$', r'pnpm-lock\.yaml$',
        r'\.lock$', r'\.min\.(js|css)$', r'\.svg$', r'\.png$', r'\.ico$',
        r'\.jpg$', r'\.gif$', r'\.woff2?$', r'\.pdf$', r'\.pyc$',
        r'poetry\.lock$', r'Pipfile\.lock$', r'\.sum$',
    ]
    return any(re.search(p, filepath) for p in ignore_patterns)


def analyze_file(filepath, diff_text, goal=""):
    """Analyze a single file's diff against the 4 principles. Returns a dict."""
    added = count_added_lines(diff_text)
    removed = count_removed_lines(diff_text)
    total_churn = added + removed
    new_funcs = has_new_functions(diff_text)
    import_changes = has_import_changes(diff_text)
    config_changes = has_config_changes(diff_text)
    comment_changes = has_docstring_changes(diff_text)

    issues = []
    scores = {'think': 5, 'simplicity': 5, 'surgical': 5, 'goal': 5}

    # Principle 1: Think Before Coding
    if total_churn > 100 and not goal:
        issues.append({
            'severity': 'med', 'principle': 'think', 'tag': 'tag-think',
            'file': filepath, 'lines': f'+{added}/-{removed}',
            'msg': f'Large change ({total_churn} lines) without a stated goal. Consider documenting assumptions.',
            'fix': 'State what assumptions you made and what alternatives were considered.'
        })
        scores['think'] -= 1
    if new_funcs > 3:
        issues.append({
            'severity': 'low', 'principle': 'think', 'tag': 'tag-think',
            'file': filepath, 'lines': f'+{new_funcs} defs',
            'msg': f'{new_funcs} new definitions added. Are all necessary? Were alternatives considered?',
            'fix': 'Verify each new function is required and alternatives were evaluated.'
        })
        scores['think'] -= 1

    # Principle 2: Simplicity First
    if total_churn > 200:
        severity = 'high' if total_churn > 500 else 'med'
        issues.append({
            'severity': severity, 'principle': 'simplicity', 'tag': 'tag-simplicity',
            'file': filepath, 'lines': f'+{added}/-{removed}',
            'msg': f'High churn ({total_churn} lines). Could this be solved with fewer changes?',
            'fix': 'Aim for the minimal change. If 200 lines can be 50, rewrite.'
        })
        scores['simplicity'] -= (2 if severity == 'high' else 1)
    if new_funcs > 5:
        issues.append({
            'severity': 'med', 'principle': 'simplicity', 'tag': 'tag-simplicity',
            'file': filepath, 'lines': f'+{new_funcs} defs',
            'msg': f'{new_funcs} new definitions — possible over-abstraction. Three similar lines > premature abstraction.',
            'fix': 'Remove helper functions used only once. Inline trivial abstractions.'
        })
        scores['simplicity'] -= 1
    if config_changes > 0:
        issues.append({
            'severity': 'low', 'principle': 'simplicity', 'tag': 'tag-simplicity',
            'file': filepath, 'lines': '+config',
            'msg': 'Config/env changes detected. Avoid adding flags or configuration unless explicitly requested.',
            'fix': 'Remove config options that are not directly tied to the stated goal.'
        })
        scores['simplicity'] -= 1

    # Principle 3: Surgical Changes
    if removed > added * 2:
        issues.append({
            'severity': 'med', 'principle': 'surgical', 'tag': 'tag-surgical',
            'file': filepath, 'lines': f'+{added}/-{removed}',
            'msg': f'Removing far more lines ({removed}) than adding ({added}). Check for drive-by deletions.',
            'fix': 'Restore code removal that is unrelated to the primary goal.'
        })
        scores['surgical'] -= 1
    if comment_changes > 5 and added < removed:
        issues.append({
            'severity': 'low', 'principle': 'surgical', 'tag': 'tag-surgical',
            'file': filepath, 'lines': 'comments',
            'msg': 'Comment-only or comment-heavy changes detected. Avoid style-only edits in functional PRs.',
            'fix': 'Remove comment-only changes unless they fix incorrect documentation.'
        })
        scores['surgical'] -= 1
    if import_changes > 3 and not goal:
        issues.append({
            'severity': 'low', 'principle': 'surgical', 'tag': 'tag-surgical',
            'file': filepath, 'lines': '+imports',
            'msg': f'{import_changes} import changes. Ensure each new dependency traces to the goal.',
            'fix': 'Remove imports not directly needed for the stated task.'
        })
        scores['surgical'] -= 1

    # Principle 4: Goal-Driven Execution
    if not goal:
        scores['goal'] -= 1
        issues.append({
            'severity': 'low', 'principle': 'goal', 'tag': 'tag-goal',
            'file': filepath, 'lines': '—',
            'msg': 'No goal specified. Each change should have a verifiable completion criterion.',
            'fix': 'Define a goal: "After this change, X should happen when Y."'
        })
    if not diff_text.strip():
        scores['goal'] = 0

    # Clamp scores
    for k in scores:
        scores[k] = max(0, min(5, scores[k]))

    return {
        'filepath': filepath,
        'added': added,
        'removed': removed,
        'churn': total_churn,
        'new_funcs': new_funcs,
        'scores': scores,
        'issues': issues,
    }


def score_class(avg):
    if avg >= 4: return 'pass'
    if avg >= 2.5: return 'warn'
    return 'fail'


def build_principle_card(num, name, desc, score):
    fill_class = 'fill-pass' if score >= 4 else ('fill-warn' if score >= 2.5 else 'fill-fail')
    pct = int(score / 5 * 100)
    return f"""<div class="principle-card">
      <h4>P{num}. {name}</h4>
      <div class="desc">{desc}</div>
      <div class="score-bar">
        <div class="bar"><div class="bar-fill {fill_class}" style="width:{pct}%"></div></div>
        <div class="bar-num">{score}/5</div>
      </div>
    </div>"""


def build_file_card(result):
    s = result['scores']
    fs = lambda v: 'fs-pass' if v >= 4 else ('fs-warn' if v >= 3 else 'fs-fail')
    return f"""<div class="file-card">
      <div class="name">{result['filepath']}</div>
      <div style="font-size:12px;color:var(--muted);margin-bottom:8px">+{result['added']}/-{result['removed']} &middot; {result['new_funcs']} new defs</div>
      <div class="scores">
        <div class="file-score {fs(s['think'])}" title="Think">{s['think']}</div>
        <div class="file-score {fs(s['simplicity'])}" title="Simplicity">{s['simplicity']}</div>
        <div class="file-score {fs(s['surgical'])}" title="Surgical">{s['surgical']}</div>
        <div class="file-score {fs(s['goal'])}" title="Goal">{s['goal']}</div>
      </div>
    </div>"""


def build_issue_html(issue):
    return f"""<div class="issue sev-{issue['severity']}">
      <div class="issue-header">
        <span class="issue-file">{issue['file']}</span>
        <span class="issue-principle {issue['tag']}">{issue['principle']}</span>
      </div>
      <div class="issue-lines">{issue['lines']}</div>
      <div class="issue-msg">{issue['msg']}</div>
      <div class="issue-fix"><strong>Suggested fix:</strong> {issue['fix']}</div>
    </div>"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate code review dashboard against Karpathy principles')
    parser.add_argument('--diff', '-d', help='Git diff reference (e.g. HEAD, main..HEAD)')
    parser.add_argument('--files', '-f', nargs='+', help='Specific files to review')
    parser.add_argument('--goal', '-g', default='', help='Stated goal of the changes')
    parser.add_argument('--output', '-o', default='dashboard.html', help='Output file path')
    args = parser.parse_args()

    if not args.diff and not args.files:
        parser.error('Either --diff or --files is required')

    # Determine which files to analyze
    if args.files:
        filepaths = args.files
        diffs = {}
        for fp in filepaths:
            try:
                with open(fp, 'r') as f:
                    diffs[fp] = f"File content: {len(f.read())} chars"
            except FileNotFoundError:
                print(f"Warning: {fp} not found")
                diffs[fp] = ""
    else:
        filepaths = get_diff_files(args.diff)
        diffs = {}
        for fp in filepaths:
            if not should_ignore_file(fp):
                diffs[fp] = get_diff_content(args.diff, fp)
        filepaths = list(diffs.keys())

    if not filepaths:
        print("No files to review.")
        return

    # Analyze each file
    results = []
    all_issues = []
    for fp in filepaths:
        result = analyze_file(fp, diffs[fp], args.goal)
        results.append(result)
        all_issues.extend(result['issues'])

    # Compute aggregate scores
    if results:
        avg_scores = {
            'think': round(sum(r['scores']['think'] for r in results) / len(results), 1),
            'simplicity': round(sum(r['scores']['simplicity'] for r in results) / len(results), 1),
            'surgical': round(sum(r['scores']['surgical'] for r in results) / len(results), 1),
            'goal': round(sum(r['scores']['goal'] for r in results) / len(results), 1),
        }
        overall = round(sum(avg_scores.values()) / 4, 1)
    else:
        avg_scores = {'think': 5, 'simplicity': 5, 'surgical': 5, 'goal': 5}
        overall = 5.0

    # Classify
    files_clean = sum(1 for r in results if sum(r['scores'].values()) / 4 >= 4)
    files_warn = sum(1 for r in results if 2.5 <= sum(r['scores'].values()) / 4 < 4)
    files_fail = len(results) - files_clean - files_warn

    if overall >= 4:
        verdict = 'PASS'
        summary = 'Changes are clean, focused, and align with the stated goal. Minor suggestions only.'
    elif overall >= 2.5:
        verdict = 'NEEDS WORK'
        summary = f'{files_warn + files_fail} of {len(results)} files have issues. Address flagged items before merging.'
    else:
        verdict = 'REJECT'
        summary = 'Significant issues across multiple principles. Simplify, focus, and re-submit.'

    # Build HTML components
    principle_cards = '\n'.join([
        build_principle_card(1, 'Think Before Coding', 'Assumptions stated, alternatives considered', avg_scores['think']),
        build_principle_card(2, 'Simplicity First', 'No over-engineering, minimal necessary lines', avg_scores['simplicity']),
        build_principle_card(3, 'Surgical Changes', 'Every line traces to the goal', avg_scores['surgical']),
        build_principle_card(4, 'Goal-Driven Execution', 'Verifiable completion criteria', avg_scores['goal']),
    ])

    file_cards = '\n'.join(build_file_card(r) for r in results)
    issue_items = '\n'.join(build_issue_html(i) for i in all_issues) if all_issues else '<p style="color:var(--muted)">No issues detected.</p>'

    overall_class = 'pass' if overall >= 4 else ('warn' if overall >= 2.5 else 'fail')

    # Render template
    template = Template(load_template('dashboard-template.html'))
    html = template.substitute(
        version=f"v{args.diff or 'files'}",
        today=datetime.now().strftime('%Y-%m-%d %H:%M'),
        total_issues=str(len(all_issues)),
        file_count=str(len(results)),
        overall_score=str(overall),
        overall_class=overall_class,
        files_clean=str(files_clean),
        files_warn=str(files_warn),
        verdict=verdict,
        summary=summary,
        principle_cards=principle_cards,
        file_cards=file_cards,
        issue_items=issue_items,
    )

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Generated: {args.output}')
    print(f'  Files reviewed: {len(results)}')
    print(f'  Issues found:   {len(all_issues)}')
    print(f'  Overall score:  {overall}/5 ({verdict})')


if __name__ == '__main__':
    main()
