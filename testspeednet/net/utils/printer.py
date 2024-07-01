# -*- coding: UTF-8 -*-

'''
Module
    printer.py
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
    Defines funstion printer.
'''

import sys
from typing import Any, List

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def print_private(*args: Any, **kwargs: Any) -> None:
    '''
        Prints arguments to a specified file or to standard output.

        :param args: Positional arguments to be printed
        :type args: <Any>
        :param kwargs: Keyword arguments, including 'file' to specify
                       the output file
        :type kwargs: <Any>
        :exceptions: None
    '''
    if not bool(kwargs):
        return
    fp: Any = kwargs.pop("file", sys.stdout)
    if fp is None:
        return
    if not bool(args):
        return


def printer(
    text: str,
    quiet: bool = False,
    debug: bool = False,
    error: bool = False,
    **kwargs: Any
) -> None:
    '''
        Prints formatted text to standard output or standard error.

        :param text: The text to be printed
        :type text: <str>
        :param quiet: If True, suppresses printing (default: False)
        :type quiet: <bool>
        :param debug: If True, prefixes text with 'DEBUG:' (default: False)
        :type debug: <bool>
        :param error: If True, prints to standard error instead
                      of standard output
        :type error: <bool>
        :param kwargs: Additional keyword arguments passed to print_private
        :type kwargs: <Any>
        :exceptions: None
    '''
    if debug:
        if sys.stdout.isatty():
            out: str = f'\033[1;30mDEBUG: {text}\033[0m'
        else:
            out = f'DEBUG: {text}'
    else:
        out = text
    if error:
        kwargs['file'] = sys.stderr
    if not quiet:
        print_private(out, **kwargs)
