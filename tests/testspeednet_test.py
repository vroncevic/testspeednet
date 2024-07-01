# -*- coding: UTF-8 -*-

'''
Module
    testspeednet_test.py
Copyright
    Copyright (C)2016  -2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    testspeednet is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    testspeednet is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class NetTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of TestSpeedNet.
Execute
    python3 -m unittest -v arm_picom_test
'''

import sys
from typing import List
from unittest import TestCase, main

try:
    from testspeednet import TestSpeedNet
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NetTestCase(TestCase):
    '''
        Defines class NetTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of TestSpeedNet.
        TestSpeedNet unit tests.

        It defines:

            :attributes:
                | None
            :methods:
                | setUp - Call before test case.
                | tearDown - Call after test case.
                | test_default_create - Default on create (not None).
                | test_missing_args - Test missing args.
                | test_wrong_arg - Test wrong arg.
                | test_process - Test speed structure.
                | test_process_upload - Test upload structure.
                | test_process_download - Test download structure.
                | test_process_fetch - Test fetch structure.
                | test_tool_not_operational - Test not operational.
    '''

    def setUp(self) -> None:
        '''Call before test case.'''

    def tearDown(self) -> None:
        '''Call after test case.'''

    def test_default_create(self) -> None:
        '''Default on create (not None)'''
        generator: TestSpeedNet = TestSpeedNet()
        self.assertIsNotNone(generator)

    def test_missing_args(self) -> None:
        '''Test missing args'''
        sys.argv.clear()
        generator: TestSpeedNet = TestSpeedNet()
        self.assertFalse(generator.process())

    def test_wrong_arg(self) -> None:
        '''Test wrong arg'''
        sys.argv.clear()
        sys.argv.insert(0, '-d')
        sys.argv.insert(1, 'wrong_pro')
        generator: TestSpeedNet = TestSpeedNet()
        self.assertFalse(generator.process())

    def test_process(self) -> None:
        '''Test speed structure'''
        sys.argv.clear()
        sys.argv.insert(0, '-c')
        sys.argv.insert(1, 'speed')
        generator: TestSpeedNet = TestSpeedNet()
        self.assertTrue(generator.process())

    def test_process_upload(self) -> None:
        '''Test upload structure'''
        sys.argv.clear()
        sys.argv.insert(0, '-c')
        sys.argv.insert(1, 'upload')
        generator: TestSpeedNet = TestSpeedNet()
        self.assertTrue(generator.process())

    def test_process_download(self) -> None:
        '''Test download structure'''
        sys.argv.clear()
        sys.argv.insert(0, '-c')
        sys.argv.insert(1, 'download')
        generator: TestSpeedNet = TestSpeedNet()
        self.assertTrue(generator.process())

    def test_process_fetch(self) -> None:
        '''Test fetch structure'''
        sys.argv.clear()
        sys.argv.insert(0, '-c')
        sys.argv.insert(1, 'fetch')
        generator: TestSpeedNet = TestSpeedNet()
        self.assertTrue(generator.process())

    def test_tool_not_operational(self) -> None:
        '''Test not operational'''
        sys.argv.clear()
        sys.argv.insert(0, '-c')
        sys.argv.insert(1, 'speed')
        generator: TestSpeedNet = TestSpeedNet()
        generator.tool_operational = False
        self.assertFalse(generator.process())


if __name__ == '__main__':
    main()
