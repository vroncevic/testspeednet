# -*- coding: UTF-8 -*-

'''
Module
    server_repository.py
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
    Defines ServerRepository for SQLite database persistence.
'''

from __future__ import annotations

from collections.abc import Sequence
import sqlite3
from typing import override

from ats_utilities.utils.reflection import to_str

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.model.speed_test_stat import SpeedTestStat
from testspeednet.core.service.iserver_repository import IServerRepository

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class ServerRepository(IServerRepository):
    '''
        Adapter implementing SQLite database repository for speed test data.

        It defines:

            :attributes:
                | _db_path - Path to SQLite database file.
                | _is_initialized - Status flag indicating if repository is initialized.
            :methods:
                | __init__ - Initializes ServerRepository and creates tables if needed.
                | save_servers - Saves speed test servers to database.
                | get_servers - Retrieves speed test servers from database.
                | save_statistic - Saves a measurement statistic record to database.
                | get_statistics - Retrieves measurement history from database.
                | is_initialized - Checks if the repository is initialized.
                | __str__ - Returns string representation of ServerRepository.
    '''

    _db_path: str
    _is_initialized: bool

    def __init__(self, db_path: str = 'testspeednet_servers.db') -> None:
        '''
            Initializes ServerRepository and creates tables if needed.

            :param db_path: Path to the SQLite database file.
            :exceptions: None.
        '''
        self._db_path = db_path
        self._is_initialized = False

        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS speedtest_servers (
                        id INTEGER PRIMARY KEY,
                        server_id TEXT NOT NULL,
                        url TEXT NOT NULL,
                        lat REAL NOT NULL,
                        lon REAL NOT NULL,
                        distance REAL NOT NULL,
                        name TEXT NOT NULL,
                        country TEXT NOT NULL,
                        cc TEXT NOT NULL,
                        sponsor TEXT NOT NULL,
                        preferred INTEGER NOT NULL,
                        host TEXT NOT NULL
                    )
                    '''
                )
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS speedtest_statistics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        operation TEXT NOT NULL,
                        download_speed REAL NOT NULL,
                        upload_speed REAL NOT NULL,
                        latency REAL,
                        server_name TEXT,
                        server_host TEXT
                    )
                    '''
                )
                conn.commit()
            self._is_initialized = True

        except sqlite3.Error:
            self._is_initialized = False

    @override
    def save_servers(self, *, servers: Sequence[SpeedTestServer]) -> bool:
        '''
            Saves speed test servers to database.

            :param servers: Sequence of SpeedTestServer entities.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''
        if not self._is_initialized:
            return False

        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM speedtest_servers')
                cursor.executemany(
                    '''
                    INSERT INTO speedtest_servers (
                        id, server_id, url, lat, lon, distance,
                        name, country, cc, sponsor, preferred, host
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    [
                        (
                            server.id,
                            server.server_id,
                            server.url,
                            server.lat,
                            server.lon,
                            server.distance,
                            server.name,
                            server.country,
                            server.cc,
                            server.sponsor,
                            1 if server.preferred else 0,
                            server.host
                        )
                        for server in servers
                    ]
                )
                conn.commit()
            return True

        except sqlite3.Error:
            return False

    @override
    def get_servers(self) -> Sequence[SpeedTestServer]:
        '''
            Retrieves speed test servers from database.

            :return: Sequence of SpeedTestServer entities.
            :exceptions: None.
        '''
        if not self._is_initialized:
            return []

        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    SELECT id, server_id, url, lat, lon, distance,
                           name, country, cc, sponsor, preferred, host
                    FROM speedtest_servers
                    ORDER BY id ASC
                    '''
                )
                rows = cursor.fetchall()
                return [
                    SpeedTestServer(
                        id=row[0],
                        server_id=row[1],
                        url=row[2],
                        lat=float(row[3]),
                        lon=float(row[4]),
                        distance=float(row[5]),
                        name=row[6],
                        country=row[7],
                        cc=row[8],
                        sponsor=row[9],
                        preferred=bool(row[10]),
                        host=row[11]
                    )
                    for row in rows
                ]

        except sqlite3.Error:
            return []

    @override
    def save_statistic(self, *, stat: SpeedTestStat) -> bool:
        '''
            Saves a measurement statistic record to database.

            :param stat: SpeedTestStat entity to save.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''
        if not self._is_initialized:
            return False

        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT INTO speedtest_statistics (
                        timestamp, operation, download_speed, upload_speed,
                        latency, server_name, server_host
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        stat.timestamp,
                        stat.operation,
                        stat.download_speed,
                        stat.upload_speed,
                        stat.latency,
                        stat.server_name,
                        stat.server_host
                    )
                )
                conn.commit()
            return True

        except sqlite3.Error:
            return False

    @override
    def get_statistics(self, *, limit: int = 50) -> Sequence[SpeedTestStat]:
        '''
            Retrieves measurement history from database.

            :param limit: Maximum number of records to retrieve.
            :return: Sequence of SpeedTestStat entities.
            :exceptions: None.
        '''
        if not self._is_initialized:
            return []

        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    SELECT id, timestamp, operation, download_speed,
                           upload_speed, latency, server_name, server_host
                    FROM speedtest_statistics
                    ORDER BY id DESC
                    LIMIT ?
                    ''',
                    (limit,)
                )
                rows = cursor.fetchall()
                return [
                    SpeedTestStat(
                        id=row[0],
                        timestamp=row[1],
                        operation=row[2],
                        download_speed=float(row[3]),
                        upload_speed=float(row[4]),
                        latency=float(row[5]) if row[5] is not None else None,
                        server_name=row[6],
                        server_host=row[7]
                    )
                    for row in rows
                ]

        except sqlite3.Error:
            return []

    @override
    def is_initialized(self) -> bool:
        '''
            Checks if the repository is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return self._is_initialized

    def __str__(self) -> str:
        '''
            Returns string representation of ServerRepository.

            :return: String representation of ServerRepository.
            :exceptions: None.
        '''
        return to_str(self)
