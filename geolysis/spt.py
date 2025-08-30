"""This module provides classes for performing Standard Penetration Test (SPT)
corrections, including energy, overburden pressure, and dilatancy corrections,
as well as calculating design N-values.
"""

import enum
from abc import abstractmethod
from typing import Annotated, Final, Sequence

from func_validator import (
    validate_func_args,
    MustBeBetween,
    MustBePositive,
    MustBeMemberOf,
    MustBeNonNegative,
    MustBeGreaterThanOrEqual,
    MustHaveLengthGreaterThan,
    MustHaveValuesBetween,
)

from .utils import AbstractStrEnum, isclose, log10, mean, round_, sqrt

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
    "OPCType",
    "create_overburden_pressure_correction",
]


class SPTDesignMethod(AbstractStrEnum):
    """Enumeration of SPT design methods."""

    MIN = enum.auto()
    AVG = enum.auto()
    WGT = enum.auto()


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
        method: SPTDesignMethod.WGT = "wgt",
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
    @validate_func_args
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
    @validate_func_args
    def method(self, val: Annotated[str, MustBeMemberOf(SPTDesignMethod)]):
        self._method = val

    @staticmethod
    def _avg_spt_n_design(vals) -> float:
        return mean(vals)

    @staticmethod
    def _min_spt_n_design(vals):
        return min(vals)

    @staticmethod
    def _wgt_spt_n_design(vals):

        sum_total = 0.0
        sum_wgts = 0.0

        for i, corr_spt_n_val in enumerate(vals, start=1):
            wgt = 1 / i**2
            sum_total += wgt * corr_spt_n_val
            sum_wgts += wgt

        return sum_total / sum_wgts

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
            return self._min_spt_n_design(self.corrected_spt_n_values)
        elif self.method == "avg":
            return self._avg_spt_n_design(self.corrected_spt_n_values)
        else:  # method="wgt"
            return self._wgt_spt_n_design(self.corrected_spt_n_values)


class HammerType(AbstractStrEnum):
    """Enumeration of hammer types."""

    AUTOMATIC = enum.auto()
    DONUT_1 = enum.auto()
    DONUT_2 = enum.auto()
    SAFETY = enum.auto()
    DROP = enum.auto()
    PIN = enum.auto()


class SamplerType(AbstractStrEnum):
    """Enumeration of sampler types."""

    STANDARD = enum.auto()
    NON_STANDARD = enum.auto()


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
    @validate_func_args
    def recorded_spt_n_value(
        self, val: Annotated[int, MustBeBetween(min_value=0, max_value=100)]
    ) -> None:
        self._recorded_spt_value = val

    @property
    def energy_percentage(self) -> float:
        """Energy percentage reaching the tip of the sampler."""
        return self._energy_percentage

    @energy_percentage.setter
    @validate_func_args
    def energy_percentage(
        self, val: Annotated[float, MustBeBetween(min_value=0.0, max_value=1.0)]
    ) -> None:
        self._energy_percentage = val

    @property
    def borehole_diameter(self) -> float:
        """Borehole diameter (mm)."""
        return self._borehole_diameter

    @borehole_diameter.setter
    @validate_func_args
    def borehole_diameter(
        self, val: Annotated[float, MustBeBetween(min_value=65.0, max_value=200.0)]
    ) -> None:
        self._borehole_diameter = val

    @property
    def rod_length(self) -> float:
        """Length of SPT rod."""
        return self._rod_length

    @rod_length.setter
    @validate_func_args
    def rod_length(self, val: Annotated[float, MustBePositive]):
        self._rod_length = val

    @property
    def hammer_type(self) -> HammerType:
        return self._hammer_type

    @hammer_type.setter
    @validate_func_args
    def hammer_type(
        self, hammer_type: Annotated[HammerType, MustBeMemberOf(HammerType)]
    ):
        self._hammer_type = hammer_type

    @property
    def sampler_type(self) -> SamplerType:
        return self._sampler_type

    @sampler_type.setter
    @validate_func_args
    def sampler_type(self, val: Annotated[SamplerType, MustBeMemberOf(SamplerType)]):
        self._sampler_type = val

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
            N_{ENERGY} = \dfrac{E_H \cdot C_B \cdot C_S \cdot C_R \cdot N}{ENERGY}
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


