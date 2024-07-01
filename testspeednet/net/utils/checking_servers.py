# -*- coding: UTF-8 -*-

'''
Module
    checking_servers.py
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
    Defines class NeighbourServer with attribute(s) and method(s).
'''

import sys
import xml.parsers.expat
import xml.etree.ElementTree as ET
from typing import Any, List, Dict, Tuple, Generator, Callable, Optional
from ssl import CertificateError, SSLError
from socket import error
from os.path import dirname
from timeit import default_timer
from time import time
from http.client import BadStatusLine, HTTPResponse
from urllib.request import HTTPError, OpenerDirector, Request
from urllib.parse import ParseResult, urlparse

try:
    from testspeednet.net.utils.distance import distance
    from testspeednet.net.utils.printer import printer
    from testspeednet.net.utils.get_exception import get_exception
    from testspeednet.net.utils.requester import Requester
    from testspeednet.net.utils.catch_request import CatchRequest
    from testspeednet.net.utils.get_response_stream import (
        get_response_stream
    )
    from testspeednet.net.utils.user_agent import UserAgent
    from testspeednet.net.utils.gzip_decoded_response import (
        GzipDecodedResponse
    )
    from testspeednet.net.utils.test_http_connection import TestHTTPConnection
    from testspeednet.net.utils.test_https_connection import (
        TestHTTPSConnection
    )
    from testspeednet.net.utils.net_exceptions import (
        ServersRetrievalError, NoMatchedServers, SpeedtestServersError,
        SpeedtestBestServerFailure
    )
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

etree_iter: Callable[..., Generator[ET.Element, None, None]] = ET.Element.iter
CERT_ERROR: Tuple[Any] = (CertificateError,)
HTTP_ERRORS = (
    (HTTPError, error, SSLError, BadStatusLine) +
    CERT_ERROR
)


