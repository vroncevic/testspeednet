# -*- coding: UTF-8 -*-

'''
Module
    requester.py
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
    Defines class Requester with attribute(s) and method(s).
    Builds HTTP or HTTPS requests with custom parameters including URL,
    data, headers, and security options.
'''

import time
from urllib.request import Request
from typing import Any, Dict, List, Optional

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Requester:
    '''
        Defines class Requester with attribute(s) and method(s).
        Builds HTTP or HTTPS requests with custom parameters including URL,
        data, headers, and security options.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | build_request - Creates and returns a Request object
                |                 with custom parameters.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::REQUESTER'

    @classmethod
    def build_request(
        cls,
        url: str,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        bump: str = '0',
        secure: bool = False
    ) -> Request:
        '''
            Creates and returns a Request object with custom parameters.

            This method constructs a URL with an optional scheme (HTTP/HTTPS),
            appends a timestamp and a bump parameter for cache control, and
            sets the provided headers or adds a default header to disable
            caching.

            :param url: The base URL for the request. If it starts with ':',
                        HTTP or HTTPS is prefixed.
            :type url: <str>
            :param data: Optional data to be sent with the request.
            :type data: <Optional[Any]>
            :param headers: Optional headers to be included in the request.
            :type headers: <Optional[Dict[str, str]]>
            :param bump: String used to append to timestamp for cache control.
            :type bump: <str>
            :param secure: If True, the scheme https is used; otherwise, http.
            :type secure: <bool>
            :return: A configured Request object ready to be used with urlopen.
            :rtype: <Request>
            :exceptions: None
        '''
        scheme: str | None = None
        if not headers:
            headers = {}
        if url[0] == ':':
            scheme = ('http', 'https')[bool(secure)]
            schemed_url: str = f'{scheme}{url}'
        else:
            schemed_url = url
        if '?' in url:
            delim = '&'
        else:
            delim = '?'
        time_param: int = int(time.time() * 1000)
        final_url: str = f'{schemed_url}{delim}x={time_param}.{bump}'
        headers.update({'Cache-Control': 'no-cache'})
        return Request(final_url, data=data, headers=headers)
