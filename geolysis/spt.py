import enum
from abc import ABC, abstractmethod
from typing import Annotated, Final, Optional, Sequence

from func_validator import (
    DependsOn,
    MustBeBetween,
    MustBeGreaterThanOrEqual,
    MustBeMemberOf,
    MustBeNonNegative,
    MustBePositive,
    MustHaveLengthGreaterThan,
    MustHaveValuesBetween,
    validate_params,
)

from .foundation import Foundation
from .utils import AbstractStrEnum, isclose, isinf, log10, mean, round_, sqrt

__all__ = [
    "SPT",
    "HammerType",
    "SamplerType",
    "EnergyCorrection",
    "GibbsHoltzOPC",
    "BazaraaPeckOPC",
    "PeckOPC",
    "LiaoWhitmanOPC",
    "SkemptonOPC",
    "DilatancyCorrection",
    "DilatancyCorrection2",
    "OPCType",
    "create_overburden_pressure_correction",
    "correct_spt_n_value",
]


class SPTDesignMethod(AbstractStrEnum):
    """Enumeration of Standard Penetration Test (SPT) design methods.

    Each member represents a different method for interpreting SPT
    results in geotechnical design calculations.
    """

    MINIMUM = "min"
    """Use the minimum SPT value."""

    AVERAGE = "avg"
    """Use the average SPT value."""

    WEIGHTED = "wgt"
    """Use the weighted SPT value."""


class SPT:
    """SPT Design Calculations.

    Due to uncertainty in field procedure in standard penetration test
    and also to consider all the N-value in the influence zone of a
    foundation, a method was suggested to calculate the design N-value
    which should be used in calculating the allowable bearing capacity
    of shallow foundation rather than using a particular N-value. All
    the N-value from the influence zone is taken under consideration by
    giving the highest weightage to the closest N-value from the base.
    """

    def __init__(
        self,
        corrected_spt_n_values: Sequence[float],
        method: SPTDesignMethod = "wgt",
    ):
        """
        :param corrected_spt_n_values: Corrected SPT N-values within the
                                       foundation influence zone.
        """
        self.corrected_spt_n_values = corrected_spt_n_values
        self.method = method

    @property
    def corrected_spt_n_values(self) -> Sequence[float]:
        """
        Corrected SPT N-values within the foundation influence zone.
        """
        return self._corrected_spt_n_values

    @corrected_spt_n_values.setter
    @validate_params
    def corrected_spt_n_values(
        self,
        corrected_spt_n_values: Annotated[
            Sequence[float],
            MustHaveLengthGreaterThan(1),
            MustHaveValuesBetween(min_value=1.0, max_value=100.0),
        ],
    ) -> None:
        self._corrected_spt_n_values = corrected_spt_n_values

    @property
    def method(self):
        return self._method

    @method.setter
    @validate_params
    def method(self, method: Annotated[str, MustBeMemberOf(SPTDesignMethod)]):
        self._method = method

    @staticmethod
    def _avg_spt_n_design(vals) -> float:
        return mean(vals)

    @staticmethod
    def _min_spt_n_design(vals):
        return min(vals)

    @staticmethod
    def _wgt_spt_n_design(vals):

        total_wgted_spt = 0.0
        total_wgt = 0.0

        for i, corr_spt_n_val in enumerate(vals, start=1):
            wgt = 1 / i**2
            total_wgted_spt += wgt * corr_spt_n_val
            total_wgt += wgt

        return total_wgted_spt / total_wgt

    @round_(ndigits=1)
    def n_design(self):
        r"""Calculates the SPT N-design within the foundation influence
        zone.

        If `method="min"`, it returns the minimum N-value within the
        foundation influence zone as the SPT N-design value. This
        approach was suggested by `Terzaghi & Peck (1948)`.

        if `method="avg"`, it returns the average N-value within the
        foundation influence zone as the SPT N-design value.

        if `method="wgt"`, it returns the weighted average N-value
        within the foundation influence zone as the SPT N-design value.

        $$
        N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}
                      {\sum_{i=1}^{n}\frac{1}{i^2}}
        $$
        """
        if self.method == "min":
            _n_design = self._min_spt_n_design
        elif self.method == "avg":
            _n_design = self._avg_spt_n_design
        else:
            _n_design = self._wgt_spt_n_design

        return _n_design(self.corrected_spt_n_values)


