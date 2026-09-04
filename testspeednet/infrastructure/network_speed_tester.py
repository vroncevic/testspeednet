# -*- coding: UTF-8 -*-

'''
Module
    network_speed_tester.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    testspeednet is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    testspeednet is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Network speed tester adapter implementing INetworkSpeedTester.
'''

from __future__ import annotations

import time
from urllib.error import URLError
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

from ats_utilities.config_io.processor.json_processor import JSONProcessor
from ats_utilities.utils.reflection import to_str

from testspeednet.core.model.speed_test_server import SpeedTestServer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '2.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NetworkSpeedTester:
    '''
        Adapter that executes low-level network speed measurements and server queries.

        It defines:

            :methods:
                | __init__ - Initializes the network speed tester adapter.
                | measure_ping - Measures ping latency to target server.
                | measure_download - Measures download speed from target server.
                | measure_upload - Measures upload speed to target server.
                | fetch_servers - Fetches servers from remote API.
                | is_initialized - Checks if the tester is initialized.
                | __str__ - Returns the NetworkSpeedTester as string representation.
    '''

    _DEFAULT_USER_AGENT: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    _SEARCH_COUNTRIES: tuple[str, ...] = ('Serbia', 'Germany', 'United Kingdom', 'United States')

    def __init__(self) -> None:
        '''
            Initializes the NetworkSpeedTester adapter.

            :exceptions: None.
        '''

    def measure_ping(self, server: SpeedTestServer) -> float:
        '''
            Measures latency to target server.

            :param server: Speed test server.
            :return: Latency in milliseconds.
            :exceptions: None.
        '''
        latency_url: str = urljoin(server.url, 'latency.txt')
        req = Request(latency_url, headers={'User-Agent': self._DEFAULT_USER_AGENT})
        samples: list[float] = []

        for _ in range(3):
            try:
                start = time.perf_counter()
                with urlopen(req, timeout=3) as resp:
                    resp.read()
                samples.append((time.perf_counter() - start) * 1000.0)
            except (URLError, TimeoutError, OSError):
                continue

        return round(min(samples), 2) if samples else 0.0

    def measure_download(self, server: SpeedTestServer) -> float:
        '''
            Measures download speed from target server.

            :param server: Speed test server.
            :return: Download speed in Mbps.
            :exceptions: None.
        '''
        download_url: str = urljoin(server.url, 'random1000x1000.jpg')
        req = Request(download_url, headers={'User-Agent': self._DEFAULT_USER_AGENT})
        total_bytes: int = 0
        total_duration: float = 0.0

        for _ in range(3):
            try:
                start = time.perf_counter()
                with urlopen(req, timeout=10) as resp:
                    data = resp.read()
                duration = time.perf_counter() - start
                if duration > 0:
                    total_bytes += len(data)
                    total_duration += duration
            except (URLError, TimeoutError, OSError):
                break

        if total_duration <= 0 or total_bytes == 0:
            return 0.0

        speed_mbps: float = (total_bytes * 8.0) / (total_duration * 1_000_000.0)
        return round(speed_mbps, 2)

    def measure_upload(self, server: SpeedTestServer) -> float:
        '''
            Measures upload speed to target server.

            :param server: Speed test server.
            :return: Upload speed in Mbps.
            :exceptions: None.
        '''
        upload_url: str = server.url
        chunk_size: int = 250 * 1024
        payload: bytes = b'0' * chunk_size
        req = Request(
            upload_url,
            data=payload,
            headers={'User-Agent': self._DEFAULT_USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        total_bytes: int = 0
        total_duration: float = 0.0

        for _ in range(3):
            try:
                start = time.perf_counter()
                with urlopen(req, timeout=10) as resp:
                    resp.read()
                duration = time.perf_counter() - start
                if duration > 0:
                    total_bytes += chunk_size
                    total_duration += duration
            except (URLError, TimeoutError, OSError):
                break

        if total_duration <= 0 or total_bytes == 0:
            return 0.0

        speed_mbps: float = (total_bytes * 8.0) / (total_duration * 1_000_000.0)
        return round(speed_mbps, 2)

    def fetch_servers(self) -> list[SpeedTestServer]:
        '''
            Fetches servers from remote API using JSONProcessor.

            :return: List of fetched servers.
            :exceptions: None.
        '''
        collected_servers: list[SpeedTestServer] = []
        idx: int = 1

        for country in self._SEARCH_COUNTRIES:
            url = f'https://www.speedtest.net/api/js/servers?engine=js&search={quote(country)}'
            req = Request(url, headers={'User-Agent': self._DEFAULT_USER_AGENT})
            try:
                with urlopen(req, timeout=5) as resp:
                    raw_content: str = resp.read().decode('utf-8', errors='ignore')
                processor: JSONProcessor = JSONProcessor()
                if processor.deserialize(raw_content):
                    data = processor.to_dict()
                    if isinstance(data, list):
                        for item in data:
                            server = SpeedTestServer(
                                id=idx,
                                server_id=str(item.get('id', '')),
                                url=str(item.get('url', '')),
                                lat=float(item.get('lat', 0.0)),
                                lon=float(item.get('lon', 0.0)),
                                distance=float(item.get('distance', 0.0)),
                                name=str(item.get('name', '')),
                                country=str(item.get('country', '')),
                                cc=str(item.get('cc', '')),
                                sponsor=str(item.get('sponsor', '')),
                                preferred=bool(item.get('preferred', 0)),
                                host=str(item.get('host', ''))
                            )
                            collected_servers.append(server)
                            idx += 1
            except (URLError, TimeoutError, OSError, ValueError, KeyError):
                continue

        return collected_servers

    def is_initialized(self) -> bool:
        '''
            Checks if the tester is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return True

    def __str__(self) -> str:
        '''
            Returns the NetworkSpeedTester as string representation.

            :return: The NetworkSpeedTester as string representation.
            :exceptions: None.
        '''
        return to_str(self)
