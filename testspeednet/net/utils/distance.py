# -*- coding: UTF-8 -*-

'''
Module
    distance.py
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
    Defines function distance.
    Calculates the great-circle distance between two points
    on the Earth's surface.
'''

import math
from typing import Tuple, List

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/testspeednet'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/testspeednet/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def distance(
    origin: Tuple[float, float], destination: Tuple[float, float]
) -> float:
    '''
        Calculates the great-circle distance between two points
        on the Earth's surface.

        :param origin: Coordinates of the origin point (lat, lon)
        :type origin: <Tuple[float, float]>
        :param destination: Coordinates of the destination point (lat, lon)
        :type destination: <Tuple[float, float]>
        :return: Distance between the two points in kilometers
        :rtype: <float>
        :exceptions: None
    '''
    lat1: float = 0
    lat2: float = 0
    lon1: float = 0
    lon2: float = 0
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km
    dlat: float = math.radians(lat2 - lat1)
    dlon: float = math.radians(lon2 - lon1)
    a: float = (
        math.sin(dlat / 2) * math.sin(dlat / 2) +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) *
        math.sin(dlon / 2)
    )
    c: float = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d: float = radius * c
    return d
