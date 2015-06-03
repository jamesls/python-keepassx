#!/usr/bin/env python
"""Integration tests for the kp CLI.

These use subprocess to actually run the kp
command.

"""
import os
import sys
import time
import unittest
from contextlib import contextmanager
from six import StringIO

from keepassx.main import main
from keepassx.main import CONFIG_FILENAME


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@contextmanager
def without_config_file():
    backup_file = None
    if os.path.isfile(CONFIG_FILENAME):
        backup_file = CONFIG_FILENAME + '.%s' % int(time.time())
        os.rename(CONFIG_FILENAME, backup_file)
    try:
        yield
    finally:
        if backup_file is not None:
            os.rename(backup_file, CONFIG_FILENAME)


@contextmanager
def capture_stdout():
    captured = StringIO()
    sys.stdout = captured
    try:
        yield captured
    finally:
        sys.stdout = sys.__stdout__


@contextmanager
def capture_stderr():
    captured = StringIO()
    sys.stderr = captured
    try:
        yield captured
    finally:
        sys.stderr = sys.__stderr__


class TestCLI(unittest.TestCase):
    # All tests are from the ./misc directory,
    # so that you can conveniently specify
    # password and keyfiles using relative paths.

    def setUp(self):
        self._original_dir = os.getcwd()
        misc_dir = os.path.join(PROJECT_DIR, 'misc')
        os.chdir(misc_dir)
        self._newenv = os.environ.copy()
        self._env = os.environ
        os.environ = self._newenv

    def tearDown(self):
        os.chdir(self._original_dir)
        os.environ = self._env

    def kp_run(self, command):
        self._newenv['KP_INSECURE_PASSWORD'] = 'password'
        if command.startswith('kp '):
            command = command[3:]
        with without_config_file():
            with capture_stdout() as captured:
                main(command.split())
            return captured.getvalue()

    def test_open_with_password_and_keyfile(self):
        output = self.kp_run(
            'kp -d ./passwordkey.kdb -k ./passwordkey.key list')
        self.assertIn('c4d301502050cd695e353b16094be4a7', output)
        self.assertIn('mytitle', output)
        self.assertIn('Internet', output)

    def test_open_file_file_from_env_var(self):
        os.environ['KP_KEY_FILE'] = './passwordkey.key'
        output = self.kp_run('kp -d ./passwordkey.kdb list')
        self.assertIn('c4d301502050cd695e353b16094be4a7', output)
        self.assertIn('mytitle', output)
        self.assertIn('Internet', output)

    def test_open_with_password(self):
        output = self.kp_run('kp -d ./password.kdb list')
        self.assertIn('c4d301502050cd695e353b16094be4a7 ', output)
        self.assertIn('mytitle ', output)
        self.assertIn('Internet ', output)

    def test_get_password_exact(self):
        output = self.kp_run('kp -d ./password.kdb get -n mytitle password')
        self.assertIn('mypassword', output)

    def test_with_missing_command(self):
        with self.assertRaises(SystemExit):
            with capture_stderr() as captured:
                self.kp_run('kp ')
        stderr = captured.getvalue()
        self.assertIn('kp: error: too few arguments', stderr)
