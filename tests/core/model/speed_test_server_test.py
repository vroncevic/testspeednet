# -*- coding: UTF-8 -*-

'''
Module
    speed_test_server_test.py
Info
    Unit tests for SpeedTestServer class.
'''

from __future__ import annotations

import unittest

from testspeednet.core.model.speed_test_server import SpeedTestServer


class TestSpeedTestServer(unittest.TestCase):

    def test_server_initialization(self) -> None:
        server = SpeedTestServer(
            id=1,
            server_id='101',
            url='http://server.org',
            lat=44.8,
            lon=20.4,
            distance=12.5,
            name='Belgrade',
            country='Serbia',
            cc='RS',
            sponsor='Telco',
            preferred=True,
            host='server.org:8080'
        )
        self.assertEqual(server.id, 1)
        self.assertEqual(server.server_id, '101')
        self.assertEqual(server.url, 'http://server.org')
        self.assertEqual(server.lat, 44.8)
        self.assertEqual(server.lon, 20.4)
        self.assertEqual(server.distance, 12.5)
        self.assertEqual(server.name, 'Belgrade')
        self.assertEqual(server.country, 'Serbia')
        self.assertEqual(server.cc, 'RS')
        self.assertEqual(server.sponsor, 'Telco')
        self.assertTrue(server.preferred)
        self.assertEqual(server.host, 'server.org:8080')


if __name__ == '__main__':
    unittest.main()
