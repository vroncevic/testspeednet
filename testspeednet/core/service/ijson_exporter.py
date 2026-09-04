# -*- coding: UTF-8 -*-

'''
Module
    ijson_exporter.py
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
    Defines abstract interface for JSON data export and loading.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


@runtime_checkable
class IJsonExporter(Protocol):
    '''
        Defines abstract interface for JSON data export and loading.

        It defines:

            :methods:
                | export_json - Exports data object or collection to JSON file.
                | load_json - Loads configuration dictionary from JSON file.
                | is_initialized - Checks if the exporter is initialized.
    '''

    def export_json(self, data: object, file_path: str) -> bool:
        '''
            Exports data object or collection to JSON file.

            :param data: Data object or collection to export.
            :param file_path: Path to target JSON file.
            :return: True if export succeeded, False otherwise.
            :exceptions: None.
        '''

    def load_json(self, file_path: str) -> dict[str, object]:
        '''
            Loads configuration dictionary from JSON file.

            :param file_path: Path to JSON file to load.
            :return: Loaded configuration dictionary.
            :exceptions: None.
        '''

    def is_initialized(self) -> bool:
        '''
            Checks if the exporter is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
