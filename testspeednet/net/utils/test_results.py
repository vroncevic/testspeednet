# -*- coding: UTF-8 -*-

'''
Module
    test_results.py
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
    Defines class TestResults with attribute(s) and method(s).
'''

import sys
from typing import Any, Dict, List, Optional
from datetime import datetime, UTC
from json import dumps
from hashlib import md5
from urllib.parse import parse_qs
from urllib.request import OpenerDirector, Request
from http.client import HTTPResponse

try:
    from testspeednet.net.utils.net_exceptions import (
        ShareResultsSubmitFailure, ShareResultsConnectFailure
    )
    from testspeednet.net.utils.opener import Opener
    from testspeednet.net.utils.catch_request import CatchRequest
    from testspeednet.net.utils.requester import Requester
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestResults:
    '''
        Defines class TestResults with attribute(s) and method(s).

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
                | download - Amount of data downloaded in bytes.
                | upload - Amount of data uploaded in bytes.
                | ping - Ping latency in milliseconds.
                | server - Details about the server used for testing.
                | client - Details about the client's environment.
                | _share - URL to share results if available.
                | timestamp - Timestamp of when the test was conducted.
                | bytes_received - Total bytes received during the test.
                | bytes_sent - Total bytes sent during the test.
                | _opener - HTTP opener used for requests.
                | _secure - Indicates if the connection is secure.
            :methods:
                | __init__ - Initializes an instance of TestResults.
                | share - Submits test results to speedtest.net and
                |         returns the shareable URL of the test result image.
                | dict - Representation of TestResults attributes.
                | json - JSON string representation of TestResults attributes.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::TEST_RESULTS'

    def __init__(
        self,
        download: int = 0,
        upload: int = 0,
        ping: int = 0,
        server: Optional[Dict[str, Any]] = None,
        client: Optional[Dict[str, Any]] = None,
        opener: Optional[OpenerDirector] = None,
        secure: bool = False
    ) -> None:
        '''
            Initializes an instance of TestResults.

            :param download: Amount of data downloaded in bytes
            :type download: <int>
            :param upload: Amount of data uploaded in bytes
            :type upload: <int>
            :param ping: Ping latency in milliseconds
            :type ping: <int>
            :param server: Details about the server used for testing
            :type server: <Optional[Dict[str, Any]]>
            :param client: Details about the client's environment
            :type client: <Optional[Dict[str, Any]]>
            :param opener: HTTP opener used for requests
            :type opener: <Optional[OpenerDirector]>
            :param secure: Indicates if the connection is secure
            :type secure: <bool>
            :exceptions: None
        '''
        self.download: int = download
        self.upload: int = upload
        self.ping: int = ping
        self.server: Dict[str, Any] = server or {}
        self.client: Dict[str, Any] = client or {}
        self._share: str | None = None
        now_date: str = datetime.now(UTC).isoformat()
        self.timestamp: str = f'{now_date}Z'
        self.bytes_received = 0
        self.bytes_sent = 0
        self._opener: OpenerDirector
        if opener:
            self._opener = opener
        else:
            self._opener = Opener.build_opener()
        self._secure: bool = secure

    def __repr__(self) -> str:
        '''
            Returns a string representation of the TestResults instance.

            :return:
            :rtype: <str>
            :exceptions: None
        '''
        return repr(self.dict())

    def share(self) -> Optional[str]:
        '''
            Submits test results to speedtest.net and returns the shareable URL
            of the test result image.

            :return: String representation of TestResults
            :rtype: <Optional[str]>
            :exceptions: ShareResultsSubmitFailure | ShareResultsConnectFailure
        '''
        if self._share:
            return self._share
        download = int(round(self.download / 1000.0, 0))
        ping = int(round(self.ping, 0))
        upload = int(round(self.upload / 1000.0, 0))
        api_hash: str = md5(
            (f'{ping}-{upload}-{download}-297aae72').encode()
        ).hexdigest()
        api_data: List[str] = [
            f'recommendedserverid={self.server["id"]}',
            f'ping={ping}',
            'screenresolution=',
            'promo=',
            f'download={download}',
            'screendpi=',
            f'upload={upload}',
            'testmethod=http',
            f'hash=_{api_hash}',
            'touchscreen=none',
            'startmode=pingselect',
            'accuracy=1',
            f'bytesreceived={self.bytes_received}',
            f'bytessent={self.bytes_sent}',
            f'serverid={self.server["id"]}'
        ]
        headers: Dict[str, str] = {
            'Referer': 'http://c.speedtest.net/flash/speedtest.swf'
        }
        request: Request = Requester.build_request(
            url='://www.speedtest.net/api/api.php',
            data='&'.join(api_data).encode(),
            headers=headers,
            secure=self._secure
        )
        res: HTTPResponse | None
        e: bool | BaseException | None
        res, e = CatchRequest.catch_request(request, opener=self._opener)
        if e:
            raise ShareResultsConnectFailure(e)
        if bool(res):
            response: bytes = res.read()
            res_code: int = res.getcode()
            res.close()
            if int(res_code) != 200:
                raise ShareResultsSubmitFailure(
                    'Could not submit results to speedtest.net'
                )
            qsargs: Dict[str, List[str]] = parse_qs(response.decode())
            resultid: List[str] | None = qsargs.get('resultid')
            if not resultid or len(resultid) != 1:
                raise ShareResultsSubmitFailure(
                    'Could not submit results to speedtest.net'
                )
            self._share = f'http://www.speedtest.net/result/{resultid[0]}.png'
        return self._share

    def dict(self) -> Dict[str, Any]:
        '''
            Returns a dictionary representation of TestResults attributes.

            :return: Dictionary containing TestResults attributes
            :rtype: <Dict[str, Any]>
            :exceptions: None
        '''
        return {
            'download': self.download,
            'upload': self.upload,
            'ping': self.ping,
            'server': self.server,
            'timestamp': self.timestamp,
            'bytes_sent': self.bytes_sent,
            'bytes_received': self.bytes_received,
            'share': self._share,
            'client': self.client,
        }

    def json(self, pretty: bool = False) -> str:
        '''
            Returns a JSON string representation of TestResults attributes.

            :param pretty: Whether to format JSON string prettily
            :type pretty: <bool>
            :return: JSON string representation of TestResults attributes
            :rtype: <str>
            :exceptions: None
        '''
        kwargs: Dict[str, Any] = {}
        if pretty:
            kwargs.update({'indent': 4, 'sort_keys': True})
        return dumps(self.dict(), **kwargs)
