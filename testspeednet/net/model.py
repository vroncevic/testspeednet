# -*- coding: UTF-8 -*-

'''
Module
    model.py
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
    Defines class SpeedTestServer with attribute(s) and method(s).
    Defines SQLAlchemy model for available servers.
'''

import sys
from typing import List

try:
    from sqlalchemy import String, Float, Boolean, Integer
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
except ImportError as ats_error_message:  # pragma: no cover
    # Force exit python #######################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')  # pragma: no cover

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__: str = '1.0.3'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class Base(DeclarativeBase):
    '''
        Defines class Base with attribute(s) and method(s).
        Defines SQLAlchemy declarative base class.

        It defines:

            :attributes:
                | None
            :methods:
                | None
    '''


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    server_id: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    distance: Mapped[float] = mapped_column(Float, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    cc: Mapped[str] = mapped_column(String(2), nullable=False)
    sponsor: Mapped[str] = mapped_column(String(255), nullable=False)
    preferred: Mapped[bool] = mapped_column(Boolean, nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        '''
            String representation of SpeedTestServer instance.

            :return: String representation of the SpeedTestServer instance.
            :rtype: <str>
            :exceptions: None
        '''
        return (
            f"SpeedTestServer(id={self.id!r}, "
            f"server_id={self.server_id!r}, "
            f"name={self.name!r})"
        )
