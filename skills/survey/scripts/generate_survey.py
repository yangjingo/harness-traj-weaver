#!/usr/bin/env python3
"""generate_survey.py — Generate feedback surveys with git & changelog context.

Usage:
  python generate_survey.py --type qa --skill traj --version v0.1.0
  python generate_survey.py --type human-loop --version v0.1.0
"""

import os
import subprocess
from datetime import datetime
from string import Template


TEMPLATES = {
    'qa': 'qa-survey.html',
    'human-loop': 'human-loop.html',
}


def load_template(name):
    path = os.path.join(os.path.dirname(__file__), '..', 'reference', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def load_file(path):
    """Read a file if it exists, otherwise return a placeholder."""
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.strip() or f"({path} is empty)"
    return f"({path} not found)"


def git_log_oneline(n=15):
    """Get recent git log in oneline format."""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', f'-{n}'],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        return result.stdout.strip() or "(no commits yet)"
    except Exception:
        return "(git unavailable)"


def git_log_detail(n=5):
    """Get recent git log with full messages."""
    try:
        result = subprocess.run(
            ['git', 'log', f'-{n}', '--format=%h %s%n%b', '--no-merges'],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        return result.stdout.strip() or "(no commits yet)"
    except Exception:
        return "(git unavailable)"


def git_diff_stat(ref='HEAD~3..HEAD'):
    """Get diffstat for recent changes."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--stat', ref],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        return result.stdout.strip() or "(no diff)"
    except Exception:
        return "(git unavailable)"


def format_changelog_html(content):
    """Convert raw CHANGELOG.md content to a compact HTML summary."""
    lines = content.split('\n')
    # Find the [Unreleased] section or most recent version section
    html = '<ul class="cl-items">'
    in_section = False
    count = 0
    for line in lines:
        if line.startswith('## ['):
            if in_section:
                break
            in_section = True
            html += f'<li class="cl-version">{line.strip("# ")}</li>'
            continue
        if in_section and line.startswith('-'):
            if count >= 20:
                break
            html += f'<li>{line.strip("- ")}</li>'
            count += 1
    html += '</ul>'
    if count == 0:
        return '<p style="color:var(--muted)">No recent changelog entries.</p>'
    return html


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate feedback survey with git & changelog context')
    parser.add_argument('--type', '-t', required=True, choices=['qa', 'human-loop'],
                        help='Survey type: qa (skill UI/UX) or human-loop (Meta-Harness paradigm)')
    parser.add_argument('--skill', '-s', help='Skill name (required for --type qa)')
    parser.add_argument('--version', '-v', required=True, help='Version tag (e.g. v0.1.0)')
    parser.add_argument('--output', '-o', help='Output file path')
    args = parser.parse_args()

    if args.type == 'qa' and not args.skill:
        parser.error('--skill is required for --type qa')

    # Collect context
    git_log = git_log_oneline()
    git_detail = git_log_detail()
    git_diffstat = git_diff_stat()
    changelog_raw = load_file('changelog.md')

    # Build changelog HTML summary
    changelog_html = format_changelog_html(changelog_raw)

    template = Template(load_template(TEMPLATES[args.type]))

    if args.type == 'qa':
        survey = template.substitute(
            SKILL_NAME=args.skill,
            VERSION=args.version,
            GIT_LOG=git_log,
            GIT_DETAIL=git_detail,
            GIT_DIFFSTAT=git_diffstat,
            CHANGELOG_HTML=changelog_html,
            TODAY=datetime.now().strftime('%Y-%m-%d %H:%M'),
        )
        default_output = f'{args.skill}-qa-survey.html'
    else:
        survey = template.substitute(
            VERSION=args.version,
            GIT_LOG=git_log,
            GIT_DETAIL=git_detail,
            GIT_DIFFSTAT=git_diffstat,
            CHANGELOG_HTML=changelog_html,
            TODAY=datetime.now().strftime('%Y-%m-%d %H:%M'),
        )
        default_output = 'meta-harness-survey.html'

    output = args.output or default_output

    with open(output, 'w', encoding='utf-8') as f:
        f.write(survey)

    print(f'Generated: {output} (type={args.type}, version={args.version})')
    print(f'  Git log:     {len(git_log.splitlines())} commits')
    print(f'  Changelog:   {"found" if not changelog_raw.startswith("(") else "missing"}')


if __name__ == '__main__':
    main()
