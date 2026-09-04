# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
Info
    Unit tests for CLIBundle class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from collections.abc import Sequence
from ats_utilities.option.imanager import IOptionManager

from testspeednet.infrastructure.cli.setup.bundle import CLIBundle


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


class TestCLIBundle(unittest.TestCase):

    def test_bundle_creation_and_to_dict(self) -> None:
        svc = DummyService()
        parser = Mock(spec=IOptionManager)
        bundle = CLIBundle(service=svc, parser=parser, commands=[])

        self.assertEqual(bundle.service, svc)
        self.assertEqual(bundle.parser, parser)
        self.assertEqual(bundle.commands, [])

        d = bundle.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d.get('service'), svc)


if __name__ == '__main__':
    unittest.main()
