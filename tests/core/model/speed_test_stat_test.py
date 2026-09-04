# -*- coding: UTF-8 -*-

'''
Module
    speed_test_stat_test.py
Info
    Unit tests for SpeedTestStat class.
'''

from __future__ import annotations

import unittest

from testspeednet.core.model.speed_test_stat import SpeedTestStat


class TestSpeedTestStat(unittest.TestCase):

    def test_stat_initialization(self) -> None:
        stat = SpeedTestStat(
            id=1,
            timestamp='2026-09-04T12:00:00',
            operation='speed',
            download_speed=150.0,
            upload_speed=40.0,
            latency=15.0,
            server_name='Novi Sad',
            server_host='speedtest.rs:8080'
        )
        self.assertEqual(stat.id, 1)
        self.assertEqual(stat.timestamp, '2026-09-04T12:00:00')
        self.assertEqual(stat.operation, 'speed')
        self.assertEqual(stat.download_speed, 150.0)
        self.assertEqual(stat.upload_speed, 40.0)
        self.assertEqual(stat.latency, 15.0)
        self.assertEqual(stat.server_name, 'Novi Sad')
        self.assertEqual(stat.server_host, 'speedtest.rs:8080')

    def test_stat_none_optional_fields(self) -> None:
        stat = SpeedTestStat(
            id=None,
            timestamp='2026-09-04T12:00:00',
            operation='download',
            download_speed=200.0,
            upload_speed=0.0,
            latency=None,
            server_name=None,
            server_host=None
        )
        self.assertIsNone(stat.id)
        self.assertIsNone(stat.latency)
        self.assertIsNone(stat.server_name)
        self.assertIsNone(stat.server_host)


if __name__ == '__main__':
    unittest.main()
