# -*- coding: UTF-8 -*-

'''
Module
    catch_request.py
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
    Makes a network request and handles exceptions that might occur.
'''

import sys
from typing import Type, List, Tuple, Callable, Optional, Union, TypeAlias
from socket import error
from ssl import CertificateError, SSLError
from urllib.request import HTTPError, Request, OpenerDirector, urlopen
from http.client import BadStatusLine, HTTPResponse

try:
    from ats_utilities.console_io.success import success_message
    from testspeednet.net.utils.get_exception import get_exception
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

HTTP_ERRORS: Tuple[Type[BaseException], ...] = (
    (HTTPError, error, SSLError, BadStatusLine) + (CertificateError,)
)

CatchRequestResult: TypeAlias = Tuple[
    Optional[HTTPResponse], Union[bool, BaseException | None]
]


class CatchRequest:
    '''
        Defines class CatchRequest with attribute(s) and method(s).
        Makes a network request and handles exceptions that might occur.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | catch_request - Makes a network request.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::CATCH_REQUEST'

    @classmethod
    def catch_request(
        cls, request: Request, opener: Optional[OpenerDirector] = None
    ) -> CatchRequestResult:
        '''
            Makes a network request.

            :param request: The HTTP request object to be opened
            :type request: <Request>
            :param opener: A custom opener
            :type opener: <Optional[OpenerDirector]>
            :return: Tuple containing the HTTP response object if successful,
                     otherwise None; and a boolean indicating no error (False)
                     or the caught exception if an error occurs
            :rtype: <CatchRequestResult>
            :exceptions: None
        '''
        if opener:
            _open: Callable[[Request], HTTPResponse] = opener.open
        else:
            _open: Callable[[Request], HTTPResponse] = urlopen
        try:
            uh: HTTPResponse = _open(request)
            if request.get_full_url() != uh.geturl():
                success_message([
                    f'{cls._TOOL_VERBOSE.lower()} Redirected to {uh.geturl()}'
                ])
            return uh, False
        except HTTP_ERRORS:
            exception: Optional[BaseException] = get_exception()
            return None, exception
