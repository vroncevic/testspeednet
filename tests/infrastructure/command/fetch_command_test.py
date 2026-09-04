# -*- coding: UTF-8 -*-

'''
Module
    fetch_command_test.py
Info
    Unit tests for FetchCommandDefinition and FetchCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.service.iservice import IService
from testspeednet.infrastructure.command.fetch_command_definition import FetchCommandDefinition
from testspeednet.infrastructure.command.fetch_command_executor import FetchCommandExecutor


class TestFetchCommand(unittest.TestCase):

    def test_definition(self) -> None:
        defn = FetchCommandDefinition()
        self.assertEqual(defn.name, 'fetch')
        self.assertIn('fetch', defn.help_text.lower())
        self.assertIn('FetchCommandDefinition', str(defn))

    def test_executor_execute_success(self) -> None:
        defn = FetchCommandDefinition()
        exec_ = FetchCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True

        server = SpeedTestServer(
            id=1, server_id='1', url='http://test.org', lat=44.0, lon=20.0, distance=5.0,
            name='Novi Sad', country='Serbia', cc='RS', sponsor='Telco', preferred=False, host='test.org:8080'
        )
        service.fetch_servers.return_value = [server]

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('Successfully fetched and saved 1 servers', res.get('stdout', ''))

    def test_executor_execute_with_json(self) -> None:
        defn = FetchCommandDefinition()
        exec_ = FetchCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True

        server = SpeedTestServer(
            id=1, server_id='1', url='http://test.org', lat=44.0, lon=20.0, distance=5.0,
            name='Novi Sad', country='Serbia', cc='RS', sponsor='Telco', preferred=False, host='test.org:8080'
        )
        service.fetch_servers.return_value = [server]

        res = exec_.execute(params={'json': 'servers.json'}, service=service)
        self.assertEqual(res.get('returncode'), 0)
        service.export_json.assert_called_once_with(data=[server], file_path='servers.json')

    def test_executor_execute_empty(self) -> None:
        defn = FetchCommandDefinition()
        exec_ = FetchCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True
        service.fetch_servers.return_value = []

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('Successfully fetched and saved 0 servers', res.get('stdout', ''))

    def test_executor_execute_not_initialized(self) -> None:
        defn = FetchCommandDefinition()
        exec_ = FetchCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = False

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('service not initialized', res.get('stderr', ''))

    def test_executor_properties(self) -> None:
        defn = FetchCommandDefinition()
        exec_ = FetchCommandExecutor(defn)
        self.assertEqual(exec_.get_definition(), defn)
        self.assertIn('FetchCommandExecutor', str(exec_))


if __name__ == '__main__':
    unittest.main()
