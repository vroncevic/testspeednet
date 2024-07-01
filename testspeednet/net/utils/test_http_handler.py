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
    Defines class TestHTTPHandler with attribute(s) and method(s).
    Extends AbstractHTTPHandler to handle HTTP requests with a custom
    connection and timeout.
'''

import sys
from http.client import HTTPResponse
from urllib.request import AbstractHTTPHandler, Request
from typing import Optional, Callable, List

try:
    from testspeednet.net.utils.test_http_connection import TestHTTPConnection
    from testspeednet.net.utils.connector import Connector
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


class TestHTTPHandler(AbstractHTTPHandler):
    '''
        Defines class TestHTTPHandler with attribute(s) and method(s).
        Extends AbstractHTTPHandler to handle HTTP requests with a custom
        connection and timeout.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | http_request - Callable for handling HTTP requests.
                | timeout - Maximum allowed time for the HTTP connection.
            :methods:
                | __init__ - Initializes an instance of TestHTTPHandler.
                | http_open - Opens the HTTP connection using a custom
                |             connection class.
    '''

    def __init__(
        self, debuglevel: Optional[int] = 0, timeout: Optional[int] = 10
    ) -> None:
        '''
            Initializes an instance of TestHTTPHandler.

            :param debuglevel: Debug level for the HTTP handler.
            :type debuglevel: <Optional[int]>
            :param timeout: Maximum allowed time for the HTTP connection.
            :type timeout: <Optional[int]>
            :exceptions: None
        '''
        AbstractHTTPHandler.__init__(self, debuglevel)
        self.timeout: Optional[int] = timeout

    def http_open(self, req: Request) -> HTTPResponse:
        '''
            Opens the HTTP connection using a custom connection class.

            This method handles the opening of HTTP connections using the
            TestHTTPConnection class and specified timeout.

            :param req: The request object to be sent.
            :type req: <Request>
            :return: The HTTP response object.
            :rtype: <HTTPResponse>
            :exceptions: None
        '''
        return self.do_open(
            Connector.build_connection(
                TestHTTPConnection, self.timeout, None
            ), req
        )

    http_request: Callable[..., Request] = AbstractHTTPHandler.do_request_
