#!/usr/bin/env python3
"""Read-only Git diagnostics; explicit --online enables gh access. Python 3.9+."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def redact(value):
    text = str(value)
    text = re.sub(r'(?i)(https?://)[^\s/@]+@', r'\1[REDACTED]@', text)
    text = re.sub(r'\b(?:github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9_]+)\b', '[REDACTED]', text)
    text = re.sub(r'(?i)([?&](?:token|access_token|key|signature|sig)=)[^\s&]+', r'\1[REDACTED]', text)
    # Exact matching of known secret environment values; never emit the environment.
    for key in ('GH_TOKEN', 'GITHUB_TOKEN', 'GH_ENTERPRISE_TOKEN', 'GITHUB_ENTERPRISE_TOKEN'):
        secret = os.environ.get(key)
        if secret:
            text = text.replace(secret, '[REDACTED]')
    return text


def run(argv, cwd, timeout):
    env = os.environ.copy()
    env.update({'GIT_OPTIONAL_LOCKS': '0', 'GIT_TERMINAL_PROMPT': '0',
                'GH_PROMPT_DISABLED': '1', 'GH_PAGER': 'cat', 'GIT_PAGER': 'cat',
                'NO_COLOR': '1'})
    try:
        result = subprocess.run(argv, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout, shell=False)
        return {'exit_code': result.returncode,
                'stdout': redact(result.stdout.decode('utf-8', errors='replace'))[:20000],
                'stderr': redact(result.stderr.decode('utf-8', errors='replace'))[:12000],
                'truncated': len(result.stdout) > 20000 or len(result.stderr) > 12000}
    except subprocess.TimeoutExpired:
        return {'exit_code': 124, 'stdout': '', 'stderr': 'Timed out; no automatic retry.'}
    except OSError as exc:
        return {'exit_code': 127, 'stdout': '', 'stderr': redact(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--path', default='.', help='Existing local repository directory')
    parser.add_argument('--online', action='store_true', help='Check gh auth; optionally repository access')
    parser.add_argument('--repo', help='OWNER/REPO, no URL or hostname')
    parser.add_argument('--host', default='github.com', help='GitHub hostname')
    parser.add_argument('--timeout', type=float, default=20, help='Seconds per command, 0 < value <= 120')
    args = parser.parse_args()
    if not 0 < args.timeout <= 120:
        parser.error('--timeout must be greater than zero and at most 120')
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?', args.host):
        parser.error('--host must be a hostname, without URL scheme, port or path')
    if args.repo and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9_.-]+', args.repo):
        parser.error('--repo must be OWNER/REPO')
    if args.repo and not args.online:
        parser.error('--repo requires --online')
    cwd = Path(args.path).expanduser().resolve()
    report = {'path': redact(cwd), 'online_requested': args.online,
              'checks': {}, 'notes': [], 'ok': True}
    if not cwd.is_dir():
        report['ok'] = False
        report['notes'].append('Path does not exist or is not a directory.')
    else:
        git = shutil.which('git')
        gh = shutil.which('gh')
        report['tools'] = {'git_available': bool(git), 'gh_available': bool(gh)}
        def check(name, argv, required=True):
            result = run(argv, cwd, args.timeout)
            report['checks'][name] = result
            if required and result['exit_code'] != 0:
                report['ok'] = False
            return result
        if not git:
            report['ok'] = False
            report['notes'].append('Git not found in PATH; local inspection unavailable.')
        else:
            prefix = [git, '--no-pager', '-c', 'core.fsmonitor=false']
            check('git_version', [git, '--version'])
            root = check('repository_root', prefix + ['rev-parse', '--show-toplevel'])
            if root['exit_code'] == 0:
                for name, command in (
                    ('status', ['status', '--short', '--branch', '--untracked-files=normal', '--ignore-submodules=all']),
                    ('branch', ['branch', '--show-current']),
                    ('remotes', ['remote', '-v']),
                    ('unstaged_summary', ['diff', '--no-ext-diff', '--no-textconv', '--stat', '--ignore-submodules=all']),
                    ('staged_summary', ['diff', '--cached', '--no-ext-diff', '--no-textconv', '--stat', '--ignore-submodules=all']),
                ):
                    check(name, prefix + command)
                head = check('head', prefix + ['rev-parse', '--verify', 'HEAD'], required=False)
                if head['exit_code'] != 0:
                    report['notes'].append('No resolvable HEAD; this may be a newly initialized repository.')
                check('upstream', prefix + ['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}'], required=False)
                active = []
                for marker in ('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply'):
                    marker_result = run(prefix + ['rev-parse', '--git-path', marker], cwd, args.timeout)
                    if marker_result['exit_code'] == 0:
                        candidate = Path(marker_result['stdout'].strip())
                        if not candidate.is_absolute():
                            candidate = cwd / candidate
                        if candidate.exists():
                            active.append(marker)
                report['in_progress_markers'] = active
                if active:
                    report['notes'].append('An operation is in progress; do not take it over automatically.')
        if args.online:
            if not gh:
                report['ok'] = False
                report['notes'].append('gh not found in PATH. A host-provided GitHub connector may still be usable.')
            else:
                check('gh_version', [gh, '--version'])
                check('gh_auth', [gh, 'auth', 'status', '--hostname', args.host])
                if args.repo:
                    check('github_repository', [gh, 'repo', 'view', args.host + '/' + args.repo,
                                              '--json', 'nameWithOwner,url,visibility,defaultBranchRef,isFork'])
        else:
            report['notes'].append('Authentication and remote reachability were not checked. Use --online to request them.')
    report['notes'].append('Diagnostic snapshot only; a successful result does not grant permission to change or publish.')
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
