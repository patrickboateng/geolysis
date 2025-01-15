from typing import TypedDict

from . import foundation, soil_classifier, spt, utils

__version__ = "0.4.2"

class SoilProperties(TypedDict, total=False):
    """ Soil properties required for calculations."""
    friction_angle: float
    cohesion: float
    moist_unit_wgt: float

