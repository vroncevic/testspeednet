# -*- coding: UTF-8 -*-

'''
Module
    user_agent.py
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
    Defines class UserAgent with attribute(s) and method(s).
'''

import platform
from typing import List

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class UserAgent:
    '''
        Defines class UserAgent with attribute(s) and method(s).

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | build_user_agent - Constructs a user agent string based
                |                    on platform and py version information.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::USER_AGENT'

    @classmethod
    def build_user_agent(cls) -> str:
        '''
            Constructs a user agent string based on platform and py version.

            :return: The constructed user agent string
            :rtype: <str>
            :exceptions: None
        '''
        ua_tuple: List[str] = [
            'Mozilla/5.0',
            f'({platform.platform()}; U; {platform.architecture()[0]}; en-us)',
            f'Python/{platform.python_version()}',
            '(KHTML, like Gecko)',
            'speedtest-cli/2.1.2'
        ]
        user_agent: str = ' '.join(ua_tuple)
        return user_agent
