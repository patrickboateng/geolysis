""" Standard penetration test module.

Enums
=====

.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    HammerType
    SamplerType

Classes
=======

.. autosummary::
    :toctree: _autosummary

    SPTDesign
    EnergyCorrection
    GibbsHoltzOPC
    BazaraaPeckOPC
    PeckOPC
    LiaoWhitmanOPC
    SkemptonOPC
    DilatancyCorrection
"""
import enum
from abc import abstractmethod
from typing import Final, Sequence

from geolysis import validators
from geolysis.utils import isclose, log10, mean, round_, sqrt

__all__ = ["SPTNDesign",
           "EnergyCorrection",
           "GibbsHoltzOPC",
           "BazaraaPeckOPC",
           "PeckOPC",
           "LiaoWhitmanOPC",
           "SkemptonOPC",
           "DilatancyCorrection"]


class SPTNDesign:
    """ SPT Design Calculations.

    Due to uncertainty in field procedure in standard penetration test and also
    to consider all the N-value in the influence zone of a foundation, a method
    was suggested to calculate the design N-value which should be used in
    calculating the allowable bearing capacity of shallow foundation rather
    than using a particular N-value. All the N-value from the influence zone is
    taken under consideration by giving the highest weightage to the closest
    N-value from the base.
    """

    def __init__(self, corrected_spt_n_values: Sequence[float]) -> None:
        """
        :param corrected_spt_n_values: Corrected SPT N-values within the
                                       foundation influence zone.
        :type corrected_spt_n_values: Sequence[float]
        """
        self.corrected_spt_n_values = corrected_spt_n_values

    @property
    def corrected_spt_n_values(self) -> Sequence[float]:
        return self._corrected_spt_n_values

    @corrected_spt_n_values.setter
    @validators.min_len(1)
    def corrected_spt_n_values(self, val: Sequence[float]) -> None:
        self._corrected_spt_n_values = val

    @round_(ndigits=1)
    def average_spt_n_design(self) -> float:
        """Calculates the average of the corrected SPT N-values within the
        foundation influence zone.
        """
        return mean(self.corrected_spt_n_values)

    @round_(ndigits=1)
    def minimum_spt_n_design(self):
        """The lowest SPT N-value within the influence zone can be taken as the
        :math:`N_{design}` as suggested by ``Terzaghi & Peck (1948)``.
        """
        return min(self.corrected_spt_n_values)

    @round_(ndigits=1)
    def weighted_spt_n_design(self):
        r"""Calculates the weighted average of the corrected SPT N-values
        within the foundation influence zone.

        Weighted average is given by the formula:

        .. math::

            N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}
                         {\sum_{i=1}^{n}\frac{1}{i^2}}
        """

        sum_total = 0.0
        sum_wgts = 0.0

        for i, corr_spt_n_val in enumerate(self.corrected_spt_n_values,
                                           start=1):
            wgt = 1 / i ** 2
            sum_total += wgt * corr_spt_n_val
            sum_wgts += wgt

        return sum_total / sum_wgts


class HammerType(enum.StrEnum):
    """Enumeration of hammer types."""
    AUTOMATIC = enum.auto()
    DONUT_1 = enum.auto()
    DONUT_2 = enum.auto()
    SAFETY = enum.auto()
    DROP = PIN = enum.auto()


class SamplerType(enum.StrEnum):
    """Enumeration of sampler types."""
    STANDARD = enum.auto()
    NON_STANDARD = enum.auto()


