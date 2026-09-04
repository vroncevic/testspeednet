# -*- coding: UTF-8 -*-

'''
Module
    command.py
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
    Defines command bundle dataclass combining command definition and executor.
'''

from __future__ import annotations

from dataclasses import dataclass

from testspeednet.infrastructure.command.icommand_definition import ICommandDefinition
from testspeednet.infrastructure.command.icommand_executor import ICommandExecutor

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


@dataclass(slots=True, frozen=True)
class CommandBundle:
    '''
        Command bundle holding command definition and command executor.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
                | executor - The command execution strategy.
            :methods:
                | None.
    '''

    definition: ICommandDefinition
    executor: ICommandExecutor[ICommandDefinition, object, object, object]
