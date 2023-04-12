from typing import Union
from collections import namedtuple

import xlwings as xw
from xlwings import conversion

from geolab.soil_classifier import soil_classifier


SoilParams = namedtuple(
    typename="SoilParams",
    field_names="liquid_limit plastic_limit plasticity_index fines sand gravels",
)


class SoilConverter(conversion.Converter):
    @staticmethod
    def read_value(value, options):
        soil_parameters = SoilParams(*value)
        return soil_parameters


@xw.func
@xw.arg("soil_parameters", SoilConverter, doc="Soil parameters")
@xw.arg("d10", doc="diameter at which 10% of the soil by weight if finer")
@xw.arg("d30", doc="diameter at which 30% of the soil by weight is finer")
@xw.arg("d60", doc="diameter at which 60% of the soil by weight is finer")
@xw.arg("color")
@xw.arg("odor")
def USCS(
    soil_parameters: SoilParams,
    d10: Union[float, None] = None,
    d30: Union[float, None] = None,
    d60: Union[float, None] = None,
    color: Union[bool, None] = None,
    odor: Union[bool, None] = None,
) -> str:
    """Determines the classification of the soil based on the `Unified Soil
    Classification System`.

    Args:
        soil_parameters: Parameters of the Soil.
        d10: Diameter at which 10% of the soil by weight is finer. Defaults to None.
        d30: Diameter at which 30% of the soil by weight is finer. Defaults to None.
        d60: Diameter at which 60% of the soil by weight is finer. Defaults to None.
        color: Indicates if soil has color or not.
        odor: Indicates if soil has color or not.
    Returns:
        A `string` representing the classification of the soil
    """
    soil = soil_classifier.Soil(
        liquid_limit=soil_parameters.liquid_limit,
        plastic_limit=soil_parameters.plastic_limit,
        plasticity_index=soil_parameters.plasticity_index,
        fines=soil_parameters.fines,
        sand=soil_parameters.sand,
        gravels=soil_parameters.gravels,
        d10=d10,
        d30=d30,
        d60=d60,
        color=color,
        odor=odor,
    )

    return soil.get_unified_classification()


@xw.func
@xw.arg("soil_parameters", SoilConverter, doc="Soil parameters")
def AASHTO(soil_parameters: SoilParams) -> str:
    """Determines the classification of the soil based on the `AASHTO` classification system.

    soil_parameters: Parameters of the soil.

    Returns:
        A `string` representing the `AASHTO` classification of the soil
    """
    soil = soil_classifier.Soil(
        liquid_limit=soil_parameters.liquid_limit,
        plastic_limit=soil_parameters.plastic_limit,
        plasticity_index=soil_parameters.plasticity_index,
        fines=soil_parameters.fines,
        sand=soil_parameters.sand,
        gravels=soil_parameters.gravels,
    )

    return soil.get_aashto_classification()
