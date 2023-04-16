import functools
from typing import Union
from collections import namedtuple

import xlwings as xw
from xlwings import conversion

from geolab.soil_classifier import Soil
from geolab import PIValueError, PSDValueError


SoilParams = namedtuple(
    typename="SoilParams",
    field_names="liquid_limit plastic_limit plasticity_index fines sand gravels",
)


class SoilConverter(conversion.Converter):
    @staticmethod
    def read_value(value, options):
        soil_parameters = SoilParams(*value)
        return soil_parameters


@functools.lru_cache
@xw.func
@xw.arg("soil_parameters", SoilConverter, doc="Soil parameters")
@xw.arg("d10", doc=r"diameter at which 10% of the soil by weight is finer")
@xw.arg("d30", doc=r"diameter at which 30% of the soil by weight is finer")
@xw.arg("d60", doc=r"diameter at which 60% of the soil by weight is finer")
@xw.arg("color")
@xw.arg("odor")
def USCS(
    soil_parameters: SoilParams,
    d10: Union[float, None] = None,
    d30: Union[float, None] = None,
    d60: Union[float, None] = None,
    color: bool = False,
    odor: bool = False,
) -> str:
    """Determines the classification of the soil based on USCS.

    Returns:
         A string representing the classification of the soil.
    """
    try:
        soil = Soil(*soil_parameters, d10=d10, d30=d30, d60=d60, color=color, odor=odor)
    except PIValueError as e:
        return str(e)
    except PSDValueError as e:
        return str(e)

    return soil.unified_classification


@functools.lru_cache
@xw.func
@xw.arg("soil_parameters", SoilConverter, doc="Soil parameters")
def AASHTO(soil_parameters: SoilParams) -> str:
    """Determines the classification of the soil based on the AASHTO.

    Returns:
        A string representing the classification of a model.
    """
    try:
        soil = Soil(*soil_parameters)
    except PIValueError as e:
        return str(e)
    except PSDValueError as e:
        return str(e)

    return soil.aashto_classification
