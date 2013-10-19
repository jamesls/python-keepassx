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


if __name__ == '__main__':
    unittest.main()
