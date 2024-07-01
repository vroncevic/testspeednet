# -*- coding: UTF-8 -*-

'''
Module
    test_http_connection.py
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
    Defines class TestHTTPConnection with attribute(s) and method(s).
    Extends HTTPConnection to allow setting a custom timeout for the
    HTTP connection.
'''

import socket
from typing import Any, List
from http.client import HTTPConnection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestHTTPConnection(HTTPConnection):
    '''
        Defines class TestHTTPConnection with attribute(s) and method(s).
        Extends HTTPConnection to allow setting a custom timeout for the
        HTTP connection.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | timeout - Maximum allowed time for the HTTP connection.
            :methods:
                | __init__ - Initializes an instance of TestHTTPConnection.
                | connect - Establishes the HTTP connection with
                |           the specified timeout.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::TEST_HTTP_CONNECTION'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''
            Initializes an instance of TestHTTPConnection.

            :param args: Arguments to be passed to the parent
                         HTTPConnection class
            :type args: <Any>
            :param kwargs: Keyword arguments to be passed to
                           the parent HTTPConnection class
            :type kwargs: <Any>
            :exceptions: None
        '''
        HTTPConnection.__init__(self, *args, **kwargs)
        self.timeout = kwargs.pop('timeout', 10)

    def connect(self) -> None:
        '''
            Establishes the HTTP connection with the specified timeout.

            :exceptions: None
        '''
        self.sock = socket.create_connection(
            (self.host, self.port), self.timeout
        )
