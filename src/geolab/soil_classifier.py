import functools
import math
from typing import Union

from attrs import define, field

from geolab import exceptions


def _check_PSD(fines: float, sand: float, gravels: float):
    """Checks if `fines + sand + gravels = 100%`.

    Args:
        fines: Percentage of fines in  soil sample.
        sand: Percentage of sand in soil sample.
        gravels: Percentage of gravels in soil sample.

    Raises:
        exceptions.PSDValueError: `fines + sand + gravels != 100%`.
    """
    total_aggregate = fines + sand + gravels
    if not math.isclose(total_aggregate, 100):
        raise exceptions.PSDValueError("fines + sand + gravels != 100%")


def _check_PI(liquid_limit: float, plastic_limit: float, plasticity_index: float):
    """Checks if `PI = LL - PL`.

    Args:
        liquid_limit: Water content beyond which soils flows under their own weight.
        plastic_limit: Water content at which plastic deformation can be initiated.
        plasticity_index: Range of water content over which soil remains in plastic
                          condition `PI = LL - PL`.

    Raises:
        exceptions.PIValueError: `LL - PL != PI`.
    """
    if not math.isclose(liquid_limit - plastic_limit, plasticity_index):
        raise exceptions.PIValueError("PI != LL - PL")


@define(frozen=True, slots=False)
class Soil:
    """Stores the soil parameters.

    Attributes:
        liquid_limit: Water content beyond which soils flows under their own weight. (%)
        plastic_limit: Water content at which plastic deformation can be initiated. (%)
        plasticity_index: Range of water content over which soil remains in plastic
                                  condition `PI = LL - PL` (%)
        fines: Percentage of fines in soil sample.
        sand:  Percentage of sand in soil sample.
        gravels: Percentage of gravels in soil sample.
        d10: diameter at which 10% of the soil by weight is finer. Defaults to None.
        d30: diameter at which 30% of the soil by weight is finer. Defaults to None.
        d60: diameter at which 60% of the soil by weight is finer. Defaults to None.
        color: Indicates if soil has color or not. Defaults to False.
        odor: Indicates if soil has odor or not. Defaults to False.

    Raises:
        exceptions.PSDValueError: `fines + sand + gravels != 100%`.
        exceptions.PIValueError: `LL - PL != PI`
    """

    liquid_limit: float
    plastic_limit: float
    plasticity_index: float
    fines: float
    sand: float
    gravels: float
    d10: Union[float, None] = field(default=None)
    d30: Union[float, None] = field(default=None)
    d60: Union[float, None] = field(default=None)
    color: bool = field(default=False)
    odor: bool = field(default=False)

    def __attrs_post_init__(self):
        _check_PI(self.liquid_limit, self.plastic_limit, self.plasticity_index)
        _check_PSD(self.fines, self.sand, self.gravels)

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

    @property
    def group_index(self):
        """The `Group Index (GI)` is used to further evaluate soils with a group (subgroups).

        $$ GI = (F_{200} - 35)[0.2 + 0.005(LL - 40)] + 0.01(F_{200} - 15)(PI - 10) $$

        - $F_{200}$: Percentage by mass passing American Sieve No. 200.
        - LL: Liquid Limit (%), expressed as a whole number.
        - PI: Plasticity Index (%), expressed as a whole number.
        """

        gi = (self.fines - 35) * (0.2 + 0.005 * (self.liquid_limit - 40)) + 0.01 * (
            self.fines - 15
        ) * (self.plasticity_index - 10)

        return 0.0 if gi <= 0 else gi

    @property
    def remarks(self):
        ...

    @functools.cached_property
    def _A_line(self) -> float:
        return 0.73 * (self.liquid_limit - 20)

    @functools.cache
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

    @functools.cache
    def get_unified_classification(self) -> str:
        """Unified Soil Classification System."""
        if self.fines < 50:
            # Coarse grained, Run Sieve Analysis
            if self.gravels > self.sand:
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
                    return "OL" if self.is_organic else "ML"

                else:
                    return "ML-CL"

            else:
                # High LL
                if self.is_above_A_line:
                    return "CH"

                else:
                    return "OH" if self.is_organic else "MH"

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
            # Obtain Cc and Cu
            if self.d10 and self.d30 and self.d60:
                return (
                    f"{soil_type}{self.get_gravel_grading()}"
                    if soil_type == "G"
                    else f"{soil_type}{self.get_sand_grading()}"
                )
            return f"{soil_type}W or {soil_type}P"

    def get_gravel_grading(self):
        return "W" if (1 < self.cc < 3) and self.cu >= 4 else "P"

    def get_sand_grading(self):
        return "W" if (1 < self.cc < 3) and self.cu >= 6 else "P"
