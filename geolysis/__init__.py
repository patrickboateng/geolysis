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
from . import bearing_capacity
from .constants import ERROR_TOLERANCE, EngineerTypeError, GeotechEng
from .estimators import (
    CompressionIndexEst,
    SoilFrictionAngleEst,
    SoilUnitWeightEst,
    UndrainedShearStrengthEst,
)
from .soil_classifier import (
    AASHTO,
    AL,
    PSD,
    USCS,
    AASHTOClassification,
    AtterbergLimits,
    ParticleSizeDistribution,
    ParticleSizes,
    UnifiedSoilClassification,
)

globals().update(GeotechEng.__members__)

__version__ = "0.2.0"
