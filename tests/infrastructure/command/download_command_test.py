# -*- coding: UTF-8 -*-

'''
Module
    download_command_test.py
Info
    Unit tests for DownloadCommandDefinition and DownloadCommandExecutor.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.service.iservice import IService
from testspeednet.infrastructure.command.download_command_definition import DownloadCommandDefinition
from testspeednet.infrastructure.command.download_command_executor import DownloadCommandExecutor


class TestDownloadCommand(unittest.TestCase):

    def test_definition(self) -> None:
        defn = DownloadCommandDefinition()
        self.assertEqual(defn.name, 'download')
        self.assertIn('download', defn.help_text)
        self.assertGreater(len(defn.options), 0)
        self.assertIn('DownloadCommandDefinition', str(defn))

    def test_executor_execute_success(self) -> None:
        defn = DownloadCommandDefinition()
        exec_ = DownloadCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True

        server = SpeedTestServer(
            id=1, server_id='1', url='http://test.org', lat=44.0, lon=20.0, distance=5.0,
            name='Belgrade', country='Serbia', cc='RS', sponsor='Telco', preferred=False, host='test.org:8080'
        )
        service.execute_download.return_value = (180.5, server)

        params = {'json': 'download.json'}
        res = exec_.execute(params=params, service=service)
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('Download: 180.5 Mbps', res.get('stdout', ''))
        service.export_json.assert_called_once()

    def test_executor_execute_failed(self) -> None:
        defn = DownloadCommandDefinition()
        exec_ = DownloadCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = True
        service.execute_download.return_value = (0.0, None)

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('no servers available', res.get('stderr', ''))

    def test_executor_execute_not_initialized(self) -> None:
        defn = DownloadCommandDefinition()
        exec_ = DownloadCommandExecutor(defn)
        service = Mock(spec=IService)
        service.is_initialized.return_value = False

        res = exec_.execute(params={}, service=service)
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('service not initialized', res.get('stderr', ''))

    def test_executor_properties(self) -> None:
        defn = DownloadCommandDefinition()
        exec_ = DownloadCommandExecutor(defn)
        self.assertEqual(exec_.get_definition(), defn)
        self.assertIn('DownloadCommandExecutor', str(exec_))


if __name__ == '__main__':
    unittest.main()
