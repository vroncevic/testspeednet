# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Encapsulates core CLI components for simplification of CLI bundle.
'''

from __future__ import annotations

from ats_utilities.option.imanager import IOptionManager

from testspeednet.core.service.iservice import IService
from testspeednet.infrastructure.cli.setup.options import CLIBundleOptions
from testspeednet.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from testspeednet.infrastructure.cli.setup.bundle import CLIBundle
from testspeednet.infrastructure.cli.setup.keys import CLIBundleKeys
from testspeednet.infrastructure.cli.setup.registry import CLIBundleRegistry
from testspeednet.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from testspeednet.infrastructure.command.command import CommandBundle
from testspeednet.infrastructure.command.icommand_definition import ICommandDefinition
from testspeednet.infrastructure.command.icommand_executor import ICommandExecutor
from testspeednet.infrastructure.command.speed_command_definition import SpeedCommandDefinition
from testspeednet.infrastructure.command.speed_command_executor import SpeedCommandExecutor
from testspeednet.infrastructure.command.download_command_definition import DownloadCommandDefinition
from testspeednet.infrastructure.command.download_command_executor import DownloadCommandExecutor
from testspeednet.infrastructure.command.upload_command_definition import UploadCommandDefinition
from testspeednet.infrastructure.command.upload_command_executor import UploadCommandExecutor
from testspeednet.infrastructure.command.fetch_command_definition import FetchCommandDefinition
from testspeednet.infrastructure.command.fetch_command_executor import FetchCommandExecutor
from testspeednet.infrastructure.command.history_command_definition import HistoryCommandDefinition
from testspeednet.infrastructure.command.history_command_executor import HistoryCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '2.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleFactory:
    '''
        Factory for creating the CLI bundle.

        It defines:

            :methods:
                | create_bundle - Creates the CLI bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    @classmethod
    def create_bundle(cls, options: CLIBundleOptions) -> CLIBundle:
        '''
            Creates the CLI bundle with optional pre-configured options.

            :param options: The CLI bundle options.
            :return: The CLI bundle.
            :exceptions:
                | ATSValueError: The CLI bundle options must be provided and have proper values.
                | ATSTypeError:  The CLI bundle options must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The CLI bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The CLI bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The CLI bundle must be provided and have proper values.
                | ATSTypeError:  The CLI bundle must be an instance of CLIBundle and
                |                its attributes must be instances of their respective types.
        '''
        CLIBundleOptionsValidator.validate(options)

        service: IService | None = options.get(CLIBundleKeys.OPTION_SERVICE) if options else None
        parser: IOptionManager | None = options.get(CLIBundleKeys.OPTION_PARSER) if options else None

        speed_def: ICommandDefinition = SpeedCommandDefinition()
        speed_exec: ICommandExecutor = SpeedCommandExecutor(definition=speed_def)
        speed_cmd: CommandBundle = CommandBundle(definition=speed_def, executor=speed_exec)

        download_def: ICommandDefinition = DownloadCommandDefinition()
        download_exec: ICommandExecutor = DownloadCommandExecutor(definition=download_def)
        download_cmd: CommandBundle = CommandBundle(definition=download_def, executor=download_exec)

        upload_def: ICommandDefinition = UploadCommandDefinition()
        upload_exec: ICommandExecutor = UploadCommandExecutor(definition=upload_def)
        upload_cmd: CommandBundle = CommandBundle(definition=upload_def, executor=upload_exec)

        fetch_def: ICommandDefinition = FetchCommandDefinition()
        fetch_exec: ICommandExecutor = FetchCommandExecutor(definition=fetch_def)
        fetch_cmd: CommandBundle = CommandBundle(definition=fetch_def, executor=fetch_exec)

        history_def: ICommandDefinition = HistoryCommandDefinition()
        history_exec: ICommandExecutor = HistoryCommandExecutor(definition=history_def)
        history_cmd: CommandBundle = CommandBundle(definition=history_def, executor=history_exec)

        commands: list[CommandBundle] = [speed_cmd, download_cmd, upload_cmd, fetch_cmd, history_cmd]

        return CLIBundleRegistry.create_bundle(
            dependencies=CLIBundleDependencies(service=service, parser=parser, commands=commands)
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version.
            :exceptions: None.
        '''
        return __version__
