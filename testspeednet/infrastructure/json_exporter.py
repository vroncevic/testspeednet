# -*- coding: UTF-8 -*-

'''
Module
    json_exporter.py
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
    JSON exporter adapter implementing IJsonExporter.
'''

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.utils.reflection import to_str

from testspeednet.core.service.ijson_exporter import IJsonExporter

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '2.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class JsonExporter(IJsonExporter):
    '''
        Adapter that executes JSON export and loading using ATS Storer and Loader.

        It defines:

            :attributes:
                | _context - The ContextBundle.
            :methods:
                | __init__ - Initializes the JSON exporter adapter.
                | export_json - Exports data object or collection to JSON file.
                | load_json - Loads configuration dictionary from JSON file.
                | is_initialized - Checks if the exporter is initialized.
                | __str__ - Returns the JsonExporter as string representation.
    '''

    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle | None = None) -> None:
        '''
            Initializes the JsonExporter adapter.

            :param context_bundle: Optional context bundle.
            :exceptions: None.
        '''
        self._context = context_bundle or ContextBundleFactory.create_bundle()

    def export_json(self, data: object, file_path: str) -> bool:
        '''
            Exports data to a JSON file using ATS Storer.

            :param data: Data object or collection to export.
            :param file_path: Path to target JSON file.
            :return: True if export succeeded, False otherwise.
            :exceptions: None.
        '''
        try:
            target_path = Path(file_path).resolve()
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.touch(exist_ok=True)

            payload: dict[str, object]
            if hasattr(data, '__dataclass_fields__'):
                payload = asdict(data)
            elif isinstance(data, (list, tuple)):
                items: list[object] = [
                    asdict(item) if hasattr(item, '__dataclass_fields__') else item
                    for item in data
                ]
                payload = {'items': items, 'count': len(items)}
            elif isinstance(data, dict):
                payload = dict(data)
            else:
                payload = {'data': str(data)}

            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(target_path),
                    context_bundle=self._context
                )
            )
            storer = Storer(bundle)
            return storer.store_configuration(payload)
        except Exception:
            return False

    def load_json(self, file_path: str) -> dict[str, object]:
        '''
            Loads data from a JSON file using ATS Loader.

            :param file_path: Path to JSON file to load.
            :return: Loaded configuration dictionary.
            :exceptions: None.
        '''
        try:
            target_path = Path(file_path).resolve()
            if not target_path.is_file():
                return {}

            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(target_path),
                    context_bundle=self._context
                )
            )
            loader = Loader(bundle)
            return loader.load_configuration()
        except Exception:
            return {}

    def is_initialized(self) -> bool:
        '''
            Checks if the exporter is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return True

    def __str__(self) -> str:
        '''
            Returns the JsonExporter as string representation.

            :return: The JsonExporter as string representation.
            :exceptions: None.
        '''
        return to_str(self)
