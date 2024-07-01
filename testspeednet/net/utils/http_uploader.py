# -*- coding: UTF-8 -*-

'''
Module
    http_uploader.py
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
    Defines class HTTPUploader with attribute(s) and method(s).
    Threaded uploader for making HTTP requests and measuring upload speeds.
'''

import sys
from timeit import default_timer
from threading import Thread, Event
from typing import Callable, List
from urllib.request import OpenerDirector, Request, urlopen
from http.client import HTTPResponse

try:
    from testspeednet.net.utils.fake_shutdown_event import FakeShutdownEvent
    from testspeednet.net.utils.net_exceptions import SpeedtestUploadTimeout
    from testspeednet.net.utils.requester import Requester
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


class HTTPUploader(Thread):
    '''
        Defines class HTTPUploader with attribute(s) and method(s).
        Threaded uploader for making HTTP requests and measuring upload speeds.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | i - Identifier for the downloader instance.
                | request - The HTTP request object to be opened.
                | result - List that stores the sizes of downloaded chunks
                |          of data during the HTTP upload operation.
                | starttime - Start time of the upload operation.
                | size - Size of data to be uploaded.
                | _opener - A custom opener for request.
                | timeout - Maximum allowed time for the upload operation.
                | _shutdown_event - Shutdown event.
            :methods:
                | __init__ - Initializes an instance of HTTPUploader.
                | run - Executes the HTTP upload operation
                |       in a separate thread.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::HTTP_UPLOADER'

    def __init__(
        self,
        i: int,
        request: Request,
        start: float,
        size: int,
        timeout: float,
        opener: OpenerDirector | None = None,
        shutdown_event: Event | FakeShutdownEvent | None = None
    ) -> None:
        '''
            Initializes an instance of HTTPUploader.

            :param i: Identifier for the downloader instance
            :type i: <int>
            :param request: The HTTP request object to be opened
            :type request: <Request>
            :param start: Start time of the upload operation
            :type start: <float>
            :param size: Size of data to be uploaded
            :type size: <int>
            :param timeout: Maximum allowed time for the upload operation
            :type timeout: <float>
            :param opener: A custom opener
            :type opener: <Optional[OpenerDirector]>
            :param shutdown_event: Shutdown event
            :type shutdown_event: <Optional[Event | FakeShutdownEvent]>
            :exceptions: None
        '''
        super().__init__()
        self.request: Request = request
        self.request.data.start = self.starttime = start  # type: ignore
        self.size: int = size
        self.result: int = 0
        self.timeout: float = timeout
        self.i: int = i
        if opener:
            self._opener: Callable[[Request], HTTPResponse] = opener.open
        else:
            self._opener: Callable[[Request], HTTPResponse] = urlopen
        self._shutdown_event: Event | FakeShutdownEvent | None
        if shutdown_event:
            self._shutdown_event = shutdown_event
        else:
            self._shutdown_event = FakeShutdownEvent()

    def run(self) -> None:
        '''
            Executes the HTTP upload operation in a separate thread.

            :exceptions: None
        '''
        request: Request = self.request
        if self._shutdown_event is None:
            raise ValueError('shutdown_event not set')
        if request.data is None:
            raise ValueError('request.data not set')
        try:
            if ((default_timer() - self.starttime) <= self.timeout and
                    not self._shutdown_event.is_set()):
                try:
                    f = self._opener(request)
                except TypeError:
                    request = Requester.build_request(
                        url=self.request.get_full_url(),
                        data=request.data.read(self.size)  # type: ignore
                    )
                    f: HTTPResponse = self._opener(request)
                f.read(11)
                f.close()
                self.result = sum(self.request.data.total)  # type: ignore
            else:
                self.result = 0
        except (IOError, SpeedtestUploadTimeout):
            self.result = sum(self.request.data.total)  # type: ignore
