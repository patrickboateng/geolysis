"""
geolab
======

``geolab`` is an open-source software that provides tools for geotechnical engineering,
including soil classification, bearing capacity analysis, estimation of soil engineering properties,
settlement analysis, and finite element modelling. It helps engineers work more efficiently and make
informed decisions about design and construction.

Soil Parameter Estimators
-------------------------


Bearing Capacity Analysis
-------------------------


Exceptions
----------

"""

import enum

from geolab.utils import deg2rad
from geolab.exceptions import PIValueError, PSDValueError


__version__ = "0.1.0"
ERROR_TOLERANCE = 0.01
DECIMAL_PLACES = 2


class GeotechEng(enum.IntEnum):
    HANSEN = enum.auto()
    HOUGH = enum.auto()
    MEYERHOF = enum.auto()
    SKEMPTON = enum.auto()
    TERZAGHI = enum.auto()
    VESIC = enum.auto()

    def __str__(self) -> str:
        return self.name


globals().update(GeotechEng.__members__)
