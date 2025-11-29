# -*- coding: UTF-8 -*-

'''
Module
    download.py
Copyright
    Copyright (C) 2016 - 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    Defines class Download with attribute(s) and method(s).
    Defines download operation for getting download net info.
'''

import sys
from typing import Any, Dict, List

try:
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
    from testspeednet.net.test import TestNet
except ImportError as ats_error_message:  # pragma: no cover
    # Force exit python #######################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')  # pragma: no cover

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '1.0.3'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class Download:
    '''
        Defines class Download with attribute(s) and method(s).
        Defines download operation for getting download net info.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | config - Container for keeping/modifying configuration.
            :methods:
                | __init__ - Initials Download constructor.
                | execute - Executes download command.
                | _download - Download command operation.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::DOWNLOAD'

    def __init__(self, config: Dict[Any, Any], verbose: bool = False) -> None:
        '''
            Initials Download constructor.

            :param config: Configuration parameters for command interface
            :type config: <Dict[Any, Any]>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} init download command']
        )
        self.config: Dict[Any, Any] = config
        self.st: TestNet = TestNet(secure=True)

    def execute(self, verbose: bool = False) -> bool:
        '''
            Executes download command.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} performs download check']
        )
        speed: Dict[str, float] = self._download()
        download: float = speed['download']
        success_message([
            f'{self._TOOL_VERBOSE.lower()} Download: {download} Mbs'
        ])
        return True

    def _download(self) -> Dict[str, float]:
        '''
            Download command operation.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: Dict with informations
            :rtype: <Dict[str, float]>
            :exceptions: None
        '''
        return {'download': self.st.download() / 1000000}
