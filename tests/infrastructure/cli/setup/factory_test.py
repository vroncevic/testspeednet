# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
Info
    Unit tests for CLIBundleFactory class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.option.imanager import IOptionManager

from testspeednet.infrastructure.cli.setup.bundle import CLIBundle
from testspeednet.infrastructure.cli.setup.factory import CLIBundleFactory


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


class TestCLIBundleFactory(unittest.TestCase):

    def test_create_bundle_success(self) -> None:
        opts = {
            'service': DummyService(),
            'parser': Mock(spec=IOptionManager)
        }
        bundle = CLIBundleFactory.create_bundle(opts)
        self.assertIsInstance(bundle, CLIBundle)

    def test_create_bundle_invalid(self) -> None:
        with self.assertRaises(Exception):
            CLIBundleFactory.create_bundle(None)

    def test_get_version(self) -> None:
        self.assertEqual(CLIBundleFactory.get_version(), '2.0.0')


if __name__ == '__main__':
    unittest.main()
