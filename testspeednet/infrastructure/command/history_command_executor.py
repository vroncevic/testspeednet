# -*- coding: UTF-8 -*-

'''
Module
    history_command_executor.py
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
    Defines HistoryCommandExecutor class.
'''

from __future__ import annotations

from collections.abc import Mapping, Sequence

from ats_utilities.utils.reflection import to_str

from testspeednet.core.model.speed_test_stat import SpeedTestStat
from testspeednet.core.service.iservice import IService
from testspeednet.infrastructure.command.icommand_definition import ICommandDefinition

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class HistoryCommandExecutor:
    '''
        Command executor strategy for viewing speed test measurement history.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
            :methods:
                | __init__ - Initializes the history command executor.
                | execute - Executes the history subcommand.
                | get_definition - Returns the command definition metadata.
                | __str__ - Returns string representation of HistoryCommandExecutor.
    '''

    definition: ICommandDefinition

    def __init__(self, definition: ICommandDefinition) -> None:
        '''
            Initializes the history command executor.

            :param definition: The command definition metadata.
            :exceptions: None.
        '''
        self.definition = definition

    def execute(self, *, params: Mapping[str, object], service: IService) -> Mapping[str, object]:
        '''
            Executes the history subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: Command orchestrator service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        if not service.is_initialized():
            return {'returncode': 1, 'stdout': '', 'stderr': 'service not initialized'}

        limit_val = params.get('limit', 50)
        limit: int = int(limit_val) if limit_val is not None else 50
        stats: Sequence[SpeedTestStat] = service.get_history(limit=limit)

        json_path = params.get('json')
        if isinstance(json_path, str) and json_path:
            service.export_json(data=stats, file_path=json_path)

        lines: list[str] = [
            f'{"ID":<5} {"Timestamp":<22} {"Operation":<12} {"Down (Mbps)":<13} {"Up (Mbps)":<11} {"Latency (ms)":<13} {"Server":<25}',
            '-' * 105
        ]
        for s in stats:
            lat_str = f'{s.latency:.2f}' if s.latency is not None else 'N/A'
            lines.append(
                f'{s.id or 0:<5} {s.timestamp[:19]:<22} {s.operation:<12} {s.download_speed:<13.2f} '
                f'{s.upload_speed:<11.2f} {lat_str:<13} {s.server_name or "":<25}'
            )

        return {'returncode': 0, 'stdout': '\n'.join(lines), 'stderr': ''}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition

    def __str__(self) -> str:
        '''
            Returns string representation of HistoryCommandExecutor.

            :return: String representation of HistoryCommandExecutor.
            :exceptions: None.
        '''
        return to_str(self)
