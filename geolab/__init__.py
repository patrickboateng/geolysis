"""
# geolab

geolab is an open-source software that provides tools for geotechnical engineering,
including soil classification, bearing capacity analysis, estimation of soil engineering properties,
settlement analysis, and finite element modelling. It helps engineers work more efficiently and make
informed decisions about design and construction.

## Soil Parameter Estimators


## Bearing Capacity Analysis


## Exceptions

"""

import numpy as np

from .exceptions import PIValueError, PSDValueError
from geolab.utils import deg2rad

VERSION = "0.1.0"
ERROR_TOLERANCE = 0.01
DECIMAL_PLACES = 2
REFERENCES = {
    "book": {
        "arora": {
            "author_surname": "Arora",
            "author_first_ini": "K",
            "year": 2003,
            "title": "Soil Mechanics and Foundation Engineering",
            "edition": 6,
            "publisher": "Standard Publishers Distributors",
            "place_of_publication": "Delhi",
        }
    }
}


@deg2rad("friction_angle")
def passive_earth_pressure_coef(*, friction_angle: float) -> float:
    r"""Coefficient of passive earth pressure ($K_p$).

    $$\dfrac{1 + \sin \phi}{1 - \sin \phi}$$

    Args:
        friction_angle: Internal angle of friction (degrees).

    Returns:
        Passive earth pressure coefficient.
    """
    return (1 + np.sin(friction_angle)) / (1 - np.sin(friction_angle))
