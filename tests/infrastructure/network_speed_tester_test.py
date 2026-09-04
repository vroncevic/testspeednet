# -*- coding: UTF-8 -*-

'''
Module
    network_speed_tester_test.py
Info
    Unit tests for NetworkSpeedTester class.
'''

from __future__ import annotations

import io
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.infrastructure.network_speed_tester import NetworkSpeedTester


class TestNetworkSpeedTester(unittest.TestCase):

    def setUp(self) -> None:
        self.server = SpeedTestServer(
            id=1,
            server_id='101',
            url='http://sample.org/speedtest/upload.php',
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

    def test_init_and_str(self) -> None:
        tester = NetworkSpeedTester()
        self.assertTrue(tester.is_initialized())
        self.assertIn('NetworkSpeedTester', str(tester))

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_measure_ping_success(self, mock_urlopen: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'test'
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        tester = NetworkSpeedTester()
        ping = tester.measure_ping(self.server)
        self.assertGreaterEqual(ping, 0.0)

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_measure_ping_failure(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.side_effect = URLError('Connection failed')
        tester = NetworkSpeedTester()
        ping = tester.measure_ping(self.server)
        self.assertEqual(ping, 0.0)

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_measure_download_success(self, mock_urlopen: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'x' * 100000
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        tester = NetworkSpeedTester()
        speed = tester.measure_download(self.server)
        self.assertGreater(speed, 0.0)

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_measure_download_failure(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.side_effect = URLError('Download failed')
        tester = NetworkSpeedTester()
        speed = tester.measure_download(self.server)
        self.assertEqual(speed, 0.0)

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_measure_upload_success(self, mock_urlopen: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'OK'
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        tester = NetworkSpeedTester()
        speed = tester.measure_upload(self.server)
        self.assertGreater(speed, 0.0)

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_measure_upload_failure(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.side_effect = URLError('Upload failed')
        tester = NetworkSpeedTester()
        speed = tester.measure_upload(self.server)
        self.assertEqual(speed, 0.0)

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_fetch_servers_success(self, mock_urlopen: MagicMock) -> None:
        json_data = b'''[
            {
                "id": "1",
                "url": "http://speed.org",
                "lat": "44.0",
                "lon": "20.0",
                "distance": 10.5,
                "name": "Belgrade",
                "country": "Serbia",
                "cc": "RS",
                "sponsor": "Sponsor",
                "preferred": 1,
                "host": "speed.org:8080"
            }
        ]'''
        mock_resp = MagicMock()
        mock_resp.read.return_value = json_data
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        tester = NetworkSpeedTester()
        servers = tester.fetch_servers()
        self.assertGreater(len(servers), 0)
        self.assertEqual(servers[0].name, 'Belgrade')

    @patch('testspeednet.infrastructure.network_speed_tester.urlopen')
    def test_fetch_servers_failure(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.side_effect = URLError('Network error')
        tester = NetworkSpeedTester()
        servers = tester.fetch_servers()
        self.assertEqual(servers, [])


if __name__ == '__main__':
    unittest.main()
