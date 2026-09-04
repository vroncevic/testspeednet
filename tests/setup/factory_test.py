# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
Info
    Unit tests for TestSpeedNetBundleFactory class.
'''

from __future__ import annotations

import unittest

from testspeednet.setup.bundle import TestSpeedNetBundle
from testspeednet.setup.factory import TestSpeedNetBundleFactory


class TestTestSpeedNetBundleFactory(unittest.TestCase):

    def test_create_bundle_default(self) -> None:
        bundle = TestSpeedNetBundleFactory.create_bundle()
        self.assertIsInstance(bundle, TestSpeedNetBundle)

    def test_create_bundle_with_options(self) -> None:
        opts = {'info_file': 'testspeednet/infrastructure/config/testspeednet.cfg'}
        bundle = TestSpeedNetBundleFactory.create_bundle(opts)
        self.assertIsInstance(bundle, TestSpeedNetBundle)

    def test_create_bundle_invalid_options(self) -> None:
        opts = {'info_file': 123}
        with self.assertRaises(Exception):
            TestSpeedNetBundleFactory.create_bundle(opts)

    def test_get_version(self) -> None:
        self.assertEqual(TestSpeedNetBundleFactory.get_version(), '2.0.0')


if __name__ == '__main__':
    unittest.main()
