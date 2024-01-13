"""

:mod:`geolysis`
===============

Open-source geotechnical analysis tool for Python.

Modules
-------

Sub-Packages
------------

Exceptions
----------

"""
from . import bearing_capacity, estimators, soil_classifier, spt
from .constants import (
    CLAY,
    ERROR_TOL,
    GRAVEL,
    HIGH_PLASTICITY,
    LOW_PLASTICITY,
    ORGANIC,
    POORLY_GRADED,
    SAND,
    SILT,
    WELL_GRADED,
    EngineerTypeError,
    GeotechEng,
)

globals().update(GeotechEng.__members__)

__version__ = "0.2.0"
