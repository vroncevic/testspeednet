# -*- coding: UTF-8 -*-

'''
Module
    test_https_connection.py
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
    Defines class TestHTTPSConnection with attribute(s) and method(s).
    Extends HTTPSConnection to handle HTTPS requests with a custom
    connection and context.
'''

from socket import create_connection
from ssl import SSLContext, create_default_context
from typing import Any, Dict, List
from http.client import HTTPSConnection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestHTTPSConnection(HTTPSConnection):
    '''
        Defines class TestHTTPSConnection with attribute(s) and method(s).
        Extends HTTPSConnection to handle HTTPS requests with a custom
        connection and context.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | default_port - Default port for HTTPS connections (443).
                | _tunnel_host - Optional hostname for tunneling - proxies.
                | timeout - Maximum allowed time for the HTTPS connection.
                | _context - SSL context for secure connections.
            :methods:
                | __init__ - Initializes an instance of TestHTTPSConnection.
                | connect - Establishes a secure connection to the host.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::TEST_HTTPS_CONNECTION'
    default_port: int = 443

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''
            Initializes an instance of TestHTTPSConnection.

            :param args: Positional arguments passed to HTTPSConnection.
            :type args: <Any>
            :param kwargs: Keyword arguments passed to HTTPSConnection.
            :type kwargs: <Any>
            :exceptions: None
        '''
        HTTPSConnection.__init__(self, *args, **kwargs)
        self._tunnel_host = None
        self.timeout = kwargs.pop('timeout', 10)
        self._context: SSLContext = create_default_context()

    def connect(self) -> None:
        '''
            Establishes a secure connection to the host.

            This method creates a socket connection to the host and port
            specified and wraps it with the SSL context to establish a
            secure connection.

            :exceptions: None
        '''
        self.sock = create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self._tunnel()  # type: ignore
        kwargs: Dict[str, Any] = {}
        kwargs['server_hostname'] = self.host
        self.sock = self._context.wrap_socket(self.sock, **kwargs)
