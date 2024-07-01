# -*- coding: UTF-8 -*-

'''
Module
    do_nothing.py
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
    Defines function do_nothing.
    Nothing but print its arguments.
'''

from typing import Any, List
from testspeednet.net.utils.printer import printer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def do_nothing(*args: Any, **kwargs: Any) -> None:
    '''
        Nothing but print its arguments.

        :param args: Positional arguments passed to the function
        :type args: <Any>
        :param kwargs: Keyword arguments passed to the function
        :type kwargs: <Any>
        :exceptions: None
    '''
    printer(f'{args} {kwargs}', debug=False)
