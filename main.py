# -*- coding: UTF-8 -*-

'''
Module
    main.py
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
    Main entry point for testspeednet CLI.
'''

from __future__ import annotations

from sys import exit as sys_exit

from testspeednet.engine import TestSpeedNet
from testspeednet.setup.factory import TestSpeedNetBundleFactory

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


def main() -> bool:
    '''
        Bootstraps and runs testspeednet with required adapters.

        :return: True if successful, False otherwise.
        :exceptions: None.
    '''
    testspeednet: TestSpeedNet = TestSpeedNet(TestSpeedNetBundleFactory.create_bundle())
    return testspeednet.process()


if __name__ == '__main__':
    '''
        Entry point for testspeednet execution.

        :exit code: 0 if successful, 1 otherwise.
        :exceptions: None.
    '''
    sys_exit(0 if main() else 1)
