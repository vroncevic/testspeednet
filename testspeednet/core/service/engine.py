# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Defines application service for speed test operations.
'''

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime

from ats_utilities.utils.reflection import to_str
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from testspeednet.core.model.speed_test_result import SpeedTestResult
from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.model.speed_test_stat import SpeedTestStat
from testspeednet.core.service.ijson_exporter import IJsonExporter
from testspeednet.core.service.iserver_repository import IServerRepository
from testspeednet.core.service.isubprocessor import ISubProcessor

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class Service:
    '''
        Service for orchestrating speed test operations.

        It defines:

            :attributes:
                | _subprocessor - Adapter for executing measurement sub-processes.
                | _server_repository - Adapter for database persistence.
                | _json_exporter - Adapter for JSON data export and loading.
            :methods:
                | __init__ - Initializes the service with adapters.
                | execute_speed - Runs speed measurement and records statistics.
                | execute_download - Runs download measurement and records statistics.
                | execute_upload - Runs upload measurement and records statistics.
                | fetch_servers - Fetches available servers and stores them.
                | get_history - Retrieves measurement statistics from database.
                | export_json - Exports data object to JSON file.
                | load_json - Loads configuration dictionary from JSON file.
                | is_initialized - Checks if the service is initialized.
                | __str__ - Returns string representation of Service.
    '''

    _subprocessor: ISubProcessor[Mapping[str, object], Mapping[str, object]]
    _server_repository: IServerRepository
    _json_exporter: IJsonExporter

    def __init__(
        self,
        subprocessor: ISubProcessor[Mapping[str, object], Mapping[str, object]],
        server_repository: IServerRepository,
        json_exporter: IJsonExporter
    ) -> None:
        '''
            Initializes the service with adapters.

            :param subprocessor: The subprocessor adapter.
            :param server_repository: The server repository adapter.
            :param json_exporter: The JSON exporter adapter.
            :exceptions:
                | ATSValueError: Adapters must be provided.
                | ATSTypeError:  Adapters must implement their respective interfaces.
        '''
        ctx: str = 'service::init(...)'
        not_none(subprocessor, ctx, 'the subprocessor must be provided')
        istype(subprocessor, ISubProcessor, ctx, 'the subprocessor must implement ISubProcessor')
        not_none(server_repository, ctx, 'the server repository must be provided')
        istype(server_repository, IServerRepository, ctx, 'the server repository must implement IServerRepository')
        not_none(json_exporter, ctx, 'the json exporter must be provided')
        istype(json_exporter, IJsonExporter, ctx, 'the json exporter must implement IJsonExporter')

        self._subprocessor = subprocessor
        self._server_repository = server_repository
        self._json_exporter = json_exporter

    def _resolve_server(self, server_id: int | None = None) -> SpeedTestServer | None:
        '''
            Resolves target server from repository or fetches new ones.

            :param server_id: Optional ID of the specific server.
            :return: Speed test server or None.
            :exceptions: None.
        '''
        servers: Sequence[SpeedTestServer] = self._server_repository.get_servers()
        if server_id is not None:
            for s in servers:
                if s.id == server_id or s.server_id == str(server_id):
                    return s

        if servers:
            return servers[0]

        fetched: list[SpeedTestServer] = self.fetch_servers()
        return fetched[0] if fetched else None

    def execute_speed(self, server_id: int | None = None) -> SpeedTestResult | None:
        '''
            Runs speed measurement and records statistics.

            :param server_id: Optional server ID.
            :return: Speed test result or None.
            :exceptions: None.
        '''
        server: SpeedTestServer | None = self._resolve_server(server_id)
        if server is None:
            return None

        data = self._subprocessor.run(params={'cmd': 'speed', 'server': server})
        ping_val: float = float(data.get('ping', 0.0))
        download_val: float = float(data.get('download', 0.0))
        upload_val: float = float(data.get('upload', 0.0))

        now_ts: str = datetime.now().isoformat()
        stat: SpeedTestStat = SpeedTestStat(
            id=None,
            timestamp=now_ts,
            operation='speed',
            download_speed=download_val,
            upload_speed=upload_val,
            latency=ping_val,
            server_name=server.name,
            server_host=server.host
        )
        self._server_repository.save_statistic(stat=stat)

        return SpeedTestResult(
            download_speed=download_val,
            upload_speed=upload_val,
            latency=ping_val,
            server_name=server.name,
            server_host=server.host,
            timestamp=now_ts
        )

    def execute_download(self, server_id: int | None = None) -> tuple[float, SpeedTestServer | None]:
        '''
            Runs download measurement and records statistics.

            :param server_id: Optional server ID.
            :return: Tuple of download speed in Mbps and server entity.
            :exceptions: None.
        '''
        server: SpeedTestServer | None = self._resolve_server(server_id)
        if server is None:
            return 0.0, None

        data = self._subprocessor.run(params={'cmd': 'download', 'server': server})
        download_val: float = float(data.get('download', 0.0))

        stat: SpeedTestStat = SpeedTestStat(
            id=None,
            timestamp=datetime.now().isoformat(),
            operation='download',
            download_speed=download_val,
            upload_speed=0.0,
            latency=None,
            server_name=server.name,
            server_host=server.host
        )
        self._server_repository.save_statistic(stat=stat)

        return download_val, server

    def execute_upload(self, server_id: int | None = None) -> tuple[float, SpeedTestServer | None]:
        '''
            Runs upload measurement and records statistics.

            :param server_id: Optional server ID.
            :return: Tuple of upload speed in Mbps and server entity.
            :exceptions: None.
        '''
        server: SpeedTestServer | None = self._resolve_server(server_id)
        if server is None:
            return 0.0, None

        data = self._subprocessor.run(params={'cmd': 'upload', 'server': server})
        upload_val: float = float(data.get('upload', 0.0))

        stat: SpeedTestStat = SpeedTestStat(
            id=None,
            timestamp=datetime.now().isoformat(),
            operation='upload',
            download_speed=0.0,
            upload_speed=upload_val,
            latency=None,
            server_name=server.name,
            server_host=server.host
        )
        self._server_repository.save_statistic(stat=stat)

        return upload_val, server

    def fetch_servers(self) -> list[SpeedTestServer]:
        '''
            Fetches available servers and stores them.

            :return: List of fetched speed test servers.
            :exceptions: None.
        '''
        data = self._subprocessor.run(params={'cmd': 'fetch'})
        servers_obj = data.get('servers', [])
        servers: list[SpeedTestServer] = servers_obj if isinstance(servers_obj, list) else []

        if servers:
            self._server_repository.save_servers(servers=servers)

        return servers

    def get_history(self, limit: int = 50) -> Sequence[SpeedTestStat]:
        '''
            Retrieves measurement statistics from database.

            :param limit: Maximum number of records.
            :return: Sequence of SpeedTestStat entities.
            :exceptions: None.
        '''
        return self._server_repository.get_statistics(limit=limit)

    def export_json(self, data: object, file_path: str) -> bool:
        '''
            Exports data object to JSON file.

            :param data: Data object or collection to export.
            :param file_path: Path to target JSON file.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''
        return self._json_exporter.export_json(data=data, file_path=file_path)

    def load_json(self, file_path: str) -> dict[str, object]:
        '''
            Loads configuration dictionary from JSON file.

            :param file_path: Path to JSON file to load.
            :return: Loaded configuration dictionary.
            :exceptions: None.
        '''
        return self._json_exporter.load_json(file_path=file_path)

    def is_initialized(self) -> bool:
        '''
            Checks if the service is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return (
            self._subprocessor.is_initialized()
            and self._server_repository.is_initialized()
            and self._json_exporter.is_initialized()
        )

    def __str__(self) -> str:
        '''
            Returns the Service as string representation.

            :return: The Service as string representation.
            :exceptions: None.
        '''
        return to_str(self)