class HammerType(AbstractStrEnum):
    """Enumeration of hammer types used in geotechnical testing.

    Each member represents a different type of hammer used for
    Standard Penetration Test (SPT) or other soil testing methods.
    """

    AUTOMATIC = enum.auto()
    """Automatic hammer."""

    DONUT_1 = enum.auto()
    """Donut-type hammer, variant 1."""

    DONUT_2 = enum.auto()
    """Donut-type hammer, variant 2."""

    SAFETY = enum.auto()
    """Safety hammer."""

    DROP = enum.auto()
    """Drop hammer."""

    PIN = enum.auto()
    """Pin-type hammer."""


class SamplerType(AbstractStrEnum):
    """Enumeration of soil sampler types.

    Each member represents a different type of sampler used in
    Standard Penetration Tests (SPT) or other geotechnical sampling
    methods.
    """

    STANDARD = enum.auto()
    """Standard sampler."""

    NON_STANDARD = enum.auto()
    """Non-standard sampler."""

    LINER_4_DENSE_SAND_AND_CLAY = enum.auto()
    """Liner sampler for dense sand and clay."""

    LINER_4_LOOSE_SAND = enum.auto()
    """Liner sampler for loose sand."""


class EnergyCorrection:
    r"""SPT N-value standardized for field procedures.

    On the basis of field observations, it appears reasonable to
    standardize the field SPT N-value as a function of the input driving
    energy and its dissipation around the sampler around the surrounding
    soil. The variations in testing procedures may be at least partially
    compensated by converting the measured N-value to $N_{60}$
    assuming 60% hammer energy being transferred to the tip of the
    standard split spoon.
    """

    _HAMMER_EFFICIENCY_FACTORS = {
        HammerType.AUTOMATIC: 0.70,
        HammerType.DONUT_1: 0.60,
        HammerType.DONUT_2: 0.50,
        HammerType.SAFETY: 0.55,
        HammerType.DROP: 0.45,
        HammerType.PIN: 0.45,
    }

    _SAMPLER_CORRECTION_FACTORS = {
        SamplerType.STANDARD: 1.00,
        SamplerType.NON_STANDARD: 1.20,
        SamplerType.LINER_4_DENSE_SAND_AND_CLAY: 0.8,
        SamplerType.LINER_4_LOOSE_SAND: 0.9,
    }

    def __init__(
        self,
        recorded_spt_n_value: int,
        *,
        energy_percentage=0.6,
        borehole_diameter=65.0,
        rod_length=3.0,
        hammer_type=HammerType.DONUT_1,
        sampler_type=SamplerType.STANDARD,
    ):
        """
        :param recorded_spt_n_value: Recorded SPT N-value from field.

        :param energy_percentage: Energy percentage reaching the tip of
                                  the sampler.
        :param borehole_diameter: Borehole diameter (mm).
        :param rod_length: Length of SPT rod, defaults to 3.0 (m).
        :param hammer_type: Hammer type.
        :param sampler_type: Sampler type.
        """
        self.recorded_spt_n_value = int(recorded_spt_n_value)
        self.energy_percentage = energy_percentage
        self.borehole_diameter = borehole_diameter
        self.rod_length = rod_length
        self.hammer_type = hammer_type
        self.sampler_type = sampler_type

    @property
    def recorded_spt_n_value(self) -> int:
        """Recorded SPT N-value from field."""
        return self._recorded_spt_value

    @recorded_spt_n_value.setter
    @validate_params
    def recorded_spt_n_value(
        self,
        recorded_spt_n_value: Annotated[int, MustBeBetween(min_value=0, max_value=100)],
    ) -> None:
        self._recorded_spt_value = recorded_spt_n_value

    @property
    def energy_percentage(self) -> float:
        """Energy percentage reaching the tip of the sampler."""
        return self._energy_percentage

    @energy_percentage.setter
    @validate_params
    def energy_percentage(
        self,
        energy_percentage: Annotated[
            float, MustBeBetween(min_value=0.0, max_value=1.0)
        ],
    ) -> None:
        self._energy_percentage = energy_percentage

    @property
    def borehole_diameter(self) -> float:
        """Borehole diameter (mm)."""
        return self._borehole_diameter

    @borehole_diameter.setter
    @validate_params
    def borehole_diameter(
        self,
        borehole_diameter: Annotated[
            float, MustBeBetween(min_value=65.0, max_value=200.0)
        ],
    ) -> None:
        self._borehole_diameter = borehole_diameter

    @property
    def rod_length(self) -> float:
        """Length of SPT rod."""
        return self._rod_length

    @rod_length.setter
    @validate_params
    def rod_length(self, rod_length: Annotated[float, MustBePositive()]):
        self._rod_length = rod_length

    @property
    def hammer_type(self) -> HammerType:
        return self._hammer_type

    @hammer_type.setter
    @validate_params
    def hammer_type(
        self,
        hammer_type: Annotated[HammerType, MustBeMemberOf(HammerType)],
    ):
        self._hammer_type = hammer_type

    @property
    def sampler_type(self) -> SamplerType:
        return self._sampler_type

    @sampler_type.setter
    @validate_params
    def sampler_type(
        self, sampler_type: Annotated[SamplerType, MustBeMemberOf(SamplerType)]
    ):
        self._sampler_type = sampler_type

    @property
    def hammer_efficiency(self) -> float:
        """Hammer efficiency correction factor."""
        return self._HAMMER_EFFICIENCY_FACTORS[self.hammer_type]

    @property
    def borehole_diameter_correction(self) -> float:
        """Borehole diameter correction factor."""
        if 65 <= self.borehole_diameter <= 115:
            corr = 1.00
        elif 115 < self.borehole_diameter <= 150:
            corr = 1.05
        else:
            corr = 1.15
        return corr

    @property
    def sampler_correction(self) -> float:
        """Sampler correction factor."""
        return self._SAMPLER_CORRECTION_FACTORS[self.sampler_type]

    @property
    def rod_length_correction(self) -> float:
        """Rod length correction factor."""
        if 3.0 <= self.rod_length <= 4.0:
            corr = 0.75
        elif 4.0 < self.rod_length <= 6.0:
            corr = 0.85
        elif 6.0 < self.rod_length <= 10.0:
            corr = 0.95
        else:
            corr = 1.00
        return corr

    def correction(self) -> float:
        r"""Energy correction factor.

        $$
        N_{ENERGY} = \dfrac{E_H \cdot C_B \cdot C_S
                     \cdot C_R \cdot N}{ENERGY}
        $$

        `ENERGY`: 0.6, 0.55, etc
        """
        numerator = (
            self.hammer_efficiency
            * self.borehole_diameter_correction
            * self.sampler_correction
            * self.rod_length_correction
        )
        return numerator / self.energy_percentage

    @round_(ndigits=1)
    def standardized_spt_n_value(self) -> float:
        """Standardized SPT N-value."""
        return self.correction() * self.recorded_spt_n_value


