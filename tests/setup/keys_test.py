# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
Info
    Unit tests for TestSpeedNetBundleKeys class.
'''

from __future__ import annotations

import unittest
from types import MappingProxyType

from testspeednet.setup.keys import TestSpeedNetBundleKeys


class TestTestSpeedNetBundleKeys(unittest.TestCase):

    def test_get_dependency_to_type(self) -> None:
        deps = TestSpeedNetBundleKeys.get_dependency_to_type()
        self.assertIsInstance(deps, MappingProxyType)
        self.assertIn(TestSpeedNetBundleKeys.DEPENDENCY_BASE, deps)
        self.assertIn(TestSpeedNetBundleKeys.DEPENDENCY_SERVICE, deps)
        self.assertIn(TestSpeedNetBundleKeys.DEPENDENCY_SUBPROCESSOR, deps)
        self.assertIn(TestSpeedNetBundleKeys.DEPENDENCY_CLI, deps)

    def test_get_option_to_type(self) -> None:
        opts = TestSpeedNetBundleKeys.get_option_to_type()
        self.assertIsInstance(opts, MappingProxyType)
        self.assertIn(TestSpeedNetBundleKeys.OPTION_INFO_FILE, opts)


if __name__ == '__main__':
    unittest.main()
