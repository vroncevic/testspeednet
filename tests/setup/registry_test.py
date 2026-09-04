# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
Info
    Unit tests for TestSpeedNetBundleRegistry class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.base.setup.bundle import BaseBundle

from testspeednet.setup.bundle import TestSpeedNetBundle
from testspeednet.setup.registry import TestSpeedNetBundleRegistry


class DummyService:

    def execute_speed(self, server_id: int | None = None) -> object:
        return None

    def execute_download(self, server_id: int | None = None) -> object:
        return None

    def execute_upload(self, server_id: int | None = None) -> object:
        return None

    def fetch_servers(self) -> Sequence[object]:
        return ()

    def get_history(self, limit: int = 10) -> Sequence[object]:
        return ()

    def export_json(self, data: object, file_path: str) -> bool:
        return True

    def load_json(self, file_path: str) -> dict[str, object] | None:
        return {}

    def is_initialized(self) -> bool:
        return True


class DummySubProcessor:

    def run(self, *, params: object) -> dict[str, object]:
        return {}

    def is_initialized(self) -> bool:
        return True


class DummyCLI:

    def run(self) -> dict[str, object]:
        return {}

    def is_initialized(self) -> bool:
        return True


class TestTestSpeedNetBundleRegistry(unittest.TestCase):

    def test_create_bundle_success(self) -> None:
        deps = {
            'base': Mock(spec=BaseBundle),
            'service': DummyService(),
            'subprocessor': DummySubProcessor(),
            'cli': DummyCLI()
        }
        bundle = TestSpeedNetBundleRegistry.create_bundle(deps)
        self.assertIsInstance(bundle, TestSpeedNetBundle)

    def test_create_bundle_invalid(self) -> None:
        with self.assertRaises(Exception):
            TestSpeedNetBundleRegistry.create_bundle({'base': Mock(spec=BaseBundle)})

    def test_get_version(self) -> None:
        self.assertEqual(TestSpeedNetBundleRegistry.get_version(), '2.0.0')


if __name__ == '__main__':
    unittest.main()