class OPC:
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
    @validate_func_args
    def eop(self, val: Annotated[float, MustBeNonNegative]):
        """Effective overburden pressure ($kPa$)."""
        self._eop = val

    @property
    def std_spt_n_value(self) -> float:
        """SPT N-value standardized for field procedures."""
        return self._std_spt_n_value

    @std_spt_n_value.setter
    @validate_func_args
    def std_spt_n_value(
        self, val: Annotated[float, MustBeBetween(min_value=0.0, max_value=100.0)]
    ):
        self._std_spt_n_value = val

    @round_(ndigits=1)
    def corrected_spt_n_value(self) -> float:
        r"""Corrected SPT N-value.

        $$
        (N_1)_{60} = C_N \cdot N_{60}
        $$

        !!! note

            `60` is used in this case to represent `60%` hammer
             efficiency and can be any percentage of hammer efficiency
             e.g $N_{55}$ for `55%` hammer efficiency.
        """
        corrected_spt = self.correction() * self.std_spt_n_value
        # Corrected SPT should not be more
        # than 2 times the Standardized SPT
        return min(corrected_spt, 2 * self.std_spt_n_value)

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
    @validate_func_args
    def eop(self, val: Annotated[float, MustBeBetween(min_value=0.0, max_value=280.0)]):
        self._eop = val

    def correction(self) -> float:
        r"""SPT Correction.

        $$
        C_N = \dfrac{350}{\sigma_o + 70} \, \sigma_o \le 280kN/m^2
        $$

        $\frac{N_c}{N_{60}}$ should lie between 0.45 and 2.0, if
        $\frac{N_c}{N_{60}}$ is greater than 2.0, :math:`N_c` should be
        divided by 2.0 to obtain the design value used in finding the
        bearing capacity of the soil.
        """
        corr = 350.0 / (self.eop + 70.0)
        return corr / 2.0 if corr > 2.0 else corr


class BazaraaPeckOPC(OPC):
    """Overburden Pressure Correction according to `Bazaraa (1967)`, and
    also by `Peck and Bazaraa (1969)`.
    """

    #: Maximum effective overburden pressure (:math:`kPa`).
    STD_PRESSURE: Final = 71.8

    def correction(self) -> float:
        r"""SPT Correction.

        $$
        C_N = \dfrac{4}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2
        $$

        $$
        C_N = \dfrac{4}{3.25 + 0.0104 \cdot \sigma_o},
               \, \sigma_o \gt 71.8kN/m^2
        $$

        $$
        C_N = 1 \, , \, \sigma_o = 71.8kN/m^2
        $$

        """
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
    @validate_func_args
    def eop(self, val: Annotated[float, MustBeGreaterThanOrEqual(24.0)]):
        self._eop = val

    def correction(self) -> float:
        r"""SPT Correction.

        $$
        C_N = 0.77 \log \left(\dfrac{2000}{\sigma_o} \right)
        $$
        """
        return 0.77 * log10(2000.0 / self.eop)


class LiaoWhitmanOPC(OPC):
    """Overburden Pressure Correction according to
    `Liao & Whitman (1986)`.
    """

    def correction(self) -> float:
        r"""SPT Correction.

        $$
        C_N = \sqrt{\dfrac{100}{\sigma_o}}
        $$
        """
        return sqrt(100.0 / self.eop)


class SkemptonOPC(OPC):
    """Overburden Pressure Correction according to `Skempton (1986)`."""

    def correction(self) -> float:
        r"""SPT Correction.

        $$
        C_N = \dfrac{2}{1 + 0.01044 \cdot \sigma_o}
        $$
        """
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
    @validate_func_args
    def corr_spt_n_value(
        self, val: Annotated[float, MustBeBetween(min_value=0.0, max_value=100.0)]
    ):
        self._corr_spt_n_value = val

    @round_(ndigits=1)
    def corrected_spt_n_value(self) -> float:
        r"""Corrected SPT N-value.

        $$
        (N_1)_{60} = 15 + \dfrac{1}{2}((N_1)_{60} - 15) \, , \,
                     (N_1)_{60} \gt 15
        $$

        $$
        (N_1)_{60} = (N_1)_{60} \, , \, (N_1)_{60} \le 15
        $$

        """
        if self.corr_spt_n_value <= 15.0:
            return self.corr_spt_n_value
        return 15.0 + 0.5 * (self.corr_spt_n_value - 15.0)


class OPCType(AbstractStrEnum):
    """Enumeration of overburden pressure correction types."""

    GIBBS = enum.auto()
    BAZARAA = enum.auto()
    PECK = enum.auto()
    LIAO = enum.auto()
    SKEMPTON = enum.auto()


_opctypes = {
    OPCType.GIBBS: GibbsHoltzOPC,
    OPCType.BAZARAA: BazaraaPeckOPC,
    OPCType.PECK: PeckOPC,
    OPCType.LIAO: LiaoWhitmanOPC,
    OPCType.SKEMPTON: SkemptonOPC,
}


@validate_func_args
def create_overburden_pressure_correction(
    std_spt_n_value: float,
    eop: float,
    opc_type: Annotated[OPCType | str, MustBeMemberOf(OPCType)] = "gibbs",
):
    """A factory function that encapsulates the creation of overburden
    pressure correction.

    :param std_spt_n_value: SPT N-value standardized for field
                            procedures.

    :param eop: Effective overburden pressure ($kPa$).

    :param opc_type: Overburden Pressure Correction type to apply.
    """
    opc_type = OPCType(opc_type)
    opc_class = _opctypes[opc_type]
    opc_corr = opc_class(std_spt_n_value=std_spt_n_value, eop=eop)
    return opc_corr
