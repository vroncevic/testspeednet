# -*- coding: UTF-8 -*-

'''
Module
    model.py
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
    Defines class SpeedTestServer with attribute(s) and method(s).
    Defines SQLAlchemy model for available servers.
'''

import sys
from typing import Any, List

try:
    from sqlalchemy import Column, String, Integer, Float, Boolean
    from sqlalchemy.ext.declarative import declarative_base
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

# Declarative base from SQLAlchemy.
Base: Any = declarative_base()


class SpeedTestServer(Base):
    '''
        Defines class SpeedTestServer with attribute(s) and method(s).
        Defines SQLAlchemy model for available servers.

        It defines:

            :attributes:
                | __tablename__ - Table name: speedtest_servers.
                | id - Integer primary key.
                | server_id - A unique identifier for the server.
                | url - The URL for the speed test server.
                | lat - The latitude coordinate of the server.
                | lon - The longitude coordinate of the server.
                | distance - Distance to the server in kilometers.
                | name - The name of the server location or city.
                | country - The full country name.
                | cc - The ISO 3166-1 alpha-2 country code.
                | sponsor - The entity sponsoring the server.
                | preferred - A boolean indicating if the server is preferred.
                | host - The host address of the server.
            :methods:
                | None
    '''

    __tablename__: str = 'speedtest_servers'

    id: Column[int] = Column(Integer, primary_key=True)
    server_id: Column[str] = Column(String, nullable=False)
    url: Column[str] = Column(String, nullable=False)
    lat: Column[float] = Column(Float, nullable=False)
    lon: Column[float] = Column(Float, nullable=False)
    distance: Column[float] = Column(Float, nullable=False)
    name: Column[str] = Column(String, nullable=False)
    country: Column[str] = Column(String, nullable=False)
    cc: Column[str] = Column(String, nullable=False)
    sponsor: Column[str] = Column(String, nullable=False)
    preferred: Column[bool] = Column(Boolean, nullable=False)
    host: Column[str] = Column(String, nullable=False)
