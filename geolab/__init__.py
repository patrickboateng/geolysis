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

import functools
from typing import Iterable

import numpy as np

from .exceptions import PIValueError, PSDValueError

VERSION = "0.1.0"
ERROR_TOLERANCE = 0.01
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

BOOK_REFERENCES = REFERENCES.get("book")


def deg2rad(*deg: Iterable):
    """A decorator that converts `deg` from degree to radians.

    Args:
        deg: registed keyword arguments to convert.

    Returns:
        A decorator.
    """

    def dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key in deg:
                angle = kwargs[key]
                kwargs[key] = np.deg2rad(angle)
            return func(*args, **kwargs)

        return wrapper

    return dec


@deg2rad("friction_angle")
def foundation_depth(
    allowable_bearing_capacity: float,
    unit_weight_of_soil: float,
    *,
    friction_angle: float,
) -> float:
    r"""Depth of foundation estimated using Rankine's formula.

    $$D_f=\dfrac{Q_{all}}{\gamma}\left(\dfrac{1 - \sin \phi}{1 + \sin \phi}\right)^2$$

    Args:
        allowable_bearing_capacity: Allowable bearing capacity.
        unit_weight_of_soil: Unit weight of soil. ($kN/m^3$)
        friction_angle: Internal angle of friction. (degrees)

    Returns:
        foundation depth.
    """
    first_expr = allowable_bearing_capacity / unit_weight_of_soil
    second_expr = (1 - np.sin(friction_angle)) / (1 + np.sin(friction_angle))

    return first_expr * (second_expr**2)


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


def spt_n60(
    recorded_spt_nvalue: int,
    hammer_efficiency: float = 0.575,
    borehole_diameter_cor: float = 1,
    sampler_cor: float = 1,
    rod_length_cor: float = 0.75,
) -> float:
    r"""SPT N-value corrected for field procedures.

    $$N_{60} = \dfrac{E_m \times C_B \times C_s \times C_R \times N_r}{0.6}$$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        hammer_efficiency: Hammer Efficiency. Defaults to 0.575.
        borehole_diameter_cor: Borehole Diameter Correction. Defaults to 1.
        sampler_cor: Sampler Correction. Defaults to 1.
        rod_length_cor: Rod Length Correction. Defaults to 0.75.

    Returns:
        SPT N-value corrected for 60% hammer efficiency.
    """
    first_expr = (
        hammer_efficiency
        * borehole_diameter_cor
        * sampler_cor
        * rod_length_cor
        * recorded_spt_nvalue
    )

    return first_expr / 0.6
