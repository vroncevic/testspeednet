"""..."""

import math
from typing import Tuple


def distance(
    origin: Tuple[float, float], destination: Tuple[float, float]
) -> float:
    """..."""
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
