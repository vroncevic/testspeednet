# -*- coding: UTF-8 -*-

'''
Module
    dep_validator.py
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
    Validator for the CLI bundle dependencies.
'''

from __future__ import annotations

from collections.abc import Mapping
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from testspeednet.infrastructure.cli.setup.keys import CLIBundleKeys
from testspeednet.infrastructure.cli.setup.dependencies import CLIBundleDependencies

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class CLIBundleDependenciesValidator:
    '''
        Validator for the CLI bundle dependencies.

        It defines:

            :methods:
                | validate - Validates the CLI bundle dependencies.
                | is_valid - Checks if the CLI bundle dependencies is valid.
    '''

    @classmethod
    def validate(cls, dependencies: CLIBundleDependencies) -> None:
        '''
            Validates the CLI bundle dependencies.

            :param dependencies: The CLI bundle dependencies to be validated.
            :exceptions:
                | ATSValueError: The CLI bundle dependencies must be provided and have proper values.
                | ATSTypeError: The CLI bundle dependencies must be an instance of Mapping and its
                | attributes must be instances of their respective types.
        '''
        ctx: str = 'cli_bundle_dependencies_validator::validate(...)'
        msg_dependencies_none: str = 'the cli bundle dependencies must be provided'
        msg_dependencies_istype: str = 'the cli bundle dependencies must be a Mapping'

        not_none(dependencies, ctx, msg_dependencies_none)
        istype(dependencies, Mapping, ctx, msg_dependencies_istype)

        for attr_name, expected_type in CLIBundleKeys.get_dependency_to_type().items():
            msg_attr_name_none: str = f'the {attr_name.replace("_", " ")} must be provided'
            msg_attr_name_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'

            attribute = dependencies.get(attr_name)

            not_none(attribute, ctx, msg_attr_name_none)
            istype(attribute, expected_type, ctx, msg_attr_name_istype)

    @classmethod
    def is_valid(cls, dependencies: CLIBundleDependencies) -> bool:
        '''
            Checks if the CLI bundle dependencies is valid.

            :param dependencies: The CLI bundle dependencies to be checked.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(dependencies)
            return True

        except (ATSValueError, ATSTypeError):
            return False
