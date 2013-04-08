#!/usr/bin/env python
"""Integration tests for the kp CLI.

These use subprocess to actually run the kp
command.

"""
import os
import unittest
from subprocess import check_output

from keepassx.main import main


class TestCLI(unittest.TestCase):
    # All tests are from the ./misc directory,
    # so that you can conveniently specify
    # password and keyfiles using relative paths.
    def setUp(self):
        self._original_dir = os.getcwd()
        misc_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'misc')
        os.chdir(misc_dir)

    def tearDown(self):
        os.chdir(self._original_dir)

    def kp_run(self, command):
        env = os.environ.copy()
        env['KP_INSECURE_PASSWORD'] = 'password'
        output = check_output(command, shell=True, env=env)
        return output

    def test_open_with_password_and_keyfile(self):
        output = self.kp_run('kp -d ./passwordkey.kdb -k ./passwordkey.key list')
        self.assertIn(
            'Entries:\n\nmytitle c4d301502050cd695e353b16094be4a7 Internet\n',
            output)

    def test_open_with_password(self):
        output = self.kp_run('kp -d ./password.kdb list')
        self.assertIn(
            'Entries:\n\nmytitle c4d301502050cd695e353b16094be4a7 Internet\n',
            output)


if __name__ == '__main__':
    unittest.main()
