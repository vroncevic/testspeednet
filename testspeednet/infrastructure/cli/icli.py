# -*- coding: UTF-8 -*-

'''
Module
    icli.py
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
    Defines abstract interface ICLI for command line interface.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


@runtime_checkable
class ICLI(Protocol):
    '''
        Abstract interface for the command line interface.

        It defines:

            :methods:
                | run - Parses command line arguments and executes selected command strategy.
                | is_initialized - Checks if the CLI is initialized.
    '''

    def run(self) -> dict[str, object]:
        '''
            Parses command line arguments and executes selected command strategy.

            :return: The execution result.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if the CLI is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
