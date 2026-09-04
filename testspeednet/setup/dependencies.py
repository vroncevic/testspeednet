# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    TestSpeedNet bundle dependencies for the testspeednet bundle.
'''

from __future__ import annotations

from typing import TypedDict

from ats_utilities.base.setup.bundle import BaseBundle

from testspeednet.core.service.iservice import IService
from testspeednet.core.service.isubprocessor import ISubProcessor
from testspeednet.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '2.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpeedNetBundleDependencies(TypedDict):
    '''
        TestSpeedNet bundle dependencies for the testspeednet bundle.

        It defines:

            :attributes:
                | base - The base bundle with the base components for testspeednet.
                | service - The service orchestrating testspeednet execution.
                | subprocessor - The adapter executing testspeednet sub-processes.
                | cli - The command-line interface adapter for testspeednet.
    '''

    base: BaseBundle
    service: IService
    subprocessor: ISubProcessor
    cli: ICLI
