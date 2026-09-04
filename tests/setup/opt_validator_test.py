# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
Info
    Unit tests for TestSpeedNetBundleOptionsValidator class.
'''

from __future__ import annotations

import unittest

from testspeednet.setup.opt_validator import TestSpeedNetBundleOptionsValidator


class TestTestSpeedNetBundleOptionsValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        opts = {'info_file': 'testspeednet/infrastructure/config/testspeednet.cfg'}
        TestSpeedNetBundleOptionsValidator.validate(opts)
        self.assertTrue(TestSpeedNetBundleOptionsValidator.is_valid(opts))

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            TestSpeedNetBundleOptionsValidator.validate(None)
        self.assertFalse(TestSpeedNetBundleOptionsValidator.is_valid(None))

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            TestSpeedNetBundleOptionsValidator.validate('invalid')
        self.assertFalse(TestSpeedNetBundleOptionsValidator.is_valid('invalid'))

    def test_validate_invalid_option_value(self) -> None:
        opts = {'info_file': 123}
        with self.assertRaises(Exception):
            TestSpeedNetBundleOptionsValidator.validate(opts)
        self.assertFalse(TestSpeedNetBundleOptionsValidator.is_valid(opts))


if __name__ == '__main__':
    unittest.main()