class EnergyCorrection:
    r"""SPT N-value standardized for field procedures.

    On the basis of field observations, it appears reasonable to standardize
    the field SPT N-value as a function of the input driving energy and its
    dissipation around the sampler around the surrounding soil. The variations
    in testing procedures may be at least partially compensated by converting
    the measured N-value to :math:`N_{60}` assuming 60% hammer energy being
    transferred to the tip of the standard split spoon.

    Energy correction is given by the formula:

    .. math::

        N_{ENERGY} = \dfrac{E_H \cdot C_B \cdot C_S \cdot C_R \cdot N}{ENERGY}

    ``ENERGY``: 0.6, 0.55, etc
    """

    #: Hammer efficiency factors
    HAMMER_EFFICIENCY_FACTORS = {HammerType.AUTOMATIC: 0.70,
                                 HammerType.DONUT_1: 0.60,
                                 HammerType.DONUT_2: 0.50,
                                 HammerType.SAFETY: 0.55,
                                 HammerType.DROP: 0.45,
                                 HammerType.PIN: 0.45}

    #: Sampler correction factors
    SAMPLER_CORRECTION_FACTORS = {SamplerType.STANDARD: 1.00,
                                  SamplerType.NON_STANDARD: 1.20}

    def __init__(self, recorded_spt_n_value: int, *,
                 energy_percentage=0.6,
                 borehole_diameter=65.0,
                 rod_length=3.0,
                 hammer_type=HammerType.DONUT_1,
                 sampler_type=SamplerType.STANDARD):
        """
        :param recorded_spt_n_value: Recorded SPT N-value from field.
        :type recorded_spt_n_value: int

        :param energy_percentage: Energy percentage reaching the tip of the 
                                  sampler, defaults to 0.6
        :type energy_percentage: float, optional

        :param borehole_diameter: Borehole diameter, defaults to 65.0. (mm)
        :type borehole_diameter: float, optional

        :param rod_length: Rod length, defaults to 3.0. (m)
        :type rod_length: float, optional

        :param hammer_type: Hammer type, defaults to :attr:`HammerType.DONUT_1`
        :type hammer_type: HammerType, optional

        :param sampler_type: Sampler type, defaults to :attr:`SamplerType.STANDARD`
        :type sampler_type: SamplerType, optional
        """

        self.recorded_spt_n_value = recorded_spt_n_value
        self.energy_percentage = energy_percentage
        self.borehole_diameter = borehole_diameter
        self.rod_length = rod_length
        self.hammer_type = hammer_type
        self.sampler_type = sampler_type

    @property
    def recorded_spt_n_value(self) -> int:
        return self._recorded_spt_value

    @recorded_spt_n_value.setter
    @validators.le(100)
    @validators.gt(0)
    def recorded_spt_n_value(self, val: int) -> None:
        self._recorded_spt_value = val

    @property
    def energy_percentage(self) -> float:
        return self._energy_percentage

    @energy_percentage.setter
    @validators.le(1.0)
    @validators.gt(0.0)
    def energy_percentage(self, val: float) -> None:
        self._energy_percentage = val

    @property
    def borehole_diameter(self) -> float:
        return self._borehole_diameter

    @borehole_diameter.setter
    @validators.le(200.0)
    @validators.ge(65.0)
    def borehole_diameter(self, val: float) -> None:
        self._borehole_diameter = val

    @property
    def rod_length(self) -> float:
        return self._rod_length

    @rod_length.setter
    @validators.gt(0.0)
    def rod_length(self, val: float) -> None:
        self._rod_length = val

    @property
    def hammer_efficiency(self) -> float:
        """Hammer efficiency correction factor."""
        return self.HAMMER_EFFICIENCY_FACTORS[self.hammer_type]

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
        return self.SAMPLER_CORRECTION_FACTORS[self.sampler_type]

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
        """Energy correction factor."""
        numerator = (self.hammer_efficiency
                     * self.borehole_diameter_correction
                     * self.sampler_correction
                     * self.rod_length_correction)
        return numerator / self.energy_percentage

    @round_(ndigits=1)
    def corrected_spt_n_value(self) -> float:
        """Corrected SPT N-value."""
        return self.correction() * self.recorded_spt_n_value


class OPC:
    """Base class for Overburden Pressure Correction (OPC)."""

    def __init__(self, std_spt_n_value: float, eop: float) -> None:
        """
        :param std_spt_n_value: SPT N-value standardized for field procedures.
        :type std_spt_n_value: float

        :param eop: Effective overburden pressure (:math:`kN/m^2`)
        :type eop: float
        """
        self.std_spt_n_value = std_spt_n_value
        self.eop = eop

    @property
    def std_spt_n_value(self) -> float:
        return self._std_spt_n_value

    @std_spt_n_value.setter
    @validators.gt(0.0)
    def std_spt_n_value(self, val: float) -> None:
        self._std_spt_n_value = val

    @round_(ndigits=1)
    def corrected_spt_n_value(self) -> float:
        """Corrected SPT N-value."""
        corrected_spt = self.correction() * self.std_spt_n_value
        # Corrected SPT should not be more 
        # than 2 times the Standardized SPT
        return min(corrected_spt, 2 * self.std_spt_n_value)

    @abstractmethod
    def correction(self) -> float:
        raise NotImplementedError