class OPC(ABC):
    """Base class for Overburden Pressure Correction (OPC)."""

    def __init__(self, std_spt_n_value: float, eop: float):
        """
        :param std_spt_n_value: SPT N-value standardized for field
                                procedures.
        :param eop: Effective overburden pressure ($kPa$).
        """
        self.std_spt_n_value = std_spt_n_value
        self.eop = eop

    @property
    def eop(self) -> float:
        """Effective overburden pressure ($kPa$)."""
        return self._eop

    @eop.setter
    @validate_params
    def eop(self, eop: Annotated[float, MustBeNonNegative()]):
        """Effective overburden pressure ($kPa$)."""
        self._eop = eop

    @property
    def std_spt_n_value(self) -> float:
        """SPT N-value standardized for field procedures."""
        return self._std_spt_n_value

    @std_spt_n_value.setter
    @validate_params
    def std_spt_n_value(
        self,
        std_spt_n_value: Annotated[
            float, MustBeBetween(min_value=0.0, max_value=100.0)
        ],
    ):
        self._std_spt_n_value = std_spt_n_value

    @round_(ndigits=1)
    def corrected_spt_n_value(self) -> float:
        r"""Corrected SPT N-value."""
        # Corrected SPT should not be more
        # than 2 times the Standardized SPT
        correction = min(self.correction(), 2.0)
        return correction * self.std_spt_n_value

    @abstractmethod
    def correction(self) -> float:
        raise NotImplementedError


