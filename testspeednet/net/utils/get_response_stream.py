# -*- coding: UTF-8 -*-

'''
Module
    get_response_stream.py
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
    Defines function get_response_stream.
    Retrieves a response stream, optionally decoding it if gzip-encoded.
'''

import sys
from typing import Any, Callable, List, Optional
from http.client import HTTPResponse

try:
    from testspeednet.net.utils.gzip_decoded_response import (
        GzipDecodedResponse
    )
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def get_response_stream(
    response: Optional[HTTPResponse]
) -> Optional[GzipDecodedResponse | HTTPResponse]:
    '''
        Retrieves a response stream, optionally decoding it if gzip-encoded.

        :param response: The HTTP response object
        :type response: <Optional[HTTPResponse]>
        :return: Either a GzipDecodedResponse or the original HTTPResponse
        :rtype: <Optional[GzipDecodedResponse | HTTPResponse]>
        :exceptions: None
    '''
    if bool(response):
        getheader: Callable[..., Any] = response.getheader
        if getheader('content-encoding') == 'gzip':
            return GzipDecodedResponse(response)
    return response
