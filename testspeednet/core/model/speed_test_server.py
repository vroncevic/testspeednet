# -*- coding: UTF-8 -*-

'''
Module
    speed_test_server.py
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
    Defines domain entity SpeedTestServer.
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
class SpeedTestServer:
    '''
        Defines domain entity SpeedTestServer.

        It defines:

            :attributes:
                | id - Integer unique identifier.
                | server_id - Server identifier from speed test API.
                | url - Speed test server URL.
                | lat - Latitude coordinate of the server.
                | lon - Longitude coordinate of the server.
                | distance - Distance to the server in kilometers.
                | name - City or location name.
                | country - Full country name.
                | cc - Two-letter country code.
                | sponsor - Sponsor organisation name.
                | preferred - Flag indicating preferred status.
                | host - Host address of the server.
            :methods:
                | None.
    '''

    id: int
    server_id: str
    url: str
    lat: float
    lon: float
    distance: float
    name: str
    country: str
    cc: str
    sponsor: str
    preferred: bool
    host: str
