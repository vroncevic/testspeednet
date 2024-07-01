# -*- coding: UTF-8 -*-

'''
Module
    config.py
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
    Defines class Fetch with attribute(s) and method(s).
    Defines fetch operation for getting available servers.
'''

import sys
from typing import Any, Dict, List
from time import sleep

try:
    from requests import get, Response
    from sqlalchemy import create_engine, Engine
    from sqlalchemy.orm import sessionmaker
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
    from testspeednet.net.model import SpeedTestServer, Base
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


class Fetch:
    '''
        Defines class Fetch with attribute(s) and method(s).
        Defines fetch operation for getting available servers.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | config - Container for keeping/modifying configuration.
            :methods:
                | __init__ - Initials Fetch constructor.
                | execute - Executes fetch command.
                | _fetch_server_list - Fetches the server list.
                | _store_server_list - Stores the server list.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::FETCH_CONFIG'

    def __init__(self, config: Dict[Any, Any], verbose: bool = False) -> None:
        '''
            Initials Fetch constructor.

            :param config: Configuration parameters for command interface
            :type config: <Dict[Any, Any]>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} init fetch command']
        )
        self.config: Dict[Any, Any] = config

    def execute(self, verbose: bool = False) -> bool:
        '''
            Fetch command.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        verbose_message(
            verbose, [f'{self._TOOL_VERBOSE.lower()} performs fetch config']
        )
        available_servers: List[Any] = self._fetch_server_list(verbose)
        self._store_server_list(available_servers)
        return True

    def _fetch_server_list(self, verbose: bool = False) -> List[Any]:
        '''
            Fetches the server list.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: List with servers
            :rtype: <List[Any]>
            :exceptions: None
        '''
        list_servers: List[Any] = []
        server: str = self.config['server']
        countries: List[str] = self.config['countries']
        for country in countries:
            success_message(
                [
                    f'{self._TOOL_VERBOSE.lower()}',
                    f'fetching configuration for country {country}'
                ]
            )
            response: Response = get(url=f'{server}{country}', timeout=4)
            if len(response.json()) > 0 and int(response.status_code) == 200:
                for result in response.json():
                    list_servers.append(result)
            sleep(1)
        verbose_message(
            verbose,
            [
                f'{self._TOOL_VERBOSE.lower()}',
                f'Number of test servers {len(list_servers)}'
            ]
        )
        return list_servers

    def _store_server_list(
        self, available_servers: List[Any], verbose: bool = False
    ) -> bool:
        '''
            Stores the server list.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        success_message(
            [
                f'{self._TOOL_VERBOSE.lower()} performs store configuration,',
                'please wait...'
            ]
        )
        engine: Engine = create_engine('sqlite:///testspeednet_servers.db')
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        for index, server_info in enumerate(available_servers, start=1):
            server = SpeedTestServer(
                id=index,
                server_id=server_info['id'],
                url=server_info['url'],
                lat=server_info['lat'],
                lon=server_info['lon'],
                distance=server_info['distance'],
                name=server_info['name'],
                country=server_info['country'],
                cc=server_info['cc'],
                sponsor=server_info['sponsor'],
                preferred=server_info['preferred'],
                host=server_info['host'],
            )
            verbose_message(
                verbose,
                [
                    f'{self._TOOL_VERBOSE.lower()} performs store config',
                    f'{str(server)}'
                ]
            )
            session.add(server)
            session.commit()
        return True
