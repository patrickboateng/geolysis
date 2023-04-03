from typing import Sequence, Union

import numpy as np
import xlwings as xw

from geolab.soil_classifier import soil_classifier


@xw.func
@xw.arg("soil_parameters", np.array, ndim=1, doc="Soil parameters")
@xw.arg("d10", doc="diameter at which 10% of the soil by weight if finer")
@xw.arg("d30", doc="diameter at which 30% of the soil by weight is finer")
@xw.arg("d60", doc="diameter at which 60% of the soil by weight is finer")
@xw.arg("color")
@xw.arg("odor")
def USCS(
    soil_parameters: Sequence,
    d10: Union[float, None] = None,
    d30: Union[float, None] = None,
    d60: Union[float, None] = None,
    color: Union[bool, None] = None,
    odor: Union[bool, None] = None,
) -> str:
    """Determines the classification of the soil based on the **Unified Soil
    Classification System**.

    Args:
        soil_parameters: Soil parameters. The parameters should be arranged in the sequence
                                    `liquid limit`, `plastic limit`, `plasticity index`, `fines`, `sand`, `gravel`
        d10: Diameter at which 10% of the soil by weight is finer. Defaults to None.
        d30: Diameter at which 30% of the soil by weight is finer. Defaults to None.
        d60: Diameter at which 60% of the soil by weight is finer. Defaults to None.
        color: Indicates if soil has color or not.
        odor: Indicates if soil has color or not.
    Returns:
        A `string` representing the classification of the soil
    """
    soil = soil_classifier.Soil(
        *soil_parameters, d10=d10, d30=d30, d60=d60, color=color, odor=odor
    )

    return soil.get_unified_classification()


@xw.func
@xw.arg("soil_parameters", np.array, ndim=1, doc="Soil parameters")
def AASHTO(soil_parameters: Sequence) -> str:
    """Determines the classification of the soil based on the `AASHTO` classification system.

    soil_parameters: Soil parameters. The parameters should be arranged in the sequence
                                    `liquid limit`, `plastic limit`, `plasticity index`, `fines`, `sand`, `gravel`

    Returns:
        A `string` representing the `AASHTO` classification of the soil
    """

    soil = soil_classifier.Soil(*soil_parameters)

    return soil.get_aashto_classification()
