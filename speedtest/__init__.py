# -*- coding: UTF-8 -*-

'''
 Module
     __init__.py
 Copyright
     Copyright (C) 2022 Vladimir Roncevic <elektron.ronca@gmail.com>
     speedtest is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by the
     Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     speedtest is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
     See the GNU General Public License for more details.
     You should have received a copy of the GNU General Public License along
     with this program. If not, see <http://www.gnu.org/licenses/>.
 Info
     Define class SpeedTest with attribute(s) and method(s).
     Load a base info, create an CLI interface and run operation(s).
'''

import sys
from os.path import dirname, realpath

try:
    from ats_utilities.splash import Splash
    from ats_utilities.logging import ATSLogger
    from ats_utilities.cli.cfg_cli import CfgCLI
    from ats_utilities.cooperative import CooperativeMeta
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.success import success_message
except ImportError as ats_error_message:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error_message)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2022, https://vroncevic.github.io/speedtest'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/vroncevic/speedtest/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpeedTest(CfgCLI):
    '''
        Define class SpeedTest with attribute(s) and method(s).
        Load a base info, create an CLI interface and run operation(s).
        It defines:

            :attributes:
                | __metaclass__ - setting cooperative metaclasses.
                | TOOL_VERBOSE - console text indicator for process-phase.
                | CONFIG - tool info file path.
                | LOG - tool log file path.
                | LOGO - logo for splash screen.
                | OPS - list of tool options.
                | logger - logger object API.
            :methods:
                | __init__ - initial constructor.
                | process - process and run tool option(s).
    '''

    __metaclass__ = CooperativeMeta
    TOOL_VERBOSE = 'SPEEDTEST'
    CONFIG = '/conf/speedtest.cfg'
    LOG = '/log/speedtest.log'
    LOGO = '/conf/speedtest.logo'
    OPS = ['-g', '--gen', '-v', '--verbose', '--version']

    def __init__(self, verbose=False):
        '''
            Initial constructor.

            :param verbose: enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: None
        '''
        current_dir = dirname(realpath(__file__))
        speedtest_property = {
            'ats_organization': 'vroncevic',
            'ats_repository': 'speedtest',
            'ats_name': 'speedtest',
            'ats_logo_path': '{0}{1}'.format(current_dir, SpeedTest.LOGO),
            'ats_use_github_infrastructure': True
        }
        splash = Splash(speedtest_property, verbose=verbose)
        base_info = '{0}{1}'.format(current_dir, SpeedTest.CONFIG)
        CfgCLI.__init__(self, base_info, verbose=verbose)
        verbose_message(SpeedTest.TOOL_VERBOSE, verbose, 'init tool info')
        self.logger = ATSLogger(
            SpeedTest.TOOL_VERBOSE.lower(),
            '{0}{1}'.format(current_dir, SpeedTest.LOG),
            verbose=verbose
        )
        if self.tool_operational:
            self.add_new_option(
                SpeedTest.OPS[0], SpeedTest.OPS[1],
                dest='opt', help='option'
            )
            self.add_new_option(
                SpeedTest.OPS[2], SpeedTest.OPS[3],
                action='store_true', default=False,
                help='activate verbose mode for generation'
            )
            self.add_new_option(
                SpeedTest.OPS[4], action='version', version=__version__
            )

    def process(self, verbose=False):
        '''
            Process and run operation.

            :param verbose: enable/disable verbose option.
            :type verbose: <bool>
            :return: boolean status, True (success) | False.
            :rtype: <bool>
            :exceptions: None
        '''
        status = False
        if self.tool_operational:
            num_of_args_sys = len(sys.argv)
            if num_of_args_sys > 1:
                operation = sys.argv[1]
                if operation not in SpeedTest.OPS:
                    sys.argv.append('-h')
            else:
                sys.argv.append('-h')
            args = self.parse_args(sys.argv[1:])
            if bool(getattr(args, 'opt')):
                print(
                    '{0} {1} [{2}]'.format(
                        '[{0}]'.format(SpeedTest.TOOL_VERBOSE.lower()),
                        'running option', getattr(args, 'opt')
                    )
                )
                #
                # Code goes here
                #
                status = True
                if status:
                    success_message(SpeedTest.TOOL_VERBOSE, 'done\n')
                    self.logger.write_log(
                        '{0} {1} done'.format(
                            'run operation', getattr(args, 'opt')
                        ), ATSLogger.ATS_INFO
                    )
                else:
                    error_message(
                        SpeedTest.TOOL_VERBOSE, 'failed to run option'
                    )
                    self.logger.write_log(
                        'failed to run option', ATSLogger.ATS_ERROR
                    )
            else:
                error_message(
                    SpeedTest.TOOL_VERBOSE, 'provide option'
                )
                self.logger.write_log(
                    'provide option', ATSLogger.ATS_ERROR
                )
        else:
            error_message(
                SpeedTest.TOOL_VERBOSE, 'tool is not operational'
            )
            self.logger.write_log(
                'tool is not operational', ATSLogger.ATS_ERROR
            )
        return status

    def __str__(self):
        '''
            Dunder method for SpeedTest.

            :return: object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1}, {2})'.format(
            self.__class__.__name__, CfgCLI.__str__(self), str(self.logger)
        )
