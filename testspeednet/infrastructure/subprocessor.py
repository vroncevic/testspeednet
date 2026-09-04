# -*- coding: UTF-8 -*-

'''
Module
    subprocessor.py
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
    Defines sub-processor adapter implementing ISubProcessor.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.utils.reflection import to_str
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.service.inetwork_speed_tester import INetworkSpeedTester
from testspeednet.core.service.isubprocessor import ISubProcessor

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class SubProcessor(ISubProcessor[Mapping[str, object], Mapping[str, object]]):
    '''
        Adapter that executes network speed test sub-processes.

        It defines:

            :attributes:
                | _speed_tester - The network speed tester adapter.
            :methods:
                | __init__ - Initializes the subprocessor adapter.
                | run - Runs a speed measurement sub-process operation.
                | is_initialized - Checks if the subprocessor is initialized.
                | __str__ - Returns the SubProcessor as string representation.
    '''

    _speed_tester: INetworkSpeedTester

    def __init__(self, speed_tester: INetworkSpeedTester) -> None:
        '''
            Initializes the SubProcessor adapter.

            :param speed_tester: The network speed tester adapter.
            :exceptions:
                | ATSValueError: The speed tester must be provided.
                | ATSTypeError:  The speed tester must implement INetworkSpeedTester.
        '''
        ctx: str = 'subprocessor::init(...)'
        not_none(speed_tester, ctx, 'the speed tester must be provided')
        istype(speed_tester, INetworkSpeedTester, ctx, 'the speed tester must implement INetworkSpeedTester')
        self._speed_tester = speed_tester

    def run(self, *, params: Mapping[str, object]) -> Mapping[str, object]:
        '''
            Runs a speed measurement sub-process operation.

            :param params: The command parameters mapping.
            :return: Result mapping with measured data.
            :exceptions: None.
        '''
        cmd = params.get('cmd')
        server_obj = params.get('server')
        server: SpeedTestServer | None = server_obj if isinstance(server_obj, SpeedTestServer) else None

        if cmd == 'fetch':
            servers: list[SpeedTestServer] = self._speed_tester.fetch_servers()
            return {'servers': servers}

        if server is None:
            return {'error': 'no target server provided'}

        if cmd == 'speed':
            ping_val: float = self._speed_tester.measure_ping(server)
            download_val: float = self._speed_tester.measure_download(server)
            upload_val: float = self._speed_tester.measure_upload(server)
            return {'ping': ping_val, 'download': download_val, 'upload': upload_val}

        if cmd == 'download':
            download_val = self._speed_tester.measure_download(server)
            return {'download': download_val}

        if cmd == 'upload':
            upload_val = self._speed_tester.measure_upload(server)
            return {'upload': upload_val}

        return {'error': f'unknown command: {cmd}'}

    def is_initialized(self) -> bool:
        '''
            Checks if the subprocessor is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return self._speed_tester.is_initialized()

    def __str__(self) -> str:
        '''
            Returns the SubProcessor as string representation.

            :return: The SubProcessor as string representation.
            :exceptions: None.
        '''
        return to_str(self)
