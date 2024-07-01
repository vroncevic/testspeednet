# -*- coding: UTF-8 -*-

'''
Module
    http_downloader.py
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
    Defines class CatchRequest with attribute(s) and method(s).
    Threaded downloader for making HTTP requests and measuring download speeds.
'''

import sys
from timeit import default_timer
from threading import Thread, Event
from typing import Callable, List, Optional
from urllib.request import OpenerDirector, Request, urlopen
from http.client import HTTPResponse

try:
    from testspeednet.net.utils.fake_shutdown_event import FakeShutdownEvent
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


class HTTPDownloader(Thread):
    '''
        Defines class CatchRequest with attribute(s) and method(s).
        Threaded downloader for making HTTP requests and measuring
        download speeds.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | i - Identifier for the downloader instance.
                | request - The HTTP request object to be opened.
                | result - List that stores the sizes of downloaded chunks
                |          of data during the HTTP download operation.
                | starttime - Start time of the download operation.
                | _opener - A custom opener for request.
                | timeout - Maximum allowed time for the download operation.
                | _shutdown_event - Shutdown event.
            :methods:
                | __init__ - Initializes an instance of HTTPDownloader.
                | run - Executes the HTTP download operation
                |       in a separate thread.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::HTTP_DOWNLOADER'

    def __init__(
        self,
        i: int,
        request: Request,
        start: float,
        timeout: float,
        opener: Optional[OpenerDirector] = None,
        shutdown_event: Optional[Event | FakeShutdownEvent] = None
    ) -> None:
        '''
            Initializes an instance of HTTPDownloader.

            :param i: Identifier for the downloader instance
            :type i: <int>
            :param request: The HTTP request object to be opened
            :type request: <Request>
            :param start: Start time of the download operation
            :type start: <float>
            :param timeout: Maximum allowed time for the download operation
            :type timeout: <float>
            :param opener: A custom opener
            :type opener: <Optional[OpenerDirector]>
            :param shutdown_event: Shutdown event
            :type shutdown_event: <Optional[Event | FakeShutdownEvent]>
            :exceptions: None
        '''
        super().__init__()
        self.request: Request = request
        self.result: List[int] = [0]
        self.starttime: float = start
        self.timeout: float = timeout
        self.i: int = i
        self._shutdown_event: Optional[Event | FakeShutdownEvent]
        if opener:
            self._opener: Callable[[Request], HTTPResponse] = opener.open
        else:
            self._opener: Callable[[Request], HTTPResponse] = urlopen
        if shutdown_event:
            self._shutdown_event = shutdown_event
        else:
            self._shutdown_event = FakeShutdownEvent()

    def run(self) -> None:
        '''
            Executes the HTTP download operation in a separate thread.

            :exceptions: None
        '''
        try:
            if (default_timer() - self.starttime) <= self.timeout:
                response: HTTPResponse = self._opener(self.request)
                if bool(self._shutdown_event):
                    while (
                        not self._shutdown_event.is_set() and
                        (default_timer() - self.starttime)
                        <= self.timeout
                    ):
                        self.result.append(len(response.read(10240)))
                        if self.result[-1] == 0:
                            break
                    response.close()
        except IOError:
            pass
