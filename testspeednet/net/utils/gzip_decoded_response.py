# -*- coding: UTF-8 -*-

'''
Module
    gzip_decoded_response.py
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
    Defines class GzipDecodedResponse with attribute(s) and method(s).
    Wraps an HTTPResponse object that contains gzip-compressed content,
    providing a readable gzip file-like interface to decompress the
    response content on-the-fly.
'''

from typing import List
from gzip import GzipFile
from io import StringIO, BytesIO
from http.client import HTTPResponse

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GzipDecodedResponse(GzipFile):
    '''
        Defines class GzipDecodedResponse with attribute(s) and method(s).
        Wraps an HTTPResponse object that contains gzip-compressed content,
        providing a readable gzip file-like interface to decompress the
        response content on-the-fly.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | io (BytesIO) - In-memory bytes buffer to store and handle
                |                the decompressed response content.
            :methods:
                | __init__ - Initializes a GzipDecodedResponse object.
                | close - Closes the gzip file and the in-memory buffer.
    '''

    def __init__(self, response: HTTPResponse) -> None:
        '''
            Initializes a GzipDecodedResponse object by reading and
            decompressing the gzip-compressed content from the provided
            HTTPResponse.
            This constructor reads the response content in chunks,
            writes it to an in-memory bytes buffer, and prepares it for
            gzip decompression.

            :param response: The HTTPResponse object containing
                             the gzip-compressed content
            :type response: <HTTPResponse>
            :exceptions: None
        '''
        IO = BytesIO or StringIO
        self.io = IO()
        while 1:
            chunk: bytes = response.read(1024)
            if len(chunk) == 0:
                break
            self.io.write(chunk)
        self.io.seek(0)
        GzipFile.__init__(self, mode='rb', fileobj=self.io)

    def close(self) -> None:
        '''
            Closes the gzip file and the underlying in-memory buffer.
            This method ensures that resources are properly released by
            closing both the gzip file and the in-memory buffer.

            :exceptions: None
        '''
        try:
            GzipFile.close(self)
        finally:
            self.io.close()
