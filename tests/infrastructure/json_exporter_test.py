# -*- coding: UTF-8 -*-

'''
Module
    json_exporter_test.py
Info
    Unit tests for JsonExporter class.
'''

from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from ats_utilities.context.factory import ContextBundleFactory

from testspeednet.core.model.speed_test_result import SpeedTestResult
from testspeednet.infrastructure.json_exporter import JsonExporter


class TestJsonExporter(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_init_and_str(self) -> None:
        ctx = ContextBundleFactory.create_bundle()
        exp1 = JsonExporter(context_bundle=ctx)
        exp2 = JsonExporter()
        self.assertTrue(exp1.is_initialized())
        self.assertTrue(exp2.is_initialized())
        self.assertIn('JsonExporter', str(exp1))

    def test_export_and_load_dict(self) -> None:
        exp = JsonExporter()
        file_path = os.path.join(self.tmp_dir.name, 'test_dict.json')
        payload = {'status': 'ok', 'code': 200}
        success = exp.export_json(payload, file_path)
        self.assertTrue(success)

        loaded = exp.load_json(file_path)
        self.assertEqual(loaded.get('status'), 'ok')
        self.assertEqual(loaded.get('code'), 200)

    def test_export_dataclass(self) -> None:
        exp = JsonExporter()
        file_path = os.path.join(self.tmp_dir.name, 'test_dc.json')
        res = SpeedTestResult(
            download_speed=100.0,
            upload_speed=50.0,
            latency=10.0,
            server_name='Novi Sad',
            server_host='speedtest.rs:8080',
            timestamp='2026-09-04T12:00:00'
        )
        self.assertTrue(exp.export_json(res, file_path))
        loaded = exp.load_json(file_path)
        self.assertEqual(loaded.get('download_speed'), 100.0)

    def test_export_list(self) -> None:
        exp = JsonExporter()
        file_path = os.path.join(self.tmp_dir.name, 'test_list.json')
        items = [{'a': 1}, {'b': 2}]
        self.assertTrue(exp.export_json(items, file_path))
        loaded = exp.load_json(file_path)
        self.assertEqual(loaded.get('count'), 2)

    def test_export_primitive(self) -> None:
        exp = JsonExporter()
        file_path = os.path.join(self.tmp_dir.name, 'test_prim.json')
        self.assertTrue(exp.export_json('simple_string', file_path))
        loaded = exp.load_json(file_path)
        self.assertEqual(loaded.get('data'), 'simple_string')

    def test_export_failure_exception(self) -> None:
        exp = JsonExporter()
        # Invalid directory path that cannot be created
        with patch('pathlib.Path.resolve', side_effect=Exception('Path error')):
            self.assertFalse(exp.export_json({}, 'invalid/path.json'))

    def test_load_non_existent(self) -> None:
        exp = JsonExporter()
        loaded = exp.load_json('/non/existent/file.json')
        self.assertEqual(loaded, {})

    def test_load_exception(self) -> None:
        exp = JsonExporter()
        with patch('pathlib.Path.resolve', side_effect=Exception('Load error')):
            self.assertEqual(exp.load_json('file.json'), {})


if __name__ == '__main__':
    unittest.main()
