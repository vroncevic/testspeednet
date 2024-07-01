# -*- coding: UTF-8 -*-

'''
Module
    test.py
Copyright
    Copyright (C) 2016 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    Defines class TestNet with attribute(s) and method(s).
'''

import sys
from timeit import default_timer
from os.path import dirname
from threading import Thread
from time import sleep
from queue import Queue
from urllib.request import OpenerDirector, Request
from typing import Any, Callable, Dict, List, Tuple, Optional

try:
    from testspeednet.net.utils.fake_shutdown_event import FakeShutdownEvent
    from testspeednet.net.utils.http_downloader import HTTPDownloader
    from testspeednet.net.utils.http_uploader import HTTPUploader
    from testspeednet.net.utils.http_uploader_data import HTTPUploaderData
    from testspeednet.net.utils.test_results import TestResults
    from testspeednet.net.utils.do_nothing import do_nothing
    from testspeednet.net.utils.requester import Requester
    from testspeednet.net.utils.opener import Opener
    from testspeednet.net.utils.test_net_config import TestNetConfig
    from testspeednet.net.utils.checking_servers import NeighbourServer
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

thread_is_alive: Callable[..., bool] = Thread.is_alive


class TestNet:
    '''
        Defines class TestNet with attribute(s) and method(s).

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | config - Configuration dictionary.
                | server_check - Instance for checking servers.
                | _opener - A custom opener for request.
                | _secure - Flag indicating secure connection.
                | _best - Best server details.
                | _shutdown_event - Fake event for shutdown control.
            :methods:
                | __init__ - Initializes an instance of TestNet.
                | best - Returns the best server based on latency.
                | download - Initiates download tests using multiple threads.
                | upload - Initiates upload tests using multiple threads.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::TEST_NET'

    def __init__(self, timeout: int = 10, secure: bool = False) -> None:
        '''
            Initializes an instance of TestNet.

            :param timeout: Maximum allowed time for the operation
            :type timeout: <int>
            :param secure: Flag indicating secure connection
            :type secure: <bool>
            :exceptions: None
        '''
        self.config: Dict[str, Any] = {}
        self._opener: OpenerDirector = Opener.build_opener(timeout)
        self._secure: bool = secure
        self._shutdown_event: FakeShutdownEvent = FakeShutdownEvent()
        config: Optional[Dict[str, Any]] = TestNetConfig.get_config(
            secure, self._opener
        )
        if bool(config):
            self.config.update(config['config'])
        self._best: Dict[str, Any] | None = None
        self.results = TestResults(
            client=self.config['client'], opener=self._opener, secure=secure
        )
        self.server_check: NeighbourServer = NeighbourServer(
            self.config, self._secure, self._opener
        )

    @property
    def best(self) -> Optional[Dict[str, Any]]:
        '''
            Returns the best server based on latency.

            :return: Details of the best server found
            :rtype: <Optional[Dict[str, Any]]>
            :exceptions: None
        '''
        if not self._best:
            self._best = self.server_check.get_best_server()
            if not self._best:
                return None
            self.results.ping = int(self._best['latency'])
            self.results.server = self._best
        return self._best

    def download(self, callback: Callable[..., Any] = do_nothing,) -> int:
        '''
            Initiates download tests using multiple threads.

            :param callback: Optional callback function for progress updates
            :type callback: <Callable[..., Any]>
            :return: Download speed in Mbps
            :rtype: <int>
            :exceptions: None
        '''
        if not self.best:
            return -1
        best_server: str = self.best['url']
        urls: List[str] = []
        for size in self.config['sizes']['download']:
            for _ in range(0, self.config['counts']['download']):
                best_url: str = dirname(best_server)
                urls.append(f'{best_url}/random{size}x{size}.jpg')
        request_count: int = len(urls)
        requests: List[Request] = []
        for i, url in enumerate(urls):
            requests.append(
                Requester.build_request(url, bump=str(i), secure=self._secure)
            )
        max_threads: int = self.config['threads']['download']
        in_flight: Dict[str, int] = {'threads': 0}

        def producer(
            q: Queue[HTTPDownloader],
            requests: List[Request],
            request_count: int
        ) -> None:
            for i, request in enumerate(requests):
                thread = HTTPDownloader(
                    i,
                    request,
                    start,
                    self.config['length']['download'],
                    opener=self._opener,
                    shutdown_event=self._shutdown_event
                )
                while in_flight['threads'] >= max_threads:
                    sleep(0.001)
                thread.start()
                q.put(thread, True)
                in_flight['threads'] += 1
                callback(i, request_count, start=True)
        finished: List[int] = []

        def consumer(q: Queue[HTTPDownloader], request_count: int) -> None:
            _is_alive: Callable[..., bool] = thread_is_alive
            while len(finished) < request_count:
                thread: HTTPDownloader = q.get(True)
                while _is_alive(thread):
                    thread.join(timeout=0.001)
                in_flight['threads'] -= 1
                finished.append(sum(thread.result))
                callback(thread.i, request_count, end=True)
        q: Queue[HTTPDownloader] = Queue(max_threads)
        prod_thread = Thread(
            target=producer, args=(q, requests, request_count)
        )
        cons_thread = Thread(target=consumer, args=(q, request_count))
        start: float = default_timer()
        prod_thread.start()
        cons_thread.start()
        _is_alive: Callable[..., bool] = thread_is_alive
        while _is_alive(prod_thread):
            prod_thread.join(timeout=0.001)
        while _is_alive(cons_thread):
            cons_thread.join(timeout=0.001)
        stop: float = default_timer()
        self.results.bytes_received = sum(finished)
        self.results.download = int(
            (self.results.bytes_received / (stop - start)) * 8.0
        )
        if self.results.download > 100000:
            self.config['threads']['upload'] = 8
        return self.results.download

    def upload(
        self,
        callback: Callable[..., Any] = do_nothing,
        pre_allocate: bool = True,
    ) -> int:
        '''
            Initiates upload tests using multiple threads.

            :param callback: Optional callback function for progress updates
            :type callback: <Callable[..., Any]>
            :return: Upload speed in Mbps.
            :rtype: <int>
            :exceptions: None
        '''
        if not self.best:
            return -1
        best_server: str = self.best['url']
        sizes: List[int] = []
        for size in self.config['sizes']['upload']:
            for _ in range(0, self.config['counts']['upload']):
                sizes.append(size)
        request_count: int = self.config['upload_max']
        requests: List[Tuple[Request, int]] = []
        for size in sizes:
            data = HTTPUploaderData(
                size,
                0,
                self.config['length']['upload'],
                shutdown_event=self._shutdown_event
            )
            if pre_allocate:
                data.pre_allocate()
            headers: Dict[str, Any] = {'Content-length': size}
            requests.append((
                Requester.build_request(
                    best_server, data, secure=self._secure, headers=headers
                ),
                size
            ))
        max_threads: int = self.config['threads']['upload']
        in_flight: Dict[str, int] = {'threads': 0}

        def producer(
            q: Queue[HTTPUploader],
            requests: List[Tuple[Request, int]],
            request_count: int
        ) -> None:
            for i, request in enumerate(requests[:request_count]):
                thread = HTTPUploader(
                    i,
                    request[0],
                    start,
                    request[1],
                    self.config['length']['upload'],
                    opener=self._opener,
                    shutdown_event=self._shutdown_event
                )
                while in_flight['threads'] >= max_threads:
                    sleep(0.001)
                thread.start()
                q.put(thread, True)
                in_flight['threads'] += 1
                callback(i, request_count, start=True)
        finished: List[int] = []

        def consumer(q: Queue[HTTPUploader], request_count: int) -> None:
            _is_alive: Callable[..., bool] = thread_is_alive
            while len(finished) < request_count:
                thread: HTTPUploader = q.get(True)
                while _is_alive(thread):
                    thread.join(timeout=0.001)
                in_flight['threads'] -= 1
                finished.append(thread.result)
                callback(thread.i, request_count, end=True)
        q: Queue[HTTPUploader] = Queue(self.config['threads']['upload'])
        prod_thread = Thread(
            target=producer, args=(q, requests, request_count)
        )
        cons_thread = Thread(target=consumer, args=(q, request_count))
        start: float = default_timer()
        prod_thread.start()
        cons_thread.start()
        _is_alive: Callable[..., bool] = thread_is_alive
        while _is_alive(prod_thread):
            prod_thread.join(timeout=0.1)
        while _is_alive(cons_thread):
            cons_thread.join(timeout=0.1)
        stop: float = default_timer()
        self.results.bytes_sent = sum(finished)
        self.results.upload = int(
            (self.results.bytes_sent / (stop - start)) * 8.0
        )
        return self.results.upload
