# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
Info
    Unit tests for TestSpeedNet engine.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.exceptions import ATSValueError

from collections.abc import Sequence
from testspeednet.engine import TestSpeedNet
from testspeednet.setup.bundle import TestSpeedNetBundle
from testspeednet.setup.factory import TestSpeedNetBundleFactory


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

    def __str__(self) -> str:
        return 'DummyService'


class DummySubProcessor:

    def run(self, *, params: object) -> dict[str, object]:
        return {}

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummySubProcessor'


class DummyCLI:

    def __init__(self, return_code: int = 0, stderr: str = '', stdout: str = '') -> None:
        self.return_code = return_code
        self.stderr = stderr
        self.stdout = stdout

    def run(self) -> dict[str, object]:
        return {
            'returncode': self.return_code,
            'stderr': self.stderr,
            'stdout': self.stdout
        }

    def is_initialized(self) -> bool:
        return True

    def __str__(self) -> str:
        return 'DummyCLI'


class TestTestSpeedNet(unittest.TestCase):

    def test_engine_init_success(self) -> None:
        bundle = TestSpeedNetBundleFactory.create_bundle()
        engine = TestSpeedNet(bundle)
        self.assertTrue(engine.is_initialized())

    def test_engine_init_fail_validation(self) -> None:
        engine = TestSpeedNet(None)
        self.assertFalse(engine.is_initialized())

    def test_engine_process_success(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='testspeednet/infrastructure/config/testspeednet.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI(return_code=0, stdout='speed measurement ok')

        bundle = TestSpeedNetBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )
        engine = TestSpeedNet(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertTrue(engine.process())

    def test_engine_process_cli_failure(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='testspeednet/infrastructure/config/testspeednet.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI(return_code=1, stderr='CLI error')

        bundle = TestSpeedNetBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )
        engine = TestSpeedNet(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_not_initialized(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='testspeednet/infrastructure/config/testspeednet.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()
        mock_base.option_manager.is_initialized = Mock(return_value=False)

        bundle = TestSpeedNetBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )
        engine = TestSpeedNet(bundle)
        self.assertFalse(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_exception(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='testspeednet/infrastructure/config/testspeednet.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=Exception('Unexpected error'))

        bundle = TestSpeedNetBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )
        engine = TestSpeedNet(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_validation_exception(self) -> None:
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='testspeednet/infrastructure/config/testspeednet.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=ATSValueError('Validation error in run'))

        bundle = TestSpeedNetBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )
        engine = TestSpeedNet(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    @patch('testspeednet.setup.validator.TestSpeedNetBundleValidator.validate')
    def test_engine_init_generic_exception(self, mock_validate: Mock) -> None:
        mock_validate.side_effect = Exception('Unexpected generic validation error')
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='testspeednet/infrastructure/config/testspeednet.cfg',
                use_generator=True,
                context_bundle=context_bundle
            )
        )
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        bundle = TestSpeedNetBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )
        engine = TestSpeedNet(bundle)
        self.assertFalse(engine.is_initialized())


if __name__ == '__main__':
    unittest.main()
