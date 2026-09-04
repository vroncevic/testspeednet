# -*- coding: UTF-8 -*-

'''
Module
    iserver_repository.py
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
    Defines abstract interface IServerRepository for database persistence.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

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
class IServerRepository(Protocol):
    '''
        Defines abstract interface IServerRepository for database persistence.

        It defines:

            :methods:
                | save_servers - Saves speed test servers to database.
                | get_servers - Retrieves speed test servers from database.
                | save_statistic - Saves a measurement statistic record to database.
                | get_statistics - Retrieves measurement history from database.
                | is_initialized - Checks if the repository is initialized.
    '''

    def save_servers(self, *, servers: Sequence[SpeedTestServer]) -> bool:
        '''
            Saves speed test servers to database.

            :param servers: Sequence of SpeedTestServer entities.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''

    def get_servers(self) -> Sequence[SpeedTestServer]:
        '''
            Retrieves speed test servers from database.

            :return: Sequence of SpeedTestServer entities.
            :exceptions: None.
        '''

    def save_statistic(self, *, stat: SpeedTestStat) -> bool:
        '''
            Saves a measurement statistic record to database.

            :param stat: SpeedTestStat entity to save.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''

    def get_statistics(self, *, limit: int = 50) -> Sequence[SpeedTestStat]:
        '''
            Retrieves measurement history from database.

            :param limit: Maximum number of records to retrieve.
            :return: Sequence of SpeedTestStat entities.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if the repository is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
