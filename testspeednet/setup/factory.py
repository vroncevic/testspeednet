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
    Factory for creating the testspeednet bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from testspeednet.setup.bundle import TestSpeedNetBundle
from testspeednet.setup.options import TestSpeedNetBundleOptions
from testspeednet.setup.registry import TestSpeedNetBundleRegistry
from testspeednet.setup.dependencies import TestSpeedNetBundleDependencies
from testspeednet.setup.opt_validator import TestSpeedNetBundleOptionsValidator
from testspeednet.setup.keys import TestSpeedNetBundleKeys
from testspeednet.core.service.engine import Service
from testspeednet.core.service.iservice import IService
from testspeednet.core.service.iserver_repository import IServerRepository
from testspeednet.core.service.isubprocessor import ISubProcessor
from testspeednet.core.service.inetwork_speed_tester import INetworkSpeedTester
from testspeednet.core.service.ijson_exporter import IJsonExporter
from testspeednet.infrastructure.database.server_repository import ServerRepository
from testspeednet.infrastructure.network_speed_tester import NetworkSpeedTester
from testspeednet.infrastructure.json_exporter import JsonExporter
from testspeednet.infrastructure.subprocessor import SubProcessor
from testspeednet.infrastructure.cli.engine import CLI
from testspeednet.infrastructure.cli.icli import ICLI
from testspeednet.infrastructure.cli.setup.bundle import CLIBundle
from testspeednet.infrastructure.cli.setup.factory import CLIBundleFactory
from testspeednet.infrastructure.cli.setup.options import CLIBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '2.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpeedNetBundleFactory:
    '''
        Factory for creating the testspeednet bundle.

        It defines:

            :attributes:
                | _info_file - Path to the testspeednet info file.
            :methods:
                | create_bundle - Creates the testspeednet bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = 'testspeednet/infrastructure/config/testspeednet.cfg'

    @classmethod
    def create_bundle(cls, options: TestSpeedNetBundleOptions | None = None) -> TestSpeedNetBundle:
        '''
            Creates the testspeednet bundle with optional pre-configured options.

            :param options: The pre-configured options for the testspeednet bundle.
            :return: The testspeednet bundle.
            :exceptions:
                | ATSValueError: The testspeednet bundle options must be provided and have proper values.
                | ATSTypeError:  The testspeednet bundle options must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The testspeednet bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The testspeednet bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The testspeednet bundle must be provided and have proper values.
                | ATSTypeError:  The testspeednet bundle must be an instance of TestSpeedNetBundle and
                |                its attributes must be instances of their respective types.
        '''
        if options is not None:
            TestSpeedNetBundleOptionsValidator.validate(options)

        info_file = options.get(TestSpeedNetBundleKeys.OPTION_INFO_FILE) if options else cls._info_file

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        server_repository: IServerRepository = ServerRepository()
        speed_tester: INetworkSpeedTester = NetworkSpeedTester()
        json_exporter: IJsonExporter = JsonExporter(context_bundle=context_bundle)

        subprocessor: ISubProcessor = SubProcessor(speed_tester=speed_tester)

        service: IService = Service(
            subprocessor=subprocessor,
            server_repository=server_repository,
            json_exporter=json_exporter
        )

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager
            )
        )

        cli: ICLI = CLI(cli_bundle)

        return TestSpeedNetBundleRegistry.create_bundle(
            dependencies=TestSpeedNetBundleDependencies(
                base=base_bundle,
                service=service,
                subprocessor=subprocessor,
                cli=cli
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version.
            :exceptions: None.
        '''
        return __version__
