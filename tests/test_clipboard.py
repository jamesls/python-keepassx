#!/usr/bin/env python

import unittest

import mock

from keepassx import clipboard


class TestClipboard(unittest.TestCase):
    def setUp(self):
        self.platform_patch = mock.patch('platform.system')
        self.platform = self.platform_patch.start()

    def tearDown(self):
        self.platform_patch.stop()

    def test_osx_clipboard(self):
        self.platform.return_value = 'Darwin'
        self.assertIsInstance(clipboard.get_clipboard(),
                              clipboard.OSXClipBoard)

    def test_linux_clipboard(self):
        self.platform.return_value = 'Linux'
        self.assertIsInstance(clipboard.get_clipboard(),
                              clipboard.LinuxClipboard)

    def test_unknown_platform_clipboard(self):
        self.platform.return_value = 'Unsupported'
        with self.assertRaises(ValueError):
            clipboard.get_clipboard()

    def test_copy_function(self):
        with mock.patch('keepassx.clipboard.OSXClipBoard.copy') as mock_copy:
            self.platform.return_value = 'Darwin'
            clipboard.copy('foo')
            mock_copy.assert_called_with('foo')

    def test_binary_written_to_stdin(self):
        unicode_password = u'\u2713'
        copier = clipboard.OSXClipBoard()
        with mock.patch('subprocess.Popen') as popen:
            popen.return_value.returncode = 0
            copier.copy(unicode_password)
            popen.return_value.communicate.assert_called_with(
                unicode_password.encode('utf-8'))
