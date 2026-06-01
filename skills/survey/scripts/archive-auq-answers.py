"""Archive AUQ answers from human-loop QA to evals inputs directory."""
import argparse
import json
import os
import sys
from datetime import datetime, timezone


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def detect_version():
    changelog = os.path.join(REPO_ROOT, 'CHANGELOG.md')
    try:
        with open(changelog) as f:
            for line in f:
                if line.startswith('## ['):
                    import re
                    m = re.match(r'## \[([0-9.]+)\]', line)
                    if m:
                        return f'v{m.group(1)}'
    except Exception:
        pass
    return 'v0.1.0'


def main():
    parser = argparse.ArgumentParser(description='Archive human-loop AUQ answers')
    parser.add_argument('--skill', required=True, help='Skill name')
    parser.add_argument('--version', default=None, help='Version (auto-detected if omitted)')
    parser.add_argument('--mode', default='quick', choices=['quick', 'full'], help='QA mode')
    parser.add_argument('--answers', required=True, help='Answers as JSON string')
    parser.add_argument('--branch', default='unknown', help='Git branch')
    parser.add_argument('--question-bank-version', default='0.2.0', help='Version of the question bank used')
    parser.add_argument('--output-dir', default=None, help='Output directory (auto if omitted)')
    args = parser.parse_args()

    version = args.version or detect_version()

    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(REPO_ROOT, '.metaharness', version, 'inputs')

    os.makedirs(output_dir, exist_ok=True)

    answers = json.loads(args.answers)

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    ts_slug = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')

    record = {
        'skill': args.skill,
        'version': version,
        'mode': args.mode,
        'branch': args.branch,
        'timestamp': timestamp,
        'question_count': len(answers),
        'question_bank_version': args.question_bank_version,
        'session_id': os.environ.get('CLAUDE_CODE_SESSION_ID', ''),
        'duration_seconds': int(os.environ.get('QA_DURATION_SECONDS', 0)) or None,
        'answers': answers,
    }

    fname = f'qa-{args.skill}-{ts_slug}.json'
    fpath = os.path.join(output_dir, fname)

    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    # Also write a human-readable summary
    summary_path = os.path.join(output_dir, f'qa-{args.skill}-{ts_slug}.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"QA Feedback — {args.skill} {version}\n")
        f.write(f"{'=' * 50}\n")
        f.write(f"Mode: {args.mode}\n")
        f.write(f"Branch: {args.branch}\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        for qid, ans in answers.items():
            if isinstance(ans, list):
                f.write(f"[{qid}]: {', '.join(ans)}\n")
            else:
                f.write(f"[{qid}]: {ans}\n")

    print(json.dumps({
        'ok': True,
        'path': os.path.relpath(fpath, REPO_ROOT),
        'summary': os.path.relpath(summary_path, REPO_ROOT),
    }))


if __name__ == '__main__':
    main()
