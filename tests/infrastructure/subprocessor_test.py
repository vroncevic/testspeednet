# -*- coding: UTF-8 -*-

'''
Module
    subprocessor_test.py
Info
    Unit tests for SubProcessor class.
'''

from __future__ import annotations

import unittest
from unittest.mock import Mock

from ats_utilities.exceptions import ATSTypeError, ATSValueError

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.service.inetwork_speed_tester import INetworkSpeedTester
from testspeednet.infrastructure.subprocessor import SubProcessor


class MockSpeedTester:

    def __init__(self, init: bool = True) -> None:
        self._init = init

    def fetch_servers(self) -> list[SpeedTestServer]:
        return [
            SpeedTestServer(
                id=1,
                server_id='1',
                url='http://test.org',
                lat=44.0,
                lon=20.0,
                distance=5.0,
                name='City',
                country='Serbia',
                cc='RS',
                sponsor='ISP',
                preferred=False,
                host='test.org:8080'
            )
        ]

    def measure_ping(self, server: SpeedTestServer) -> float:
        return 15.5

    def measure_download(self, server: SpeedTestServer) -> float:
        return 120.0

    def measure_upload(self, server: SpeedTestServer) -> float:
        return 45.0

    def is_initialized(self) -> bool:
        return self._init

    def __str__(self) -> str:
        return 'MockSpeedTester'


class TestSubProcessor(unittest.TestCase):

    def setUp(self) -> None:
        self.server = SpeedTestServer(
            id=1,
            server_id='1',
            url='http://test.org',
            lat=44.0,
            lon=20.0,
            distance=5.0,
            name='City',
            country='Serbia',
            cc='RS',
            sponsor='ISP',
            preferred=False,
            host='test.org:8080'
        )

    def test_init_success_and_str(self) -> None:
        tester = MockSpeedTester()
        sub = SubProcessor(tester)
        self.assertTrue(sub.is_initialized())
        self.assertIn('SubProcessor', str(sub))

    def test_init_validation_failures(self) -> None:
        with self.assertRaises(ATSValueError):
            SubProcessor(None)

        with self.assertRaises(ATSTypeError):
            SubProcessor('not_a_tester')

    def test_run_fetch(self) -> None:
        tester = MockSpeedTester()
        sub = SubProcessor(tester)
        result = sub.run(params={'cmd': 'fetch'})
        self.assertIn('servers', result)
        self.assertEqual(len(result['servers']), 1)

    def test_run_no_target_server(self) -> None:
        tester = MockSpeedTester()
        sub = SubProcessor(tester)
        result = sub.run(params={'cmd': 'speed'})
        self.assertEqual(result, {'error': 'no target server provided'})

    def test_run_speed(self) -> None:
        tester = MockSpeedTester()
        sub = SubProcessor(tester)
        result = sub.run(params={'cmd': 'speed', 'server': self.server})
        self.assertEqual(result.get('ping'), 15.5)
        self.assertEqual(result.get('download'), 120.0)
        self.assertEqual(result.get('upload'), 45.0)

    def test_run_download(self) -> None:
        tester = MockSpeedTester()
        sub = SubProcessor(tester)
        result = sub.run(params={'cmd': 'download', 'server': self.server})
        self.assertEqual(result.get('download'), 120.0)

    def test_run_upload(self) -> None:
        tester = MockSpeedTester()
        sub = SubProcessor(tester)
        result = sub.run(params={'cmd': 'upload', 'server': self.server})
        self.assertEqual(result.get('upload'), 45.0)

    def test_run_unknown_command(self) -> None:
        tester = MockSpeedTester()
        sub = SubProcessor(tester)
        result = sub.run(params={'cmd': 'unknown', 'server': self.server})
        self.assertEqual(result, {'error': 'unknown command: unknown'})

    def test_is_initialized_false(self) -> None:
        tester = MockSpeedTester(init=False)
        sub = SubProcessor(tester)
        self.assertFalse(sub.is_initialized())


if __name__ == '__main__':
    unittest.main()
