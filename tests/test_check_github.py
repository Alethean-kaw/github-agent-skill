"""Offline regression tests: Git operations are confined to temporary fixtures."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'github-agent/scripts/check_github.py'
spec = importlib.util.spec_from_file_location('diagnostics', SCRIPT)
diagnostics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostics)
GIT = shutil.which('git')


@unittest.skipUnless(GIT, 'Git is required for local integration tests')
class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skill test ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Prevent an outer Git worktree or user config from changing fixture behavior.
        self.env = os.environ.copy()
        for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR'):
            self.env.pop(key, None)
        self.env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull})
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Skill Test Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'core.autocrlf', 'false')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'empty-hooks'))

    def git(self, *args, check=True):
        return subprocess.run([GIT, *args], cwd=self.root, env=self.env,
                              check=check, capture_output=True, text=True)

    def diagnose(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), '--path', str(self.root), *args],
                                env=self.env, capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout)

    def initial_commit(self):
        (self.root / 'tracked.txt').write_text('base\n', encoding='utf-8')
        self.git('add', '--', 'tracked.txt')
        self.git('commit', '-m', 'fixture baseline')

    def test_empty_repository_without_head_is_valid(self):
        code, report = self.diagnose()
        self.assertEqual(code, 0)
        self.assertTrue(report['ok'])
        self.assertNotEqual(report['checks']['head']['exit_code'], 0)
        self.assertFalse(report['online_requested'])

    def test_dirty_and_staged_content_is_preserved(self):
        self.initial_commit()
        tracked = self.root / 'tracked.txt'
        tracked.write_text('staged\n', encoding='utf-8')
        self.git('add', '--', 'tracked.txt')
        tracked.write_text('unstaged\n', encoding='utf-8')
        (self.root / 'untracked.txt').write_text('private draft\n', encoding='utf-8')
        before_index = (self.root / '.git/index').read_bytes()
        before_status = self.git('status', '--porcelain').stdout
        code, report = self.diagnose()
        self.assertEqual(code, 0)
        self.assertEqual((self.root / '.git/index').read_bytes(), before_index)
        self.assertEqual(self.git('status', '--porcelain').stdout, before_status)
        self.assertEqual(tracked.read_text(), 'unstaged\n')
        self.assertIn('tracked.txt', report['checks']['staged_summary']['stdout'])

    def test_real_merge_conflict_is_detected_and_preserved(self):
        self.initial_commit()
        self.git('switch', '-c', 'other')
        (self.root / 'tracked.txt').write_text('other\n', encoding='utf-8')
        self.git('commit', '-am', 'other change')
        self.git('switch', 'main')
        (self.root / 'tracked.txt').write_text('main\n', encoding='utf-8')
        self.git('commit', '-am', 'main change')
        merged = self.git('merge', 'other', check=False)
        self.assertNotEqual(merged.returncode, 0)
        before = (self.root / '.git/index').read_bytes()
        code, report = self.diagnose()
        self.assertEqual(code, 0)
        self.assertIn('MERGE_HEAD', report['in_progress_markers'])
        self.assertEqual((self.root / '.git/index').read_bytes(), before)
        self.assertTrue((self.root / '.git/MERGE_HEAD').exists())

    def test_detached_head_is_reported_without_switching(self):
        self.initial_commit()
        self.git('checkout', '--detach')
        code, report = self.diagnose()
        self.assertEqual(code, 0)
        self.assertEqual(report['checks']['branch']['stdout'].strip(), '')
        self.assertEqual(self.git('branch', '--show-current').stdout.strip(), '')

    def test_resolved_merge_is_still_reported_as_in_progress(self):
        self.initial_commit()
        self.git('switch', '-c', 'other')
        (self.root / 'other.txt').write_text('other change\n', encoding='utf-8')
        self.git('add', '--', 'other.txt')
        self.git('commit', '-m', 'other commit')
        self.git('switch', 'main')
        self.git('merge', '--no-ff', '--no-commit', 'other')
        self.assertNotIn('U', self.git('status', '--porcelain').stdout[:2])
        code, report = self.diagnose()
        self.assertEqual(code, 0)
        self.assertIn('MERGE_HEAD', report['in_progress_markers'])
        self.assertTrue((self.root / '.git/MERGE_HEAD').exists())

    def test_sequencer_state_is_preserved(self):
        self.initial_commit()
        state = self.root / '.git/sequencer'
        state.mkdir()
        todo = state / 'todo'
        todo.write_text('fixture state\n', encoding='utf-8')
        code, report = self.diagnose()
        self.assertEqual(code, 0)
        self.assertIn('sequencer', report['in_progress_markers'])
        self.assertEqual(todo.read_text(), 'fixture state\n')

    def test_remote_credentials_are_not_reported(self):
        self.git('remote', 'add', 'origin', 'https://test-user:test-password@example.invalid/repo.git?token=fixture-secret')
        code, report = self.diagnose()
        self.assertEqual(code, 0)
        output = json.dumps(report)
        self.assertNotIn('test-password', output)
        self.assertNotIn('fixture-secret', output)
        self.assertIn('[REDACTED]', output)

    def test_non_repository_returns_failure(self):
        directory = self.root / 'outside'
        directory.mkdir()
        # Use a sibling temporary directory to avoid Git finding the parent fixture.
        with tempfile.TemporaryDirectory() as outside:
            result = subprocess.run([sys.executable, str(SCRIPT), '--path', outside],
                                    env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['ok'])


class ErrorAndPrivacyTests(unittest.TestCase):
    def test_invalid_arguments_fail_before_command_execution(self):
        cases = [['--repo', 'a/b'], ['--host', 'https://github.com'],
                 ['--timeout', '0'], ['--timeout', 'nan'], ['--timeout', '121']]
        for args in cases:
            with self.subTest(args=args), patch.object(sys, 'argv', ['check', *args]), \
                    patch.object(diagnostics, 'run') as runner, contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as exc:
                    diagnostics.main()
                self.assertEqual(exc.exception.code, 2)
                runner.assert_not_called()

    def test_missing_directory_returns_json_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(sys, 'argv', ['check', '--path', str(Path(folder) / 'missing')]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(diagnostics.main(), 1)
                self.assertFalse(json.loads(output.getvalue())['ok'])

    def test_missing_gh_is_clear_in_online_mode(self):
        with tempfile.TemporaryDirectory() as folder:
            output = io.StringIO()
            with patch.object(sys, 'argv', ['check', '--path', folder, '--online']), \
                    patch.object(diagnostics.shutil, 'which', return_value=None), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(diagnostics.main(), 1)
            self.assertIn('gh not found', ' '.join(json.loads(output.getvalue())['notes']))

    def test_redacts_tokens_queries_and_known_secret_values(self):
        with patch.dict(os.environ, {'GH_TOKEN': 'custom-sensitive-value'}):
            output = diagnostics.redact('ghp_abc123 github_pat_example https://a:b@host/?sig=123&token=456 custom-sensitive-value')
        for secret in ('abc123', 'github_pat_example', 'a:b@', 'sig=123', 'token=456', 'custom-sensitive-value'):
            self.assertNotIn(secret, output)

    def test_timeout_has_no_partial_secret_output(self):
        exc = subprocess.TimeoutExpired('git', 1, output=b'private incomplete output')
        with patch.object(diagnostics.subprocess, 'run', side_effect=exc):
            result = diagnostics.run(['git', 'status'], Path.cwd(), 1)
        self.assertEqual(result['exit_code'], 124)
        self.assertEqual(result['stdout'], '')

    def test_os_error_is_structured(self):
        with patch.object(diagnostics.subprocess, 'run', side_effect=FileNotFoundError('missing tool')):
            result = diagnostics.run(['absent-tool'], Path.cwd(), 1)
        self.assertEqual(result['exit_code'], 127)


if __name__ == '__main__':
    unittest.main()
