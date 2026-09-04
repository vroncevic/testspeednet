# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
Info
    Unit tests for CLIBundleValidator class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.option.imanager import IOptionManager

from testspeednet.infrastructure.cli.setup.bundle import CLIBundle
from testspeednet.infrastructure.cli.setup.validator import CLIBundleValidator


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


class TestCLIBundleValidator(unittest.TestCase):

    def test_validate_bundle_success(self) -> None:
        bundle = CLIBundle(
            service=DummyService(),
            parser=Mock(spec=IOptionManager),
            commands=[]
        )
        CLIBundleValidator.validate(bundle)
        self.assertTrue(CLIBundleValidator.is_valid(bundle))

    def test_validate_bundle_none(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleValidator.validate(None)
        self.assertFalse(CLIBundleValidator.is_valid(None))

    def test_validate_bundle_invalid_type(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleValidator.validate('invalid')
        self.assertFalse(CLIBundleValidator.is_valid('invalid'))


if __name__ == '__main__':
    unittest.main()
