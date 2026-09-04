# -*- coding: UTF-8 -*-

'''
Module
    speed_test_stat.py
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
    Defines domain entity SpeedTestStat for measurement history.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


@dataclass(slots=True, frozen=True)
class SpeedTestStat:
    '''
        Defines domain entity SpeedTestStat for measurement history.

        It defines:

            :attributes:
                | id - Primary key identifier or None for new records.
                | timestamp - UTC timestamp in ISO 8601 format.
                | operation - Type of operation performed.
                | download_speed - Download speed in Mbps.
                | upload_speed - Upload speed in Mbps.
                | latency - Latency in milliseconds.
                | server_name - Name of the test server.
                | server_host - Host of the test server.
            :methods:
                | None.
    '''

    id: int | None
    timestamp: str
    operation: str
    download_speed: float
    upload_speed: float
    latency: float | None
    server_name: str | None
    server_host: str | None
