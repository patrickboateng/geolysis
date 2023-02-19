import functools
import math

import xlwings as xw
import numpy as np


class SoilData:
    """Stores the soil parameters"""

    def __init__(
        self,
        liquid_limit: float,
        plastic_limit: float,
        plasticity_index: float,
        fines: float,
        sand: float,
        gravel: float,
        color: bool = False,
        odor: bool = False,
        d10=None,
        d30=None,
        d60=None,
    ) -> None:
        """Soil Parameters Initializer

        Args:
            liquid_limit (float): Liquid Limit of soil (%)
            plastic_limit (float): Plastic Limit of soil (%)
            plasticity_index (float): Plasticity Index of soil (%)
            fines (float): The amount of fines in the soil sample (%)
            sand (float):  The amount of sand in the soil sample (%)
            gravel (float): The amount of gravel in the soil sample (%)
        """
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit
        self.plasticity_index = plasticity_index
        self.fines = fines
        self.sand = sand
        self.gravel = gravel
        self.color = color
        self.odor = odor
        self.d10 = d10
        self.d30 = d30
        self.d60 = d60

    @functools.cached_property
    def _A_line(self) -> float:
        return 0.73 * (self.liquid_limit - 20)

    @property
    def is_above_A_line(self) -> bool:
        return self.plasticity_index > self._A_line

    @property
    def is_organic(self) -> bool:
        return self.color or self.odor

    @property
    def in_hatched_zone(self) -> bool:
        return math.isclose(self.plasticity_index, self._A_line)

    def percentange_retained_on_200_sieve(self) -> float:
        return self.fines

    def get_aashto_classification(self):
        pass

    def get_unified_classification(self):
        """Unified Classification System

        Args:
            soil_data (SoilData): Soil Sample
        """
        if self.fines < 50:
            # Coarse grained, Run Sieve Analysis
            if self.gravel > self.sand:
                # Gravel
                soil_type = "G"
                return self._check_fines(soil_type)
            else:
                # Sand
                soil_type = "S"
                return self._check_fines(soil_type)
        else:
            # Fine grained, Run Atterberg
            if self.liquid_limit < 50:
                # Low LL
                if self.is_above_A_line and self.plasticity_index > 7:
                    return "CL"

                elif not self.is_above_A_line or self.plasticity_index < 4:
                    if self.is_organic:
                        return "OL"
                    else:
                        return "ML"
                else:
                    return "ML-CL"

            else:
                # High LL
                if self.is_above_A_line:
                    return "CH"
                else:
                    if self.is_organic:
                        return "OH"
                    else:
                        return "MH"

    def _check_fines(self, soil_type):
        if self.fines > 12:
            if self.is_above_A_line:
                return f"{soil_type}C"
            elif self.in_hatched_zone:
                return f"{soil_type}M-{soil_type}C"
            else:
                return f"{soil_type}M"
        elif 5 <= self.fines <= 12:
            return f"{soil_type}W-{soil_type}M, {soil_type}P-{soil_type}M, {soil_type}W-{soil_type}C, {soil_type}P-{soil_type}C"
        else:
            return f"{soil_type}W or {soil_type}P"  # Obtain Cc and Cu


@xw.func
@xw.arg("soil_parameters", np.array, ndim=1)
def unified_classification(soil_parameters) -> str:
    soil = SoilData(*soil_parameters)
    print(soil_parameters)

    return soil.get_unified_classification()


if __name__ == "__main__":
    soil_samples = [
        (34.1, 21.1, 13, 47.88, 37.84, 14.28),
        (27.5, 13.8, 13.7, 54.23, 45.69, 0.08),
        (28.2, 14.6, 13.6, 56.43, 43.47, 0.1),
        (28.5, 15.3, 13.2, 54.1, 45.71, 0.19),
        (17.9, 15.9, 2, 20.99, 54.72, 24.29),
        (15.1, 14.8, 0.27, 27.33, 61.8, 10.88),
        (17.8, 15.5, 2.31, 45.35, 54.31, 0.35),
        (53.5, 20.6, 33, 42.35, 57.3, 0.36),
        (44.1, 27.3, 16.8, 43.21, 55.89, 0.89),
        (37.9, 26.5, 11.3, 35.91, 63.77, 0.32),
        (40.4, 23.3, 17, 37.97, 61.28, 0.75),
    ]

    print(
        SoilData(*(15.1, 14.8, 0.27, 27.33, 61.8, 10.88)).get_unified_classification()
    )
