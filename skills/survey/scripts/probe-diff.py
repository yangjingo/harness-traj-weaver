"""State probe for Section G diff-aware QA — outputs JSON with all placeholder values."""
import subprocess
import json
import os
import sys


def git(*args):
    try:
        r = subprocess.run(['git'] + list(args), capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return ''


def main():
    diff_ref = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'

    ns = git('diff', '--name-status', diff_ref)
    lines = [l for l in ns.split('\n') if l.strip()]
    new_count = sum(1 for l in lines if l.startswith('A'))
    mod_count = sum(1 for l in lines if l.startswith('M'))
    del_count = sum(1 for l in lines if l.startswith('D'))

    untracked = git('ls-files', '--others', '--exclude-standard')
    untracked_list = [l for l in untracked.split('\n') if l.strip()]

    shortstat = git('diff', '--shortstat', diff_ref)
    mod_files = git('diff', '--name-only', diff_ref)
    branch = git('branch', '--show-current') or 'unknown'

    design_doc = 'yes' if os.path.exists('skills/survey/reference/human-loop-design.md') else 'no'

    all_changed = git('diff', '--name-only', diff_ref)
    changed_list = [f for f in all_changed.split('\n') if f.strip()]

    def match(f, keywords):
        return any(k in f.lower() for k in keywords)

    test_files = [f for f in changed_list if match(f, ('test', 'spec', '__tests__', 'eval'))]
    dep_files = [f for f in changed_list if match(f, ('package.json', 'requirements', 'pyproject', 'go.mod', 'gemfile', 'dockerfile', 'makefile'))]
    sec_files = [f for f in changed_list if match(f, ('auth', 'token', 'secret', 'credential', '.env', 'settings.json', 'cert', 'key.pem'))]
    skill_files = [f for f in changed_list if f.startswith('skills/')]

    probe = {
        'branch': branch,
        'new_count': new_count,
        'mod_count': mod_count,
        'del_count': del_count,
        'untracked_count': len(untracked_list),
        'shortstat': shortstat,
        'modified_files': mod_files.replace('\n', ', '),
        'new_files': ', '.join([l.split('\t')[1] if '\t' in l else l[2:] for l in lines if l.startswith('A')]),
        'deleted_files': ', '.join([l.split('\t')[1] if '\t' in l else l[2:] for l in lines if l.startswith('D')]),
        'untracked_files': ', '.join(untracked_list),
        'design_doc': design_doc,
        'test_files_changed': ', '.join(test_files),
        'test_count': len(test_files),
        'dep_files_changed': ', '.join(dep_files),
        'dep_count': len(dep_files),
        'sec_files_changed': ', '.join(sec_files),
        'sec_count': len(sec_files),
        'skill_files': ', '.join(skill_files),
        'skill_count': len(skill_files),
    }

    print(json.dumps(probe, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
