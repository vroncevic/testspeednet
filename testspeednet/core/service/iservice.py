# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines abstract interface for speed test orchestration service.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from testspeednet.core.model.speed_test_result import SpeedTestResult
from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.model.speed_test_stat import SpeedTestStat

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


@runtime_checkable
class IService(Protocol):
    '''
        Defines abstract interface for speed test orchestration service.

        It defines:

            :methods:
                | execute_speed - Runs speed measurement and records statistics.
                | execute_download - Runs download measurement and records statistics.
                | execute_upload - Runs upload measurement and records statistics.
                | fetch_servers - Fetches available servers and stores them.
                | get_history - Retrieves measurement statistics from database.
                | export_json - Exports data object to JSON file.
                | load_json - Loads configuration dictionary from JSON file.
                | is_initialized - Checks if the service is initialized.
    '''

    def execute_speed(self, server_id: int | None = None) -> SpeedTestResult | None:
        '''
            Runs speed measurement and records statistics.

            :param server_id: Optional server ID.
            :return: Speed test result or None.
            :exceptions: None.
        '''

    def execute_download(self, server_id: int | None = None) -> tuple[float, SpeedTestServer | None]:
        '''
            Runs download measurement and records statistics.

            :param server_id: Optional server ID.
            :return: Tuple of download speed in Mbps and server entity.
            :exceptions: None.
        '''

    def execute_upload(self, server_id: int | None = None) -> tuple[float, SpeedTestServer | None]:
        '''
            Runs upload measurement and records statistics.

            :param server_id: Optional server ID.
            :return: Tuple of upload speed in Mbps and server entity.
            :exceptions: None.
        '''

    def fetch_servers(self) -> list[SpeedTestServer]:
        '''
            Fetches available servers and stores them.

            :return: List of fetched speed test servers.
            :exceptions: None.
        '''

    def get_history(self, limit: int = 50) -> Sequence[SpeedTestStat]:
        '''
            Retrieves measurement statistics from database.

            :param limit: Maximum number of records.
            :return: Sequence of SpeedTestStat entities.
            :exceptions: None.
        '''

    def export_json(self, data: object, file_path: str) -> bool:
        '''
            Exports data object to JSON file.

            :param data: Data object or collection to export.
            :param file_path: Path to target JSON file.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''

    def load_json(self, file_path: str) -> dict[str, object]:
        '''
            Loads configuration dictionary from JSON file.

            :param file_path: Path to JSON file to load.
            :return: Loaded configuration dictionary.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if the service is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
