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

import numpy as np

from geolab.utils import deg2rad

from .exceptions import PIValueError, PSDValueError

__version__ = "0.1.0"
ERROR_TOLERANCE = 0.01
DECIMAL_PLACES = 2


@deg2rad
def passive_earth_pressure_coef(*, friction_angle: float) -> float:
    r"""Coefficient of passive earth pressure :math:`K_p`.

    .. math::

        \dfrac{1 + \sin \phi}{1 - \sin \phi}

    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    :return: Passive earth pressure coefficient
    :rtype: float
    """
    kp = (1 + np.sin(friction_angle)) / (1 - np.sin(friction_angle))
    return round(kp, DECIMAL_PLACES)
