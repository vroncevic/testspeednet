# -*- coding: UTF-8 -*-

'''
Module
    upload_command_executor.py
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
    Defines UploadCommandExecutor class.
'''

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict

from ats_utilities.utils.reflection import to_str

from testspeednet.core.model.speed_test_server import SpeedTestServer
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


class UploadCommandExecutor:
    '''
        Command executor strategy for upload speed checking.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
            :methods:
                | __init__ - Initializes the upload command executor.
                | execute - Executes the upload subcommand.
                | get_definition - Returns the command definition metadata.
                | __str__ - Returns string representation of UploadCommandExecutor.
    '''

    definition: ICommandDefinition

    def __init__(self, definition: ICommandDefinition) -> None:
        '''
            Initializes the upload command executor.

            :param definition: The command definition metadata.
            :exceptions: None.
        '''
        self.definition = definition

    def execute(self, *, params: Mapping[str, object], service: IService) -> Mapping[str, object]:
        '''
            Executes the upload subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: Command orchestrator service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        if not service.is_initialized():
            return {'returncode': 1, 'stdout': '', 'stderr': 'service not initialized'}

        upload_val, server = service.execute_upload()
        if server is None:
            return {'returncode': 1, 'stdout': '', 'stderr': 'no servers available'}

        json_path = params.get('json')
        if isinstance(json_path, str) and json_path:
            service.export_json(
                data={'upload': upload_val, 'server': asdict(server)},
                file_path=json_path
            )

        stdout_msg: str = (
            f'Server: {server.name} ({server.country}) by {server.sponsor}\n'
            f'Upload: {upload_val} Mbps\n'
            f'Saved to sqlite database.'
        )
        return {'returncode': 0, 'stdout': stdout_msg, 'stderr': ''}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition

    def __str__(self) -> str:
        '''
            Returns string representation of UploadCommandExecutor.

            :return: String representation of UploadCommandExecutor.
            :exceptions: None.
        '''
        return to_str(self)
