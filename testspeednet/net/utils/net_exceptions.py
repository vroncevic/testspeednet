# -*- coding: UTF-8 -*-

'''
Module
    net_exceptions.py
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
    Defines class exceptions.
'''


class SpeedtestException(Exception):
    '''Base exception for this module.'''


class SpeedtestCLIError(SpeedtestException):
    '''Generic exception for raising errors during CLI operation.'''


class SpeedtestHTTPError(SpeedtestException):
    '''Base HTTP exception for this module.'''


class SpeedtestConfigError(SpeedtestException):
    '''Configuration XML is invalid.'''


class SpeedtestServersError(SpeedtestException):
    '''Servers XML is invalid.'''


class ConfigRetrievalError(SpeedtestHTTPError):
    '''Could not retrieve config.php.'''


class ServersRetrievalError(SpeedtestHTTPError):
    '''Could not retrieve speedtest-servers.php.'''


class InvalidServerIDType(SpeedtestException):
    '''Server ID used for filtering was not an integer.'''


class NoMatchedServers(SpeedtestException):
    '''No servers matched when filtering.'''


class SpeedtestMiniConnectFailure(SpeedtestException):
    '''Could not connect to the provided speedtest mini server.'''


class InvalidSpeedtestMiniServer(SpeedtestException):
    '''
        Server provided as a speedtest mini server does not actually appear
        to be a speedtest mini server.
    '''


class ShareResultsConnectFailure(SpeedtestException):
    '''Could not connect to speedtest.net API to POST results.'''


class ShareResultsSubmitFailure(SpeedtestException):
    '''
        Unable to successfully POST results to speedtest.net
        API after connection.
    '''


class SpeedtestUploadTimeout(SpeedtestException):
    '''
        Test length configuration reached during upload.
        Used to ensure the upload halts when no additional
        data should be sent.
    '''


class SpeedtestBestServerFailure(SpeedtestException):
    '''Unable to determine best server.'''


class SpeedtestMissingBestServer(SpeedtestException):
    '''get_best_server not called or not able to determine best server.'''
