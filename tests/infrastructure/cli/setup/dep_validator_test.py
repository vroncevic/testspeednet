# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
Info
    Unit tests for CLIBundleDependenciesValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.option.imanager import IOptionManager

from testspeednet.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator


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


class TestCLIBundleDependenciesValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        mock_service = DummyService()
        mock_parser = Mock(spec=IOptionManager)
        dependencies = {
            'service': mock_service,
            'parser': mock_parser,
            'commands': []
        }
        CLIBundleDependenciesValidator.validate(dependencies)
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(dependencies))

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate(None)
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate('invalid')
        self.assertFalse(CLIBundleDependenciesValidator.is_valid('invalid'))

    def test_validate_missing_dependency(self) -> None:
        dependencies = {
            'service': DummyService()
        }
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate(dependencies)
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(dependencies))


if __name__ == '__main__':
    unittest.main()
