# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
Info
    Unit tests for CLIBundleKeys class.
'''

from __future__ import annotations

from types import MappingProxyType
import unittest

from testspeednet.infrastructure.cli.setup.keys import CLIBundleKeys


class TestCLIBundleKeys(unittest.TestCase):

    def test_get_dependency_to_type(self) -> None:
        deps = CLIBundleKeys.get_dependency_to_type()
        self.assertIsInstance(deps, MappingProxyType)
        self.assertIn('service', deps)
        self.assertIn('parser', deps)
        self.assertIn('commands', deps)

    def test_get_option_to_type(self) -> None:
        opts = CLIBundleKeys.get_option_to_type()
        self.assertIsInstance(opts, MappingProxyType)
        self.assertIn('service', opts)
        self.assertIn('parser', opts)


if __name__ == '__main__':
    unittest.main()
