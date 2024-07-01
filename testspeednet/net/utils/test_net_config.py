# -*- coding: UTF-8 -*-

'''
Module
    test_net_config.py
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
    Defines class TestNetConfig with attribute(s) and method(s).
    Provides methods to retrieve network configuration details
    from speedtest.net.
'''

import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional
from math import ceil
from urllib.request import OpenerDirector, Request
from http.client import HTTPResponse

try:
    from testspeednet.net.utils.get_exception import get_exception
    from testspeednet.net.utils.requester import Requester
    from testspeednet.net.utils.catch_request import CatchRequest
    from testspeednet.net.utils.get_response_stream import (
        get_response_stream
    )
    from testspeednet.net.utils.gzip_decoded_response import (
        GzipDecodedResponse
    )
    from testspeednet.net.utils.net_exceptions import (
        ConfigRetrievalError, SpeedtestConfigError
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


class TestNetConfig:
    '''
        Defines class TestNetConfig with attribute(s) and method(s).
        Provides methods to retrieve network configuration details
        from speedtest.net.

        It defines:

            :attributes:
                | _TOOL_VERBOSE - Console text indicator for process-phase.
            :methods:
                | get_config - Retrieves and parses the network configuration
                |              from speedtest.net.
    '''

    _TOOL_VERBOSE: str = 'TEST_SPEED_NET::NET::UTILS::TEST_NET_CONFIG'

    @classmethod
    def get_config(
        cls, secure: bool = False, opener: Optional[OpenerDirector] = None
    ) -> Optional[Dict[str, Any]]:
        '''
            Retrieves and parses the network configuration from speedtest.net.

            This method fetches the network configuration XML from
            speedtest.net, decodes it, and parses relevant details
            such as server configurations, download/upload configurations,
            client details, etc.

            :param secure: Flag indicating whether to use secure HTTPS
                           connection (default: False).
            :type secure: <bool>
            :param opener: Optional custom opener to use for the request
                           (default: None).
            :type opener: <Optional[OpenerDirector]>
            :return: Dictionary containing parsed network configuration.
            :rtype: <Optional[Dict[str, Any]]>
            :exceptions: ConfigRetrievalError, SpeedtestConfigError
        '''
        headers: Dict[str, Any] = {}
        headers['Accept-Encoding'] = 'gzip'
        request: Request = Requester.build_request(
            url='://www.speedtest.net/speedtest-config.php',
            headers=headers, secure=secure
        )
        uh: HTTPResponse | None
        e: bool | BaseException | None
        uh, e = CatchRequest.catch_request(request, opener=opener)
        if e:
            raise ConfigRetrievalError(e)
        configxml_list: List[bytes] = []
        stream: GzipDecodedResponse | HTTPResponse | None
        stream = get_response_stream(uh)
        if not bool(stream):
            return None
        while 1:
            try:
                configxml_list.append(stream.read(1024))
            except (OSError, EOFError) as e:
                raise ConfigRetrievalError(get_exception()) from e
            if len(configxml_list[-1]) == 0:
                break
        stream.close()
        if bool(uh):
            uh.close()
            if int(uh.code) != 200:  # type: ignore
                return None
        configxml: bytes = ''.encode().join(configxml_list)
        try:
            root: ET.Element = ET.fromstring(configxml)
        except ET.ParseError as e:
            raise SpeedtestConfigError(
                f'Malformed speedtest.net configuration: {get_exception()}'
            ) from e
        server_config: Dict[str, Any]
        server_config_element: ET.Element | None = root.find('server-config')
        if server_config_element is not None:
            server_config = server_config_element.attrib
        else:
            raise SpeedtestConfigError('Server config not found in XML')
        download: Dict[str, Any]
        download_element: ET.Element | None = root.find('download')
        if download_element is not None:
            download = download_element.attrib
        else:
            raise SpeedtestConfigError('download config not found in XML')
        upload: Dict[str, Any]
        upload_element: ET.Element | None = root.find('upload')
        if upload_element is not None:
            upload = upload_element.attrib
        else:
            raise SpeedtestConfigError('upload config not found in XML')
        client: Dict[str, Any]
        client_element: ET.Element | None = root.find('client')
        if client_element is not None:
            client = client_element.attrib
        else:
            raise SpeedtestConfigError('client config not found in XML')
        ignore_servers = list(map(int, server_config['ignoreids'].split(',')))
        ratio = int(upload['ratio'])
        upload_max = int(upload['maxchunkcount'])
        up_sizes: List[int] = [
            32768, 65536, 131072, 262144, 524288, 1048576, 7340032
        ]
        sizes: Dict[str, List[int]] = {
            'upload': up_sizes[ratio - 1:],
            'download': [
                350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000
            ]
        }
        size_count: int = len(sizes['upload'])
        upload_count = int(ceil(upload_max / size_count))
        counts: Dict[str, int] = {
            'upload': upload_count,
            'download': int(download['threadsperurl'])
        }
        threads: Dict[str, int] = {
            'upload': int(upload['threads']),
            'download': int(server_config['threadcount']) * 2
        }
        length: Dict[str, int] = {
            'upload': int(upload['testlength']),
            'download': int(download['testlength'])
        }
        try:
            config: Dict[str, Any] = {
                'config': {
                    'client': client,
                    'ignore_servers': ignore_servers,
                    'sizes': sizes,
                    'counts': counts,
                    'threads': threads,
                    'length': length,
                    'upload_max': upload_count * size_count
                },
                'lat_lon': (
                    float(client['lat']), float(client['lon'])
                )
            }
            return config
        except ValueError as e:
            raise SpeedtestConfigError(
                f'Unknown loc: lat={client.get("lat")} lon={client.get("lon")}'
            ) from e
