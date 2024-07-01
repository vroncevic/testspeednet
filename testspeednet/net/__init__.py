# -*- coding: UTF-8 -*-

'''
Module
    __init__.py
Copyright
    Copyright (C) 2016 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    Defines class TestSpeedNetProcessor with attribute(s) and method(s).
    Prepares command interface and processes request.
'''

import sys
from typing import List
from os.path import dirname, realpath

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.pro_config import ProConfig
    from ats_utilities.config_io.yaml.yaml2object import Yaml2Object
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.error import error_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from testspeednet.net.speed import Speed
    from testspeednet.net.download import Download
    from testspeednet.net.upload import Upload
    from testspeednet.net.config import Fetch
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpeedNetProcessor(FileCheck, ProConfig):
    '''
        Defines class TestSpeedNetProcessor with attribute(s) and method(s).
        Prepares command interface and processes request.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | _NET_CONFIG - List of servers and countries for net checking.
                | speed - Command instance for getting speed info.
                | download - Command instance for download info.
                | upload - Command instance for upload info.
                | fetch - Command instance for fetch configuration.
            :methods:
                | __init__ - Initials TestSpeedNetProcessor constructor.
                | execute - Executes command parsed from arguments.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::TEST_SPEED_NET_PROCESSOR'
    _NET_CONFIG: str = '/../conf/apis.yaml'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials TestSpeedNetProcessor constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        FileCheck.__init__(self, verbose)
        ProConfig.__init__(self, verbose)
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} init net cmd processor']
        )
        current_dir: str = dirname(realpath(__file__))
        net_config: str = f'{current_dir}{self._NET_CONFIG}'
        self.check_path(net_config, verbose)
        self.check_mode('r', verbose)
        self.check_format(net_config, 'yaml', verbose)
        if self.is_file_ok():
            yml2obj = Yaml2Object(net_config)
            self.config = yml2obj.read_configuration()
        self.speed: Speed | None = None
        self.download: Download | None = None
        self.upload: Upload | None = None
        self.fetch: Fetch | None = None

    def execute(self, cmd: str, verbose: bool = False) -> bool:
        '''
            Executes command parsed from arguments.

            :param cmd: Command from arguments
            :type cmd: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([('str:cmd', cmd)])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(cmd):
            raise ATSValueError('missing command')
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} executes command {cmd}']
        )
        status: bool = False
        match cmd:
            case 'speed':
                if bool(self.config):
                    self.speed = Speed(self.config, verbose)
                    status = self.speed.execute(verbose)
            case 'download':
                if bool(self.config):
                    self.download = Download(self.config, verbose)
                    status = self.download.execute(verbose)
            case 'upload':
                if bool(self.config):
                    self.upload = Upload(self.config, verbose)
                    status = self.upload.execute(verbose)
            case 'fetch':
                if bool(self.config):
                    self.fetch = Fetch(self.config, verbose)
                    status = self.fetch.execute(verbose)
            case _:
                error_message(
                    [f'{self._TOOL_VERBOSE.lower()} unexpected command {cmd}']
                )
        return status
