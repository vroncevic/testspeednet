# -*- coding: UTF-8 -*-

'''
Module
    opener.py
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
    Defines class Opener with attribute(s) and method(s).
    Creates a custom URL opener with specific handlers for HTTP and HTTPS
    requests, including proxy handling and error processing.
'''

import sys
from typing import Any, List, Optional
from urllib.request import (
    ProxyHandler, HTTPDefaultErrorHandler, HTTPRedirectHandler,
    HTTPErrorProcessor, OpenerDirector
)

try:
    from testspeednet.net.utils.test_http_handler import TestHTTPHandler
    from testspeednet.net.utils.test_https_handler import TestHTTPSHandler
    from testspeednet.net.utils.user_agent import UserAgent
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


class Opener:
    '''
        Defines class Opener with attribute(s) and method(s).
        Creates a custom URL opener with specific handlers for HTTP and HTTPS
        requests, including proxy handling and error processing.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | build_opener - Creates and returns a custom URL opener.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::OPENER'

    @classmethod
    def build_opener(cls, timeout: Optional[int] = 10) -> OpenerDirector:
        '''
            Creates and returns a custom URL opener.

            Builds an `OpenerDirector` with handlers for proxy handling,
            HTTP and HTTPS request handling, error processing, and
            redirection. It also sets a custom user agent.

            :param timeout: Maximum allowed time for opening connection
            :type timeout: <Optional[int]>
            :return: A custom opener
            :rtype: <OpenerDirector>
            :exceptions: None
        '''
        handlers: List[Any] = [
            ProxyHandler(),
            TestHTTPHandler(timeout),
            TestHTTPSHandler(timeout),
            HTTPDefaultErrorHandler(),
            HTTPRedirectHandler(),
            HTTPErrorProcessor()
        ]
        opener = OpenerDirector()
        opener.addheaders = [('User-agent', UserAgent.build_user_agent())]
        for handler in handlers:
            opener.add_handler(handler)
        return opener
