# -*- coding: UTF-8 -*-

'''
Module
    speed_test_result_test.py
Info
    Unit tests for SpeedTestResult class.
'''

from __future__ import annotations

import unittest

from testspeednet.core.model.speed_test_result import SpeedTestResult


class TestSpeedTestResult(unittest.TestCase):

    def test_result_initialization(self) -> None:
        res = SpeedTestResult(
            download_speed=100.5,
            upload_speed=50.2,
            latency=15.3,
            server_name='Novi Sad',
            server_host='speedtest.rs:8080',
            timestamp='2026-09-04T12:00:00'
        )
        self.assertEqual(res.download_speed, 100.5)
        self.assertEqual(res.upload_speed, 50.2)
        self.assertEqual(res.latency, 15.3)
        self.assertEqual(res.server_name, 'Novi Sad')
        self.assertEqual(res.server_host, 'speedtest.rs:8080')
        self.assertEqual(res.timestamp, '2026-09-04T12:00:00')

    def test_result_none_optional_fields(self) -> None:
        res = SpeedTestResult(
            download_speed=0.0,
            upload_speed=0.0,
            latency=None,
            server_name=None,
            server_host=None,
            timestamp='2026-09-04T12:00:00'
        )
        self.assertIsNone(res.latency)
        self.assertIsNone(res.server_name)
        self.assertIsNone(res.server_host)


if __name__ == '__main__':
    unittest.main()
