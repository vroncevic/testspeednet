# -*- coding: UTF-8 -*-

'''
Module
    speed_command_test.py
Info
    Unit tests for SpeedCommandDefinition and SpeedCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from testspeednet.core.model.speed_test_result import SpeedTestResult
from testspeednet.core.service.iservice import IService
from testspeednet.infrastructure.command.command import CommandBundle
from testspeednet.infrastructure.command.speed_command_definition import SpeedCommandDefinition
from testspeednet.infrastructure.command.speed_command_executor import SpeedCommandExecutor


class TestSpeedCommand(unittest.TestCase):

    def test_definition(self) -> None:
        defn = SpeedCommandDefinition()
        self.assertEqual(defn.name, 'speed')
        self.assertIn('speed', defn.help_text)
        self.assertGreater(len(defn.options), 0)
        self.assertIn('SpeedCommandDefinition', str(defn))

    def test_bundle(self) -> None:
        defn = SpeedCommandDefinition()
        exec_ = SpeedCommandExecutor(defn)
        bundle = CommandBundle(definition=defn, executor=exec_)
        self.assertEqual(bundle.definition, defn)
        self.assertEqual(bundle.executor, exec_)

    def test_executor_execute_success(self) -> None:
        defn = SpeedCommandDefinition()
        exec_ = SpeedCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True

        result_obj = SpeedTestResult(
            download_speed=150.0,
            upload_speed=50.0,
            latency=15.0,
            server_name='Novi Sad',
            server_host='speed.rs:8080',
            timestamp='2026-09-04T12:00:00'
        )
        service.execute_speed.return_value = result_obj

        params = {'json': 'speed.json'}
        res = exec_.execute(params=params, service=service)
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('Download: 150.0 Mbps', res.get('stdout', ''))
        service.export_json.assert_called_once_with(data=result_obj, file_path='speed.json')

    def test_executor_execute_failed_measurement(self) -> None:
        defn = SpeedCommandDefinition()
        exec_ = SpeedCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True
        service.execute_speed.return_value = None

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('no servers available', res.get('stderr', ''))

    def test_executor_execute_not_initialized(self) -> None:
        defn = SpeedCommandDefinition()
        exec_ = SpeedCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = False

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('service not initialized', res.get('stderr', ''))

    def test_executor_properties(self) -> None:
        defn = SpeedCommandDefinition()
        exec_ = SpeedCommandExecutor(defn)
        self.assertEqual(exec_.get_definition(), defn)
        self.assertIn('SpeedCommandExecutor', str(exec_))


if __name__ == '__main__':
    unittest.main()