class GibbsHoltzOPC(OPC):
    """Overburden Pressure Correction according to
    `Gibbs & Holtz (1957)`.
    """

    @property
    def eop(self) -> float:
        """Effective overburden pressure ($kPa$)."""
        return self._eop

    @eop.setter
    @validate_params
    def eop(
        self,
        eop: Annotated[float, MustBeBetween(min_value=0.0, max_value=280.0)],
    ):
        self._eop = eop

    def correction(self) -> float:
        r"""SPT Correction."""
        corr = 350.0 / (self.eop + 70.0)
        return corr / 2.0 if corr > 2.0 else corr


class BazaraaPeckOPC(OPC):
    """Overburden Pressure Correction according to `Bazaraa (1967)`, and
    also by `Peck and Bazaraa (1969)`.
    """

    #: Maximum effective overburden pressure (:math:`kPa`).
    STD_PRESSURE: Final = 71.8

    def correction(self) -> float:
        r"""SPT Correction."""
        if isclose(self.eop, self.STD_PRESSURE, rel_tol=0.01):
            corr = 1.0
        elif self.eop < self.STD_PRESSURE:
            corr = 4.0 / (1.0 + 0.0418 * self.eop)
        else:
            corr = 4.0 / (3.25 + 0.0104 * self.eop)
        return corr


class PeckOPC(OPC):
    """Overburden Pressure Correction according to
    `Peck et al. (1974)`.
    """

    @property
    def eop(self) -> float:
        """Effective overburden pressure ($kPa$)."""
        return self._eop

    @eop.setter
    @validate_params
    def eop(self, eop: Annotated[float, MustBeGreaterThanOrEqual(24.0)]):
        self._eop = eop

    def correction(self) -> float:
        r"""SPT Correction."""
        return 0.77 * log10(2000.0 / self.eop)


class LiaoWhitmanOPC(OPC):
    """Overburden Pressure Correction according to
    `Liao & Whitman (1986)`.
    """

    def correction(self) -> float:
        r"""SPT Correction."""
        return sqrt(100.0 / self.eop)


class SkemptonOPC(OPC):
    """Overburden Pressure Correction according to `Skempton (1986)`."""

    def correction(self) -> float:
        r"""SPT Correction."""
        return 2.0 / (1.0 + 0.01044 * self.eop)


class DilatancyCorrection:
    """Dilatancy SPT Correction according to `Terzaghi & Peck (1948)`.

    For coarse sand, this correction is not required. In applying this
    correction, overburden pressure correction is applied first and then
    dilatancy correction is applied.
    """

    def __init__(self, corr_spt_n_value: float):
        """
        :param corr_spt_n_value: SPT N-value standardized for field
                                 procedures and/or corrected for
                                 overburden pressure.
        """
        self.corr_spt_n_value = corr_spt_n_value

    @property
    def corr_spt_n_value(self) -> float:
        """SPT N-value standardized for field procedures and/or corrected
        for overburden pressure.
        """
        return self._corr_spt_n_value

    @corr_spt_n_value.setter
    @validate_params
    def corr_spt_n_value(
        self,
        corr_spt_n_value: Annotated[
            float, MustBeBetween(min_value=0.0, max_value=100.0)
        ],
    ):
        self._corr_spt_n_value = corr_spt_n_value

    @round_(ndigits=1)
    def corrected_spt_n_value(self) -> float:
        r"""Corrected SPT N-value for presence of water."""
        if self.corr_spt_n_value <= 15.0:
            return self.corr_spt_n_value
        return 15.0 + 0.5 * (self.corr_spt_n_value - 15.0)


class DilatancyCorrection2(DilatancyCorrection):
    """Correction factor for groundwater level."""

    def __init__(self, corr_spt_n_value: float, foundation_size: Foundation):
        super().__init__(corr_spt_n_value)
        self.foundation_size = foundation_size

    def correction(self) -> float:
        water_lvl = self.foundation_size.ground_water_level
        f_width = self.foundation_size.width
        f_depth = self.foundation_size.depth
        correction = 1.0

        if not isinf(water_lvl):
            if (d1 := water_lvl - f_depth) <= f_width or water_lvl < f_width:
                correction = 0.5 + (d1 / (2 * (f_depth + f_width)))

        return correction

    def corrected_spt_n_value(self) -> float:
        """Corrected SPT N-value for presence of water."""
        correction = min(self.correction(), 2.0)
        return correction * self.corr_spt_n_value