class NeighbourServer:
    '''
        Defines class NeighbourServer with attribute(s) and method(s).

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | __init__ - Initializes an instance of NeighbourServer.
                | get_servers - Retrieves a dictionary of servers
                |               from speedtest.net.
                | get_best_server - Finds and returns the best server
                |                   based on latency.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::NEIGHBOUR_SERVER'

    def __init__(
        self,
        config: Dict[str, Any],
        secure: bool = False,
        opener: Optional[OpenerDirector] = None
    ) -> None:
        '''
            Initializes an instance of NeighbourServer.

            :param config: Configuration dictionary
            :type config: <Dict[str, Any]>
            :param secure: Flag indicating HTTPS usage
            :type secure: <bool>
            :param opener: A custom opener
            :type opener: <Optional[OpenerDirector]>
            :exceptions: None
        '''
        self.config: Dict[str, Any] = config
        self.secure: bool = secure
        self.opener: Optional[OpenerDirector] = opener

    def get_servers(self) -> Optional[Dict[Any, Any]]:
        '''
            Retrieves a dictionary of servers from speedtest.net.

            :return: Dictionary of servers
            :rtype: <Optional[Dict[Any, Any]]>
            :exceptions: ServersRetrievalError
        '''
        urls: List[str] = [
            '://www.speedtest.net/speedtest-servers-static.php',
            'http://c.speedtest.net/speedtest-servers-static.php',
            '://www.speedtest.net/speedtest-servers.php',
            'http://c.speedtest.net/speedtest-servers.php',
        ]
        servers: Dict[Any, Any] = {}
        headers: Dict[str, str] = {}
        headers['Accept-Encoding'] = 'gzip'
        errors: List[str] = []
        for url in urls:
            try:
                request: Request = Requester.build_request(
                    url=f'{url}?threads={self.config["threads"]["download"]}',
                    headers=headers,
                    secure=self.secure
                )
                uh: HTTPResponse | None
                e: bool | BaseException | None
                uh, e = CatchRequest.catch_request(request, opener=self.opener)
                if e:
                    errors.append(f'{e}')
                    raise ServersRetrievalError()
                stream: GzipDecodedResponse | HTTPResponse | None
                stream = get_response_stream(uh)
                if not bool(stream):
                    return None
                serversxml_list: List[bytes] = []
                while 1:
                    try:
                        serversxml_list.append(stream.read(1024))
                    except (OSError, EOFError) as e:
                        raise ServersRetrievalError(get_exception()) from e
                    if len(serversxml_list[-1]) == 0:
                        break
                stream.close()
                if bool(uh):
                    uh.close()
                    if int(uh.code) != 200:  # type: ignore
                        raise ServersRetrievalError()
                serversxml: bytes = ''.encode().join(serversxml_list)
                try:
                    try:
                        root: ET.Element = ET.fromstring(serversxml)
                    except ET.ParseError as e:
                        raise SpeedtestServersError(
                            f'Malformed speedtest.net list: {get_exception()}'
                        ) from e
                    elements: Generator[
                        ET.Element, None, None
                    ] = etree_iter(root, 'server')
                except (SyntaxError, xml.parsers.expat.ExpatError) as e:
                    raise ServersRetrievalError() from e
                for server in elements:
                    attrib: Dict[str, Any] = server.attrib
                    server_id: int = int(attrib.get('id', 0))
                    if server_id in self.config['ignore_servers']:
                        continue
                    try:
                        d: float = distance(
                            (
                                float(self.config['client']['lat']),
                                float(self.config['client']['lon'])
                            ),
                            (
                                float(attrib.get('lat', 0.0)),
                                float(attrib.get('lon', 0.0))
                            )
                        )
                    except ValueError:
                        continue
                    attrib['d'] = d
                    servers[d] = [attrib]
                break
            except ServersRetrievalError:
                continue
        if not servers:
            raise NoMatchedServers()
        else:
            return servers

    def get_best_server(self, limit: int = 5) -> Optional[Dict[str, Any]]:
        '''
            Finds and returns the best server based on latency.

            :param limit: Maximum number of servers to consider.
            :type limit: <int>
            :return: Best server dictionary
            :rtype: <Optional[Dict[str, Any]]>
            :exceptions: SpeedtestBestServerFailure
        '''
        servers: Dict[Any, Any] | None = self.get_servers()
        closest: List[Dict[Any, Any]] = []
        if bool(servers):
            for d in sorted(servers.keys()):
                for s in servers[d]:
                    closest.append(s)
                    if len(closest) == limit:
                        break
                else:
                    continue
                break
        else:
            return None
        user_agent: str = UserAgent.build_user_agent()
        results: Dict[Any, Any] = {}
        for server in closest:
            cum: List[int | float] = []
            url: str = dirname(server['url'])
            stamp = int(time() * 1000)
            latency_url: str = f'{url}/latency.txt?x={stamp}'
            i: int = 0
            while True:
                urlparts: ParseResult = urlparse(latency_url)
                try:
                    if urlparts[0] == 'https':
                        h = TestHTTPSConnection(urlparts[1])
                    else:
                        h = TestHTTPConnection(urlparts[1])
                    headers: Dict[str, str] = {'User-Agent': user_agent}
                    path: str = f'{urlparts[2]}?{urlparts[4]}'
                    start: float = default_timer()
                    h.request("GET", path, headers=headers)
                    r: HTTPResponse = h.getresponse()
                    total: float = default_timer() - start
                except HTTP_ERRORS:
                    printer(f'ERROR: {get_exception()}', debug=False)
                    cum.append(3600)
                    continue
                text: bytes = r.read(9)
                if int(r.status) == 200 and text == 'test=test'.encode():
                    cum.append(total)
                else:
                    cum.append(3600)
                h.close()
                i += 1
                if i >= 3:
                    break

            avg: float = round((sum(cum) / 6) * 1000.0, 3)
            results[avg] = server

        try:
            fastest: float = sorted(results.keys())[0]
        except IndexError as e:
            raise SpeedtestBestServerFailure(
                'Unable to connect to servers to test latency.'
            ) from e
        best: Dict[str, Any] = results[fastest]
        best['latency'] = fastest
        return best
