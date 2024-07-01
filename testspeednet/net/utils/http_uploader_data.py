# -*- coding: UTF-8 -*-

'''
Module
    http_uploader_data.py
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
    Defines class HTTPUploaderData with attribute(s) and method(s).
    Manage the data to be uploaded in an HTTP upload operation, including
    handling data pre-allocation and reading chunks of data for the upload.
'''

import timeit
from threading import Event
from typing import List, Optional
from io import StringIO, BytesIO
from testspeednet.net.utils.fake_shutdown_event import FakeShutdownEvent
from testspeednet.net.utils.net_exceptions import (
    SpeedtestUploadTimeout, SpeedtestCLIError
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class HTTPUploaderData:
    '''
        Defines class HTTPUploaderData with attribute(s) and method(s).
        Manage the data to be uploaded in an HTTP upload operation, including
        handling data pre-allocation and reading chunks of data for the upload.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | length - Length of the data to upload.
                | start - Start time of the upload operation.
                | timeout - Maximum allowed time for the download operation.
                | _shutdown_event - Shutdown event.
                | _data - Pre-allocated upload data buffer.
                | total - List tracking the sizes of uploaded chunks.
            :methods:
                | __init__ - Initializes an instance of HTTPUploaderData.
                | pre_allocate - Pre-allocates the data buffer for upload.
                | data - Property to get the pre-allocated data buffer.
                | read - Reads a chunk of data from the pre-allocated buffer.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::HTTP_UPLOADER_DATA'

    def __init__(
        self,
        length: int,
        start: int,
        timeout: int,
        shutdown_event: Optional[Event | FakeShutdownEvent] = None
    ) -> None:
        '''
            Initializes an instance of HTTPUploaderData.

            :param length: Length of the data to upload
            :type length: <int>
            :param start: Start time of the download operation
            :type start: <int>
            :param timeout: Maximum allowed time for the download operation
            :type timeout: <int>
            :param shutdown_event: Shutdown event
            :type shutdown_event: <Optional[Event | FakeShutdownEvent]>
            :exceptions: None
        '''
        self.length: int = length
        self.start: int = start
        self.timeout: int = timeout
        self._shutdown_event: Event | None | FakeShutdownEvent
        if shutdown_event:
            self._shutdown_event = shutdown_event
        else:
            self._shutdown_event = FakeShutdownEvent()
        self._data: BytesIO | None = None
        self.total: List[int] = [0]

    def pre_allocate(self) -> None:
        '''
            Pre-allocates the data buffer for upload.

            :exceptions: None
        '''
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        multiplier = int(round(int(self.length) / 36.0))
        IO = BytesIO or StringIO
        try:
            self._data = IO((
                f'content1={(chars * multiplier)[0:int(self.length) - 9]}'
            ).encode())
        except MemoryError as e:
            raise SpeedtestCLIError(
                'Insufficient memory to pre-allocate upload data.'
                'Please use --no-pre-allocate'
            ) from e

    @property
    def data(self) -> Optional[BytesIO]:
        '''
            Property to get the pre-allocated data buffer.

            :return: The pre-allocated data buffer
            :rtype: <Optional[BytesIO]>
            :exceptions: None
        '''
        if not self._data:
            self.pre_allocate()
        return self._data

    def read(self, n: int = 10240) -> bytes:
        '''
            Reads a chunk of data from the pre-allocated buffer.

            Reads up to `n` bytes of data from the pre-allocated buffer,
            appending the size of the read chunk to `self.total`. Raises
            `SpeedtestUploadTimeout` if the operation exceeds the allowed
            timeout or if the shutdown event is set.

            :param n: Number of bytes to read from the buffer
            :type n: <int>
            :return: A chunk of data from the pre-allocated buffer
            :rtype: <bytes>
            :exceptions: None
        '''
        if self.data is None:
            raise ValueError("data is None")
        if self._shutdown_event is None:
            raise ValueError("shutdown_event is None")
        if ((timeit.default_timer() - self.start) <= self.timeout and
                not self._shutdown_event.is_set()):
            chunk: bytes = self.data.read(n)
            self.total.append(len(chunk))
            return chunk
        raise SpeedtestUploadTimeout()

    def __len__(self) -> int:
        '''
            Returns the length of the data to upload.

            :return: The length of the data
            :rtype: <int>
            :exceptions: None
        '''
        return self.length