class OPCType(AbstractStrEnum):
    """Enumeration of overburden pressure correction (OPC) methods.

    Each member represents a method used to correct SPT results
    for the effects of overburden pressure in geotechnical design.
    """

    GIBBS = enum.auto()
    """Gibbs method for overburden pressure correction."""

    BAZARAA = enum.auto()
    """Bazaraa method for overburden pressure correction."""

    PECK = enum.auto()
    """Peck method for overburden pressure correction."""

    LIAO = enum.auto()
    """Liao method for overburden pressure correction."""

    SKEMPTON = enum.auto()
    """Skempton method for overburden pressure correction."""


class DilatancyCorrType(AbstractStrEnum):
    NON_WATER_AWARE = enum.auto()
    WATER_AWARE = enum.auto()


_opc_methods: Final = {
    OPCType.GIBBS: GibbsHoltzOPC,
    OPCType.BAZARAA: BazaraaPeckOPC,
    OPCType.PECK: PeckOPC,
    OPCType.LIAO: LiaoWhitmanOPC,
    OPCType.SKEMPTON: SkemptonOPC,
}


@validate_params
def correct_spt_n_value(
    recorded_spt_n_value: int,
    *,
    eop: float,
    energy_percentage: float = 0.6,
    borehole_diameter: float = 65.0,
    rod_length: float = 3.0,
    hammer_type: HammerType = HammerType.DONUT_1,
    sampler_type: SamplerType = SamplerType.STANDARD,
    opc_method: OPCType = "gibbs",
    dilatancy_corr_method: Annotated[
        Optional[DilatancyCorrType], MustBeMemberOf(DilatancyCorrType)
    ] = None,
    foundation_size: Annotated[
        Foundation,
        DependsOn(dilatancy_corr_method=DilatancyCorrType.WATER_AWARE),
    ] = None,
) -> float:
    """SPT N-value correction for overburden pressure and groundwater
    level.

    :param recorded_spt_n_value: Recorded SPT N-value from field.
    :param eop: Effective overburden pressure ($kPa$).
    :param energy_percentage: Energy percentage reaching the tip of
                              the sampler.
    :param borehole_diameter: Borehole diameter (mm).
    :param rod_length: Length of SPT rod, defaults to 3.0 (m).
    :param hammer_type: Hammer type.
    :param sampler_type: Sampler type.
    :param opc_method: Overburden pressure correction method.
    :param dilatancy_corr_method: Dilatancy correction method.
    :param foundation_size: Foundation size.
    """
    energy_correction = EnergyCorrection(
        recorded_spt_n_value,
        energy_percentage=energy_percentage,
        borehole_diameter=borehole_diameter,
        rod_length=rod_length,
        hammer_type=hammer_type,
        sampler_type=sampler_type,
    )
    std_spt_n_value = energy_correction.standardized_spt_n_value()
    opc_corr = create_overburden_pressure_correction(
        std_spt_n_value=std_spt_n_value, eop=eop, opc_method=opc_method
    )
    corr_spt_n_value = opc_corr.corrected_spt_n_value()

    if dilatancy_corr_method is not None:
        if dilatancy_corr_method == DilatancyCorrType.NON_WATER_AWARE:
            dil_corr = DilatancyCorrection(corr_spt_n_value=corr_spt_n_value)
            corr_spt_n_value = dil_corr.corrected_spt_n_value()
        else:
            dil_corr = DilatancyCorrection2(
                corr_spt_n_value=corr_spt_n_value,
                foundation_size=foundation_size,
            )
            corr_spt_n_value = dil_corr.corrected_spt_n_value()

    return corr_spt_n_value


@validate_params
def create_overburden_pressure_correction(
    std_spt_n_value: float,
    eop: float,
    opc_method: Annotated[OPCType | str, MustBeMemberOf(OPCType)] = "gibbs",
):
    """A factory function that encapsulates the creation of overburden
    pressure correction.

    :param std_spt_n_value: SPT N-value standardized for field
                            procedures.
    :param eop: Effective overburden pressure ($kPa$).
    :param opc_method: Overburden Pressure Correction type to apply.
    """
    opc_method = OPCType(opc_method)
    opc_class = _opc_methods[opc_method]
    opc_corr = opc_class(std_spt_n_value=std_spt_n_value, eop=eop)
    return opc_corr
