"""Soil Classifier addin for `Microsoft Excel`."""

from functools import lru_cache
from typing import NamedTuple

import xlwings as xw
from xlwings.conversion import Converter

from exceptions import PIValueError, PSDValueError
from soil_classifier import Soil


class SoilParams(NamedTuple):
    liquid_limit: float
    plastic_limit: float
    plasticity_index: float
    fines: float
    sand: float
    gravels: float


class ParamConverter(Converter):
    """Converts Soil Parameters into a namedtuple."""

    @staticmethod
    def read_value(value, options):
        return SoilParams(*value)


@lru_cache
@xw.func
@xw.arg("soil_parameters", convert=ParamConverter, doc="Soil parameters")
@xw.arg("d10", doc=r"diameter at which 10% of the soil by weight is finer")
@xw.arg("d30", doc=r"diameter at which 30% of the soil by weight is finer")
@xw.arg("d60", doc=r"diameter at which 60% of the soil by weight is finer")
@xw.arg("color")
@xw.arg("odor")
def USCS(
    soil_parameters: SoilParams,
    d10=None,
    d30=None,
    d60=None,
    color=False,
    odor=False,
) -> str:
    """Determine the classification of the soil based on USCS.

    Returns:
          The unified classification of the soil.

    """
    try:
        soil = Soil(
            soil_parameters.liquid_limit,
            soil_parameters.plastic_limit,
            soil_parameters.plasticity_index,
            soil_parameters.fines,
            soil_parameters.sand,
            soil_parameters.gravels,
            d10=d10,
            d30=d30,
            d60=d60,
            color=color,
            odor=odor,
        )
    except PIValueError as error:
        return str(error)
    except PSDValueError as error:
        return str(error)

    return soil.uscs


@lru_cache
@xw.func
@xw.arg("soil_parameters", convert=ParamConverter, doc="Soil parameters")
def AASHTO(soil_parameters: SoilParams) -> str:
    """Determine the classification of the soil based on the AASHTO.

    Returns:
        The AASHTO classification of the soil.

    """
    try:
        soil = Soil(
            soil_parameters.liquid_limit,
            soil_parameters.plastic_limit,
            soil_parameters.plasticity_index,
            soil_parameters.fines,
            soil_parameters.sand,
            soil_parameters.gravels,
        )
    except PIValueError as error:
        return str(error)
    except PSDValueError as error:
        return str(error)

    return soil.aashto
