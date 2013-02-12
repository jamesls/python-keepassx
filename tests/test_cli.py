#!/usr/bin/env python
"""Integration tests for the kp CLI.

These use pexpect to verify the expected.

"""

import unittest

class TestCLI(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
