# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
Info
    Unit tests for CLIBundleOptionsValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.option.imanager import IOptionManager

from testspeednet.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator


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


class TestCLIBundleOptionsValidator(unittest.TestCase):

    def test_validate_success(self) -> None:
        options = {
            'service': DummyService(),
            'parser': Mock(spec=IOptionManager)
        }
        CLIBundleOptionsValidator.validate(options)
        self.assertTrue(CLIBundleOptionsValidator.is_valid(options))

    def test_validate_none(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate(None)
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))

    def test_validate_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate('invalid')
        self.assertFalse(CLIBundleOptionsValidator.is_valid('invalid'))

    def test_is_valid_success(self) -> None:
        options = {
            'service': DummyService(),
            'parser': Mock(spec=IOptionManager)
        }
        self.assertTrue(CLIBundleOptionsValidator.is_valid(options))

    def test_is_valid_failure(self) -> None:
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))
        self.assertFalse(CLIBundleOptionsValidator.is_valid('invalid'))
        self.assertFalse(CLIBundleOptionsValidator.is_valid({'service': DummyService()}))


if __name__ == '__main__':
    unittest.main()