class GibbsHoltzOPC(OPC):
    r"""Overburden Pressure Correction according to ``Gibbs & Holtz (1957)``.

    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \dfrac{350}{\sigma_o + 70} \, \sigma_o \le 280kN/m^2

    :math:`\frac{N_c}{N_{60}}` should lie between 0.45 and 2.0, if
    :math:`\frac{N_c}{N_{60}}` is greater than 2.0, :math:`N_c` should be
    divided by 2.0 to obtain the design value used in finding the bearing
    capacity of the soil.
    """

    @property
    def eop(self) -> float:
        return self._eop

    @eop.setter
    @validators.le(280.0)
    @validators.gt(0.0)
    def eop(self, val: float) -> None:
        self._eop = val

    def correction(self) -> float:
        """SPT Correction."""
        corr = 350.0 / (self.eop + 70.0)
        return corr / 2.0 if corr > 2.0 else corr


class BazaraaPeckOPC(OPC):
    r"""Overburden Pressure Correction according to ``Bazaraa (1967)``, and
    also by ``Peck and Bazaraa (1969)``.

    Overburden Pressure Correction is given by the formula:

    .. math::

        C_N &= \dfrac{4}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2

        C_N &= \dfrac{4}{3.25 + 0.0104 \cdot \sigma_o}, 
               \, \sigma_o \gt 71.8kN/m^2

        C_N &= 1 \, , \, \sigma_o = 71.8kN/m^2
    """

    #: Maximum effective overburden pressure. (:math:`kN/m^2`)
    STD_PRESSURE: Final = 71.8

    @property
    def eop(self) -> float:
        return self._eop

    @eop.setter
    @validators.ge(0.0)
    def eop(self, val: float) -> None:
        self._eop = val

    def correction(self) -> float:
        """SPT Correction."""
        if isclose(self.eop, self.STD_PRESSURE, rel_tol=0.01):
            corr = 1.0
        elif self.eop < self.STD_PRESSURE:
            corr = 4.0 / (1.0 + 0.0418 * self.eop)
        else:
            corr = 4.0 / (3.25 + 0.0104 * self.eop)
        return corr


class PeckOPC(OPC):
    r"""Overburden Pressure Correction according to ``Peck et al. (1974)``.

    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = 0.77 \log \left(\dfrac{2000}{\sigma_o} \right)
    """

    @property
    def eop(self) -> float:
        return self._eop

    @eop.setter
    @validators.ge(24.0)
    def eop(self, val: float) -> None:
        self._eop = val

    def correction(self) -> float:
        """SPT Correction."""
        return 0.77 * log10(2000.0 / self.eop)


class LiaoWhitmanOPC(OPC):
    r"""Overburden Pressure Correction according to ``Liao & Whitman (1986)``.

    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \sqrt{\dfrac{100}{\sigma_o}}
    """

    @property
    def eop(self) -> float:
        return self._eop

    @eop.setter
    @validators.gt(0.0)
    def eop(self, val: float) -> None:
        self._eop = val

    def correction(self) -> float:
        """SPT Correction."""
        return sqrt(100.0 / self.eop)


class SkemptonOPC(OPC):
    r"""Overburden Pressure Correction according to ``Skempton (1986)``.

    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \dfrac{2}{1 + 0.01044 \cdot \sigma_o}
    """

    @property
    def eop(self) -> float:
        return self._eop

    @eop.setter
    @validators.ge(0.0)
    def eop(self, val: float) -> None:
        self._eop = val

    def correction(self) -> float:
        """SPT Correction."""
        return 2.0 / (1.0 + 0.01044 * self.eop)


class DilatancyCorrection:
    r"""Dilatancy SPT Correction according to ``Terzaghi & Peck (1948)``.

    For coarse sand, this correction is not required. In applying this
    correction, overburden pressure correction is applied first and then
    dilatancy correction is applied.

    Dilatancy correction is given by the formula:

    .. math::

        (N_1)_{60} &= 15 + \dfrac{1}{2}((N_1)_{60} - 15) \, , \,
                      (N_1)_{60} \gt 15

        (N_1)_{60} &= (N_1)_{60} \, , \, (N_1)_{60} \le 15
    """

    def __init__(self, std_spt_n_value: float) -> None:
        """
        :param std_spt_n_value: SPT N-value standardized for field procedures
                                and/or corrected for overburden pressure.
        :type std_spt_n_value: float
        """
        self.std_spt_n_value = std_spt_n_value

    @property
    def std_spt_n_value(self) -> float:
        return self._std_spt_n_value

    @std_spt_n_value.setter
    @validators.gt(0.0)
    def std_spt_n_value(self, val: float) -> None:
        self._std_spt_n_value = val

    @round_(ndigits=1)
    def corrected_spt_n_value(self) -> float:
        """Corrected SPT N-value."""
        if self.std_spt_n_value <= 15.0:
            return self.std_spt_n_value
        return 15.0 + 0.5 * (self.std_spt_n_value - 15.0)
