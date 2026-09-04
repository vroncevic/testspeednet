# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
Info
    Unit tests for TestSpeedNetBundleValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.base.setup.bundle import BaseBundle

from testspeednet.setup.bundle import TestSpeedNetBundle
from testspeednet.setup.validator import TestSpeedNetBundleValidator


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


class TestTestSpeedNetBundleValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        bundle = TestSpeedNetBundle(
            base=Mock(spec=BaseBundle),
            service=DummyService(),
            subprocessor=DummySubProcessor(),
            cli=DummyCLI()
        )
        TestSpeedNetBundleValidator.validate(bundle)
        self.assertTrue(TestSpeedNetBundleValidator.is_valid(bundle))

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            TestSpeedNetBundleValidator.validate(None)
        self.assertFalse(TestSpeedNetBundleValidator.is_valid(None))

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            TestSpeedNetBundleValidator.validate('invalid')
        self.assertFalse(TestSpeedNetBundleValidator.is_valid('invalid'))


if __name__ == '__main__':
    unittest.main()
