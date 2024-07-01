# -*- coding: UTF-8 -*-

'''
Module
    connector.py
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
    Defines class Connector with attribute(s) and method(s).
    Provides utility functions for building HTTP and HTTPS connections
    with configurable timeout and optional SSL context.
'''

from typing import Any, List, Callable, Optional, Union, TypeAlias
from ssl import SSLContext
from http.client import HTTPConnection, HTTPSConnection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


ConnectionCall: TypeAlias = Callable[
    ..., Union[HTTPConnection, HTTPSConnection]
]


class Connector:
    '''
        Defines class Connector with attribute(s) and method(s).
        Provides utility functions for building HTTP and HTTPS connections
        with configurable timeout and optional SSL context.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | build_connection - Creates a new connection call function
                |                    with specified timeout and SSL context.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::CONNECTOR'

    @classmethod
    def build_connection(
        cls,
        connection: ConnectionCall,
        timeout: Optional[int] = 10,
        context: Optional[SSLContext] = None
    ) -> ConnectionCall:
        '''
            Creates a new connection call function with the specified timeout
            and SSL context.

            :param connection: A callable that creates a new connection
                               instance (either HTTP or HTTPS)
            :type connection: <ConnectionCall>
            :param timeout: Defines connection timeout (default 10 seconds)
            :type timeout: <Optional[int]>
            :param context: SSL context for HTTPS connections (default is None)
            :type context: <Optional[SSLContext]>
            :return: An instance of HTTPConnection or HTTPSConnection
            :rtype: <ConnectionCall>
            :exceptions: None
        '''
        def inner(
            host: str, **kwargs: Any
        ) -> Union[HTTPConnection, HTTPSConnection]:
            '''
                Creates a connection to the specified host with the configured
                timeout and SSL context.

                :param host: Host to connect
                :type host: <str>
                :param kwargs: Additional parameters to pass to the
                               connection callable
                :type kwargs: <Dict[str, Any]>
                :return: An instance of HTTPConnection or HTTPSConnection
                :rtype: <ConnectionCall>
                :exceptions: None
            '''
            kwargs.update({'timeout': timeout})
            if context:
                kwargs['context'] = context
            return connection(host, **kwargs)
        return inner
