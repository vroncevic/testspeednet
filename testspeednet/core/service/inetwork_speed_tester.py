# -*- coding: UTF-8 -*-

'''
Module
    inetwork_speed_tester.py
Copyright
    Copyright (C) 2016 - 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    testspeednet is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    testspeednet is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines abstract interface for network speed testing adapter.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from testspeednet.core.model.speed_test_server import SpeedTestServer

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


@runtime_checkable
class INetworkSpeedTester(Protocol):
    '''
        Defines abstract interface for network speed testing adapter.

        It defines:

            :methods:
                | measure_ping - Measures ping latency to target server.
                | measure_download - Measures download speed from target server.
                | measure_upload - Measures upload speed to target server.
                | fetch_servers - Fetches servers from remote API.
                | is_initialized - Checks if the tester is initialized.
    '''

    def measure_ping(self, server: SpeedTestServer) -> float:
        '''
            Measures ping latency to target server.

            :param server: Speed test server.
            :return: Latency in milliseconds.
            :exceptions: None.
        '''

    def measure_download(self, server: SpeedTestServer) -> float:
        '''
            Measures download speed from target server.

            :param server: Speed test server.
            :return: Download speed in Mbps.
            :exceptions: None.
        '''

    def measure_upload(self, server: SpeedTestServer) -> float:
        '''
            Measures upload speed to target server.

            :param server: Speed test server.
            :return: Upload speed in Mbps.
            :exceptions: None.
        '''

    def fetch_servers(self) -> list[SpeedTestServer]:
        '''
            Fetches servers from remote API.

            :return: List of fetched servers.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if the tester is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
