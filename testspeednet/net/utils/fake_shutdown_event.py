# -*- coding: UTF-8 -*-

'''
Module
    fake_shutdown_event.py
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
    Defines class FakeShutdownEvent with attribute(s) and method(s).
    Mock implementation of a shutdown event.
'''

from typing import List

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FakeShutdownEvent:
    '''
        Defines class FakeShutdownEvent with attribute(s) and method(s).
        Mock implementation of a shutdown event.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | is_set - Indicates whether the shutdown event is set.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::FAKE_SHUTDOWN_EVENT'

    @staticmethod
    def is_set() -> bool:
        '''
            Indicates whether the shutdown event is set.

            :return: Always returns `False`.
            :rtype: <bool>
            :exceptions: None
        '''
        return False
