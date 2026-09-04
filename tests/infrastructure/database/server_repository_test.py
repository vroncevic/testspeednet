# -*- coding: UTF-8 -*-

'''
Module
    server_repository_test.py
Info
    Unit tests for ServerRepository class.
'''

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.model.speed_test_stat import SpeedTestStat
from testspeednet.infrastructure.database.server_repository import ServerRepository


class TestServerRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, 'test.db')
        self.repo = ServerRepository(self.db_path)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_init_success_and_str(self) -> None:
        self.assertTrue(self.repo.is_initialized())
        self.assertIn('ServerRepository', str(self.repo))

    def test_init_failure(self) -> None:
        repo = ServerRepository('/non_existent_directory/invalid_db.db')
        self.assertFalse(repo.is_initialized())

    def test_save_and_get_servers(self) -> None:
        server = SpeedTestServer(
            id=1,
            server_id='101',
            url='http://sample.org',
            lat=44.8,
            lon=20.4,
            distance=10.0,
            name='Belgrade',
            country='Serbia',
            cc='RS',
            sponsor='Telco',
            preferred=True,
            host='sample.org:8080'
        )
        saved = self.repo.save_servers(servers=[server])
        self.assertTrue(saved)

        retrieved = self.repo.get_servers()
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0].server_id, '101')
        self.assertEqual(retrieved[0].name, 'Belgrade')
        self.assertTrue(retrieved[0].preferred)

    def test_save_and_get_servers_uninitialized(self) -> None:
        repo = ServerRepository('/non_existent_directory/invalid_db.db')
        self.assertFalse(repo.save_servers(servers=[]))
        self.assertEqual(repo.get_servers(), [])

    def test_save_servers_error(self) -> None:
        with patch('sqlite3.connect', side_effect=sqlite3.Error('DB error')):
            self.assertFalse(self.repo.save_servers(servers=[]))

    def test_get_servers_error(self) -> None:
        with patch('sqlite3.connect', side_effect=sqlite3.Error('DB error')):
            self.assertEqual(self.repo.get_servers(), [])

    def test_save_and_get_statistics(self) -> None:
        stat = SpeedTestStat(
            id=None,
            timestamp='2026-09-04T12:00:00',
            operation='speed',
            download_speed=150.0,
            upload_speed=50.0,
            latency=15.0,
            server_name='Novi Sad',
            server_host='speedtest.rs:8080'
        )
        saved = self.repo.save_statistic(stat=stat)
        self.assertTrue(saved)

        history = self.repo.get_statistics(limit=10)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].operation, 'speed')
        self.assertEqual(history[0].download_speed, 150.0)
        self.assertEqual(history[0].latency, 15.0)

    def test_save_and_get_statistics_uninitialized(self) -> None:
        repo = ServerRepository('/non_existent_directory/invalid_db.db')
        stat = SpeedTestStat(
            id=None,
            timestamp='2026-09-04T12:00:00',
            operation='speed',
            download_speed=150.0,
            upload_speed=50.0,
            latency=15.0,
            server_name='Novi Sad',
            server_host='speedtest.rs:8080'
        )
        self.assertFalse(repo.save_statistic(stat=stat))
        self.assertEqual(repo.get_statistics(), [])

    def test_save_statistic_error(self) -> None:
        stat = SpeedTestStat(
            id=None,
            timestamp='2026-09-04T12:00:00',
            operation='speed',
            download_speed=150.0,
            upload_speed=50.0,
            latency=15.0,
            server_name='Novi Sad',
            server_host='speedtest.rs:8080'
        )
        with patch('sqlite3.connect', side_effect=sqlite3.Error('DB error')):
            self.assertFalse(self.repo.save_statistic(stat=stat))

    def test_get_statistics_error(self) -> None:
        with patch('sqlite3.connect', side_effect=sqlite3.Error('DB error')):
            self.assertEqual(self.repo.get_statistics(), [])


if __name__ == '__main__':
    unittest.main()
