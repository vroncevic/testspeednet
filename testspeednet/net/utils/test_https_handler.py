# -*- coding: UTF-8 -*-

'''
Module
    test_https_handler.py
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
    Defines class TestHTTPSHandler with attribute(s) and method(s).
    Extends AbstractHTTPHandler to handle HTTPS requests with a
    custom connection.
'''

import sys
from typing import Callable, Optional, List
from ssl import SSLContext
from http.client import HTTPResponse
from urllib.request import AbstractHTTPHandler, Request

try:
    from testspeednet.net.utils.test_https_connection import (
        TestHTTPSConnection
    )
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


class TestHTTPSHandler(AbstractHTTPHandler):
    '''
        Defines class TestHTTPSHandler with attribute(s) and method(s).
        Extends AbstractHTTPHandler to handle HTTPS requests with a
        custom connection.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | https_request - Callable for processing HTTPS requests.
                | _context - The HTTP request object to be opened.
                | timeout - Maximum allowed time for the download operation.
            :methods:
                | __init__ - Initializes an instance of TestHTTPSHandler.
                | https_open - Opens the HTTPS connection for a request.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::TEST_HTTPS_HANDLER'

    def __init__(
        self,
        debuglevel: Optional[int] = 0,
        context: Optional[SSLContext] = None,
        timeout: Optional[int] = 10
    ) -> None:
        '''
            Initializes an instance of TestHTTPSHandler.

            :param debuglevel: Debugging level for HTTP transactions,
                               defaults to 0.
            :type debuglevel: <Optional[int]>
            :param context: SSL context for secure connections,
                            defaults to None.
            :type context: <Optional[SSLContext]>
            :param timeout: Timeout for the HTTPS operation,
                            defaults to 10 seconds.
            :type timeout: <Optional[int]>
            :exceptions: None
        '''
        AbstractHTTPHandler.__init__(self, debuglevel)
        self._context: Optional[SSLContext] = context
        self.timeout: Optional[int] = timeout

    def https_open(self, req: Request) -> HTTPResponse:
        '''
            Opens the HTTPS connection for a given request.

            This method establishes a connection to the specified URL
            using HTTPS, handling the SSL context and timeout settings.

            :param req: The HTTP request object to be opened.
            :type req: <Request>
            :return: The HTTP response object for the opened request.
            :rtype: <HTTPResponse>
            :exceptions: None
        '''
        return self.do_open(
            Connector.build_connection(
                TestHTTPSConnection, self.timeout, self._context,
            ),
            req
        )

    https_request: Callable[..., Request] = AbstractHTTPHandler.do_request_
