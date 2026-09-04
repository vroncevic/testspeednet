# -*- coding: UTF-8 -*-

'''
Module
    history_command_test.py
Info
    Unit tests for HistoryCommandDefinition and HistoryCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from testspeednet.core.model.speed_test_stat import SpeedTestStat
from testspeednet.core.service.iservice import IService
from testspeednet.infrastructure.command.history_command_definition import HistoryCommandDefinition
from testspeednet.infrastructure.command.history_command_executor import HistoryCommandExecutor


class TestHistoryCommand(unittest.TestCase):

    def test_definition(self) -> None:
        defn = HistoryCommandDefinition()
        self.assertEqual(defn.name, 'history')
        self.assertIn('history', defn.help_text.lower())
        self.assertGreater(len(defn.options), 0)
        self.assertIn('HistoryCommandDefinition', str(defn))

    def test_executor_execute_success(self) -> None:
        defn = HistoryCommandDefinition()
        exec_ = HistoryCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True

        stat = SpeedTestStat(
            id=1,
            timestamp='2026-09-04T12:00:00',
            operation='speed',
            download_speed=150.0,
            upload_speed=50.0,
            latency=15.0,
            server_name='Novi Sad',
            server_host='speed.rs:8080'
        )
        service.get_history.return_value = [stat]

        params = {'limit': 5, 'json': 'history.json'}
        res = exec_.execute(params=params, service=service)
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('Novi Sad', res.get('stdout', ''))
        service.get_history.assert_called_once_with(limit=5)
        service.export_json.assert_called_once()

    def test_executor_execute_empty_history(self) -> None:
        defn = HistoryCommandDefinition()
        exec_ = HistoryCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True
        service.get_history.return_value = []

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('ID', res.get('stdout', ''))

    def test_executor_execute_not_initialized(self) -> None:
        defn = HistoryCommandDefinition()
        exec_ = HistoryCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = False

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('service not initialized', res.get('stderr', ''))

    def test_executor_properties(self) -> None:
        defn = HistoryCommandDefinition()
        exec_ = HistoryCommandExecutor(defn)
        self.assertEqual(exec_.get_definition(), defn)
        self.assertIn('HistoryCommandExecutor', str(exec_))


if __name__ == '__main__':
    unittest.main()
