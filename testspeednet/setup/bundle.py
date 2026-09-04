# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Defines the testspeednet bundle.
'''

from __future__ import annotations

from dataclasses import dataclass

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.utils.reflection import instance_to_dict

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


@dataclass(slots=True, frozen=True, kw_only=True)
class TestSpeedNetBundle:
    '''
        TestSpeedNet bundle holding the components of testspeednet.

        It defines:

            :attributes:
                | base - The base bundle with the base components.
                | service - The service orchestrating the testspeednet execution.
                | subprocessor - The adapter executing the testspeednet sub-processes.
                | cli - The command-line interface adapter.
            :methods:
                | to_dict - Converts the testspeednet bundle to a dictionary.
    '''

    base: BaseBundle
    service: IService
    subprocessor: ISubProcessor
    cli: ICLI

    def to_dict(self) -> dict[str, object]:
        '''
            Converts the testspeednet bundle to a dictionary.

            :return: Dictionary representation of the testspeednet bundle.
            :exceptions: None.
        '''
        return instance_to_dict(self)
