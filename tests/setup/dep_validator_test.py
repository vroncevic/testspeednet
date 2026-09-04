# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
Info
    Unit tests for TestSpeedNetBundleDependenciesValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.base.setup.bundle import BaseBundle

from testspeednet.setup.dep_validator import TestSpeedNetBundleDependenciesValidator


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


class TestTestSpeedNetBundleDependenciesValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        mock_base = Mock(spec=BaseBundle)
        dependencies = {
            'base': mock_base,
            'service': DummyService(),
            'subprocessor': DummySubProcessor(),
            'cli': DummyCLI()
        }
        TestSpeedNetBundleDependenciesValidator.validate(dependencies)
        self.assertTrue(TestSpeedNetBundleDependenciesValidator.is_valid(dependencies))

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            TestSpeedNetBundleDependenciesValidator.validate(None)
        self.assertFalse(TestSpeedNetBundleDependenciesValidator.is_valid(None))

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            TestSpeedNetBundleDependenciesValidator.validate('invalid')
        self.assertFalse(TestSpeedNetBundleDependenciesValidator.is_valid('invalid'))

    def test_validate_missing_dependency(self) -> None:
        deps = {'base': Mock(spec=BaseBundle)}
        with self.assertRaises(Exception):
            TestSpeedNetBundleDependenciesValidator.validate(deps)
        self.assertFalse(TestSpeedNetBundleDependenciesValidator.is_valid(deps))


if __name__ == '__main__':
    unittest.main()
