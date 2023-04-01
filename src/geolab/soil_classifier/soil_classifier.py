import functools
import math

from geolab import PSDValueError, PIValueError


def check_PSD(fines: float, sand: float, gravels: float):
    """Checks if `fines + sand + gravels = 100%`.

    Args:
        fines (float): Percentage of fines in  soil sample.
        sand (float): Percentage of sand in soil sample.
        gravel (float): Percentage of gravels in soil sample.

    Raises:
        PSDValueError: `fines + sand + gravels != 100%`.
    """
    total_aggregate = fines + sand + gravels
    if not math.isclose(total_aggregate, 100):
        raise PSDValueError("fines + sand + gravels = 100%")


def check_PI(liquid_limit: float, plastic_limit: float, plasticity_index: float):
    """Checks if `PI = LL - PL`

    Args:
        liquid_limit (float): Water content beyond which soils flows under their own weight.
        plastic_limit (float): Water content at which plastic deformation can be initiated.
        plasticity_index (float): Range of water content over which soil remains in plastic
                                  condition `PI = LL - PL`

    Raises:
        PIValueError: `LL - PL != PI`
    """
    if not math.isclose(liquid_limit - plastic_limit, plasticity_index):
        raise PIValueError("Liquid limit - Plastic limit != Plasticity Index")


class Soil:
    """Stores the soil parameters.

    Args:
        liquid_limit (float): Water content beyond which soils flows under their own weight. (%)
        plastic_limit (float): Water content at which plastic deformation can be initiated. (%)
        plasticity_index (float): Range of water content over which soil remains in plastic
                                  condition `PI = LL - PL` (%)
        fines (float): Percentage of fines in soil sample.
        sand (float):  Percentage of sand in soil sample.
        gravel (float): Percentage of gravels in soil sample.
        d10 (float): diameter at which 10% of the soil by weight is finer.
        d30 (float): diameter at which 30% of the soil by weight is finer.
        d60 (float): diameter at which 60% of the soil by weight is finer.
        color (bool): Indicates if soil has color or not.
        odor (bool): Indicates if soil has odor or not.

    Raises:
        PSDValueError: `fines + sand + gravels != 100%`.
        PIValueError: `LL - PL != PI`

    """

    def __init__(
        self,
        liquid_limit: float,
        plastic_limit: float,
        plasticity_index: float,
        fines: float,
        sand: float,
        gravel: float,
        d10=None,
        d30=None,
        d60=None,
        color: bool = False,
        odor: bool = False,
    ) -> None:
        self.liquid_limit = liquid_limit
        self.plastic_limit = plastic_limit
        self.plasticity_index = plasticity_index
        self.fines = fines
        self.sand = sand
        self.gravel = gravel
        self.d10 = d10
        self.d30 = d30
        self.d60 = d60
        self.color = color
        self.odor = odor

        check_PI(self.liquid_limit, self.plastic_limit, self.plasticity_index)
        check_PSD(self.fines, self.sand, self.gravel)

    @functools.cached_property
    def _A_line(self) -> float:
        return 0.73 * (self.liquid_limit - 20)

    @property
    def cc(self) -> float:
        """Calculates the coefficient of curvature of the soil."""
        return math.pow(self.d30, 2) / (self.d60 * self.d10)

    @property
    def cu(self) -> float:
        """Calculates the coefficient of uniformity of the soil."""
        return self.d60 / self.d10

    @property
    def is_above_A_line(self) -> bool:
        return self.plasticity_index > self._A_line

    @property
    def is_organic(self) -> bool:
        return self.color or self.odor

    @property
    def in_hatched_zone(self) -> bool:
        return math.isclose(self.plasticity_index, self._A_line)

    def percentage_retained_on_200_sieve(self) -> float:
        return self.fines

    @property
    def group_index(self):
        """The `Group Index (GI)` is used to further evaluate soils with a group (subgroups).

        Formula:
            $$ GI = (F_200 - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_200 - 15)(PI - 10) $$
        """

        gi = (self.fines - 35) * (0.2 + 0.005 * (self.liquid_limit - 40)) + 0.01 * (
            self.fines - 15
        ) * (self.plasticity_index - 10)

        return 0.0 if gi <= 0 else gi

    def get_aashto_classification(self) -> str:
        if self.fines <= 35:
            # Gravels A1-A3
            if self.fines <= 10:
                return f"A-3({self.group_index})"

            elif self.fines <= 15:
                return f"A-1-a({self.group_index})"

            elif self.fines <= 25:
                return f"A-1-b({self.group_index})"

            else:
                if self.liquid_limit <= 40:
                    return (
                        f"A-2-4({self.group_index})"
                        if self.plasticity_index <= 10
                        else f"A-2-6({self.group_index})"
                    )

                else:
                    return (
                        f"A-2-5({self.group_index})"
                        if self.plasticity_index <= 10
                        else f"A-2-7({self.group_index})"
                    )

        else:
            # Silts A4-A7
            if self.liquid_limit <= 40:
                return (
                    f"A-4({self.group_index:.0f})"
                    if self.plasticity_index <= 10
                    else f"A-6({self.group_index:.0f})"
                )

            else:
                if self.plasticity_index <= 10:
                    return f"A-5({self.group_index:.0f})"
                else:
                    return (
                        f"A-7-5({self.group_index:.0f})"
                        if self.plasticity_index <= (self.liquid_limit - 30)
                        else f"A-7-6({self.group_index:.0f})"
                    )

    def get_unified_classification(self) -> str:
        """Unified Soil Classification System."""
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

    def get_gravel_grading(self):
        return "W" if (1 < self.cc < 3) and self.cu >= 4 else "P"

    def get_sand_grading(self):
        return "W" if (1 < self.cc < 3) and self.cu >= 6 else "P"

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
            if self.d10 and self.d30 and self.d60:
                if soil_type == "G":
                    return f"{soil_type}{self.get_gravel_grading()}"
                return f"{soil_type}{self.get_sand_grading()}"
            return f"{soil_type}W or {soil_type}P"  # Obtain Cc and Cu
