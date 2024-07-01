# -*- coding: UTF-8 -*-

'''
Module
    speed.py
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
    Defines class Speed with attribute(s) and method(s).
    Defines speed operation for getting download/upload net info.
'''

import sys
from typing import Any, Dict, List

try:
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
    from testspeednet.net.test import TestNet
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Speed:
    '''
        Defines class Speed with attribute(s) and method(s).
        Defines speed operation for getting download/upload net info.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | config - Container for keeping/modifying configuration.
            :methods:
                | __init__ - Initials Speed constructor.
                | execute - Executes speed command.
                | _speed - Speed command operation.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::FETCH_CONFIG'

    def __init__(self, config: Dict[Any, Any], verbose: bool = False) -> None:
        '''
            Initials Speed constructor.

            :param config: Configuration parameters for command interface
            :type config: <Dict[Any, Any]>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} init speed command']
        )
        self.config: Dict[Any, Any] = config
        self.st: TestNet = TestNet(secure=True)

    def execute(self, verbose: bool = False) -> bool:
        '''
            Executes speed command.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} performs speed check']
        )
        speed: Dict[str, float] = self._speed()
        download: float = speed['download']
        upload: float = speed['upload']
        success_message([
            f'{self._TOOL_VERBOSE.lower()} Download: {download} Mbs'
        ])
        success_message([
            f'{self._TOOL_VERBOSE.lower()} Upload: {upload} Mbs'
        ])
        return True

    def _speed(self) -> Dict[str, float]:
        '''
            Speed command operation.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: List of informations
            :rtype: List[Any]
            :exceptions: None
        '''
        return {
            'download': self.st.download() / 1000000,
            'upload': self.st.upload() / 1000000
        }
