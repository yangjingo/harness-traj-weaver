#!/usr/bin/env python3
"""generate_survey.py — Generate feedback surveys from templates.

Usage:
  python generate_survey.py --type qa --skill traj-display --version v0.1.0
  python generate_survey.py --type human-loop --version v0.1.0
"""

import os
from string import Template


TEMPLATES = {
    'qa': 'qa-survey.html',
    'human-loop': 'human-loop.html',
}


def load_template(name):
    path = os.path.join(os.path.dirname(__file__), '..', 'reference', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate feedback survey')
    parser.add_argument('--type', '-t', required=True, choices=['qa', 'human-loop'],
                        help='Survey type: qa (skill UI/UX) or human-loop (Meta-Harness paradigm)')
    parser.add_argument('--skill', '-s', help='Skill name (required for --type qa)')
    parser.add_argument('--version', '-v', required=True, help='Version tag (e.g. v0.1.0)')
    parser.add_argument('--output', '-o', help='Output file path')
    args = parser.parse_args()

    if args.type == 'qa' and not args.skill:
        parser.error('--skill is required for --type qa')

    template = Template(load_template(TEMPLATES[args.type]))

    if args.type == 'qa':
        survey = template.substitute(SKILL_NAME=args.skill, VERSION=args.version)
        default_output = f'{args.skill}-qa-survey.html'
    else:
        survey = template.substitute(VERSION=args.version)
        default_output = 'meta-harness-survey.html'

    output = args.output or default_output

    with open(output, 'w', encoding='utf-8') as f:
        f.write(survey)

    print(f'Generated: {output} (type={args.type}, version={args.version})')


if __name__ == '__main__':
    main()
