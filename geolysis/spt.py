from abc import abstractmethod
from dataclasses import KW_ONLY, dataclass
from statistics import StatisticsError
from typing import Protocol, Sequence

from geolysis.constants import ERROR_TOL
from geolysis.utils import isclose, log10, mean, round_, sqrt

__all__ = [
    "SPT",
    "EnergyCorrection",
    "GibbsHoltzOPC",
    "BazaraaPeckOPC",
    "PeckOPC",
    "LiaoWhitmanOPC",
    "SkemptonOPC",
    "DilatancyCorrection",
]


class OPCError(ValueError):
    pass


class SPT:
    r"""A class for calculating the design value (:math:`N_{design}`) from a list
    of SPT N-values.

    Parameters
    ----------
    corrected_spt_numbers : Sequence[float]
        SPT N-values within the foundation influence zone. i.e. :math:`D_f`
        to :math:`D_f + 2B`. ``corrected_spt_numbers`` can either be **corrected**
        or **uncorrected**.

    Attributes
    ----------
    corrected_spt_n_vals : Sequence[float]

    Raises
    ------
    StatisticError
        If ``corrected_spt_numbers`` is empty, StatisticError is raised.

    Notes
    -----
    Weighted average is given by the formula:

    .. math::

        N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}{\sum_{i=1}^{n} \frac{1}{i^2}}

    Average is given by the formula:

    .. math::  N_{design} = \dfrac{\sum_{i=1}^{n}N_i}{n}

    Examples
    --------
    >>> from geolysis.spt import SPT
    >>> corrected_spt_numbers = [7.0, 15.0, 18.0]
    >>> spt_avg = SPT(corrected_spt_numbers=corrected_spt_numbers)
    >>> spt_avg.weighted_average()
    9.37
    >>> spt_avg.average()
    13.33
    >>> spt_avg.min()
    7.0

    >>> SPT(corrected_spt_numbers=[])
    Traceback (most recent call last):
        ...
    StatisticsError: corrected_spt_numbers requires at least one SPT N-value
    """

    def __init__(self, corrected_spt_numbers: Sequence[float]) -> None:
        self.corrected_spt_numbers = corrected_spt_numbers

    @property
    def corrected_spt_numbers(self) -> Sequence[float]:
        return self._corrected_spt_numbers

    @corrected_spt_numbers.setter
    def corrected_spt_numbers(self, __val: Sequence[float]):
        if not __val:
            err_msg = "corrected_spt_numbers requires at least one SPT N-value"
            raise StatisticsError(err_msg)
        self._corrected_spt_numbers = __val

    @round_(ndigits=2)
    def weighted_average(self) -> float:
        """Calculates the weighted average of the corrected SPT N-values in the
        foundation influence zone.

        Due to uncertainty in field procedure in standard penetration test and also
        to consider all the N-value in the influence zone of a foundation, a method
        was suggested to calculate the design N-value which should be used in
        calculating the allowable bearing capacity of shallow foundation rather than
        using a particular N-value. All the N-value from the influence zone is taken
        under consideration by giving the highest weightage to the closest N-value
        from the base.
        """

        sum_total = 0.0
        total_wgts = 0.0

        for i, corrected_spt in enumerate(self.corrected_spt_numbers, start=1):
            wgt = 1 / i**2
            sum_total += wgt * corrected_spt
            total_wgts += wgt

        return sum_total / total_wgts

    @round_(ndigits=2)
    def average(self) -> float:
        """Calculates the average of the corrected SPT N-values in the foundation
        influence zone.
        """
        return mean(self.corrected_spt_numbers)

    @round_(ndigits=2)
    def min(self) -> float:
        """For ease in calculation, the lowest N-value from the influence zone can be
        taken as the :math:`N_{design}` as suggested by ``Terzaghi & Peck (1948)``.
        """
        return min(self.corrected_spt_numbers)


class _SPTCorrection(Protocol):
    @property
    @abstractmethod
    def corrected_spt_number(self) -> float: ...


@dataclass
class EnergyCorrection:
    r"""SPT N-value standardized for field procedures.

    On the basis of field observations, it appears reasonable to standardize
    the field SPT N-value as a function of the input driving energy and its
    dissipation around the sampler around the surrounding soil. The variations
    in testing procedures may be at least partially compensated by converting
    the measured N-value to :math:`N_{60}` assuming 60% hammer energy being
    transferred to the tip of the standard split spoon.

    Parameters
    ----------
    recorded_spt_number : int
        Recorded SPT N-value from field.
    energy_percentage : float, default=0.6
        Energy percentage reaching the tip of the sampler.
    hammer_efficiency : float, default=0.6
        Hammer efficiency, defaults to 0.6
    borehole_diameter_correction : float, default=1.0
        Borehole diameter correction
    sampler_correction : float, default=1.0
        Sampler correction
    rod_length_correction : float, default=0.75
        Rod length correction

    Attributes
    ----------
    recorded_spt_number : int
    energy_percentage : float
    hammer_efficiency : float
    borehole_diameter_correction : float
    sampler_correction : float
    rod_length_correction : float

    Notes
    -----
    Energy correction is given by the formula:

    .. math::
        N_{ENERGY} = \dfrac{E_H \cdot C_B \cdot C_S \cdot C_R \cdot N}{ENERGY}

    Examples
    --------
    >>> from geolysis.spt import EnergyCorrection
    >>> energy_cor = EnergyCorrection(recorded_spt_number=30)
    >>> energy_cor.correction
    0.75
    >>> energy_cor.corrected_spt_number
    22.5
    """

    recorded_spt_number: float

    _: KW_ONLY

    energy_percentage = 0.6
    hammer_efficiency = 0.6
    borehole_diameter_correction = 1.0
    sampler_correction = 1.0
    rod_length_correction = 0.75

    @property
    @round_(ndigits=2)
    def correction(self) -> float:
        return (
            self.hammer_efficiency
            * self.borehole_diameter_correction
            * self.sampler_correction
            * self.rod_length_correction
        ) / self.energy_percentage

    @property
    @round_(ndigits=2)
    def corrected_spt_number(self) -> float:
        return self.correction * self.recorded_spt_number


class _OPC(Protocol):
    std_spt_number: float
    eop: float

    @property
    @abstractmethod
    def correction(self) -> float: ...

    @property
    @round_(ndigits=2)
    def corrected_spt_number(self) -> float:
        corrected_spt = self.correction * self.std_spt_number
        return min(corrected_spt, 2 * self.std_spt_number)


@dataclass
class GibbsHoltzOPC(_OPC):
    r"""Overburden Pressure Correction according to ``Gibbs & Holtz (1957)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, unit = :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    std_spt_number : float
    eop : float, unit = :math:`kN/m^2`
    correction : float
    corrected_spt_number : float
    STD_PRESSURE: float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \dfrac{350}{\sigma_o + 70} \, \sigma_o \le 280kN/m^2

    :math:`\dfrac{N_c}{N_{60}}` should lie between 0.45 and 2.0, if :math:`\dfrac{N_c}{N_{60}}`
    is greater than 2.0, :math:`N_c` should be divided by 2.0 to obtain the design value
    used in finding the bearing capacity of the soil.

    Examples
    --------
    >>> from geolysis.spt import GibbsHoltzOPC
    >>> opc_cor = GibbsHoltzOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.correction
    2.06
    >>> opc_cor.corrected_spt_number
    23.18
    """

    #: Maximum effective overburden pressure.
    STD_PRESSURE = 280.0

    def __init__(self, std_spt_number: float, eop: float) -> None:
        self.std_spt_number = std_spt_number
        self.eop = eop

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.std_spt_number=}, {self.eop=})"

    @property
    def eop(self) -> float:
        """Effective overburden pressure."""
        return self._eop

    @eop.setter
    def eop(self, __val: float):
        if __val <= 0:
            err_msg = f"eop = {__val} cannot be less than or equal to 0"
            raise OPCError(err_msg)

        if __val > self.STD_PRESSURE:
            err_msg = f"eop = {__val} should be less than {self.STD_PRESSURE}"
            raise OPCError(err_msg)
        self._eop = __val

    @property
    @round_(ndigits=2)
    def correction(self) -> float:
        return 350.0 / (self.eop + 70)

    @property
    @round_(ndigits=2)
    def corrected_spt_number(self) -> float:
        corrected_spt = self.correction * self.std_spt_number
        spt_ratio = corrected_spt / self.std_spt_number

        if spt_ratio > 2.0:
            corrected_spt /= 2

        return min(corrected_spt, 2 * self.std_spt_number)


@dataclass
class BazaraaPeckOPC(_OPC):
    r"""Overburden Pressure Correction according to ``Bazaraa (1967)``, and also
    by ``Peck and Bazaraa (1969)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, unit = :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    std_spt_number : float
    eop : float, unit = :math:`kN/m^2`
    correction : float
    corrected_spt_number : float
    STD_PRESSURE : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math::

        C_N &= \dfrac{4}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2

        C_N &= \dfrac{4}{3.25 + 0.0104 \cdot \sigma_o}, \, \sigma_o \gt 71.8kN/m^2

        C_N &= 1 \, , \, \sigma_o = 71.8kN/m^2

    Examples
    --------
    >>> from geolysis.spt import BazaraaPeckOPC
    >>> opc_cor = BazaraaPeckOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.correction
    0.93
    >>> opc_cor.corrected_spt_number
    20.93
    """

    std_spt_number: float
    eop: float

    #: Maximum effective overburden pressure.
    STD_PRESSURE = 71.8

    @property
    @round_(ndigits=2)
    def correction(self) -> float:
        if isclose(self.eop, self.STD_PRESSURE, rel_tol=ERROR_TOL):
            correction = 1.0
        elif self.eop < self.STD_PRESSURE:
            correction = 4 / (1 + 0.0418 * self.eop)
        else:
            correction = 4 / (3.25 + 0.0104 * self.eop)

        return correction

    @property
    def corrected_spt_number(self) -> float:
        return super().corrected_spt_number


@dataclass
class PeckOPC(_OPC):
    r"""Overburden Pressure Correction according to ``Peck et al (1974)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, unit = :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    std_spt_number : float
    eop: float, unit = :math:`kN/m^2`
    correction : float
    corrected_spt_number : float
    STD_PRESSURE : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = 0.77 \log \left( \dfrac{2000}{\sigma_o} \right)

    Examples
    --------
    >>> from geolysis.spt import PeckOPC
    >>> opc_cor = PeckOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.correction
    1.0
    >>> opc_cor.corrected_spt_number
    22.5
    """

    #: Maximum effective overburden pressure.
    STD_PRESSURE = 24.0

    def __init__(self, std_spt_number: float, eop: float) -> None:
        self.std_spt_number = std_spt_number
        self.eop = eop

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.std_spt_number=}, {self.eop=})"

    @property
    def eop(self) -> float:
        return self._eop

    @eop.setter
    def eop(self, __val: float):
        if __val < self.STD_PRESSURE:
            err_msg = f"eop = {__val} cannot be less than 24"
            raise OPCError(err_msg)
        self._eop = __val

    @property
    @round_(ndigits=2)
    def correction(self) -> float:
        return 0.77 * log10(2000 / self.eop)

    @property
    def corrected_spt_number(self) -> float:
        return super().corrected_spt_number


@dataclass
class LiaoWhitmanOPC(_OPC):
    r"""Overburden Pressure Correction according to ``Liao & Whitman (1986)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, unit = :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    std_spt_number : float
    eop: float, unit = :math:`kN/m^2`
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \sqrt{\dfrac{100}{\sigma_o}}

    Examples
    --------
    >>> from geolysis.spt import LiaoWhitmanOPC
    >>> opc_cor = LiaoWhitmanOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.correction
    1.0
    >>> opc_cor.corrected_spt_number
    22.5
    """

    def __init__(self, std_spt_number: float, eop: float) -> None:
        self.std_spt_number = std_spt_number
        self.eop = eop

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.std_spt_number=}, {self.eop=})"

    @property
    def eop(self) -> float:
        return self._eop

    @eop.setter
    def eop(self, __val: float):
        if __val <= 0:
            err_msg = f"eop = {__val} cannot be less than or equal to 0"
            raise OPCError(err_msg)
        self._eop = __val

    @property
    @round_(ndigits=2)
    def correction(self) -> float:
        return sqrt(100 / self.eop)

    @property
    def corrected_spt_number(self) -> float:
        return super().corrected_spt_number


@dataclass
class SkemptonOPC(_OPC):
    r"""Overburden Pressure Correction according to ``Skempton (1986)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, unit = :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    std_spt_number : float
    eop: float, unit = :math:`kN/m^2`
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \dfrac{2}{1 + 0.01044 \cdot \sigma_o}

    Examples
    --------
    >>> from geolysis.spt import SkemptonOPC
    >>> opc_cor = SkemptonOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.correction
    0.98
    >>> opc_cor.corrected_spt_number
    22.05
    """

    std_spt_number: float
    eop: float

    @property
    @round_(ndigits=2)
    def correction(self) -> float:
        return 2 / (1 + 0.01044 * self.eop)

    @property
    def corrected_spt_number(self) -> float:
        return super().corrected_spt_number


@dataclass
class DilatancyCorrection:
    r"""Dilatancy SPT Correction according to ``Terzaghi & Peck (1948)``.

    For coarse sand, this correction is not required. In applying this correction,
    overburden pressure correction is applied first and then dilatancy correction
    is applied.

    Parameters
    ----------
    spt_number : float
        SPT N-value standardized for field procedures or corrected for overburden
        pressure.

    Attributes
    ----------
    spt_number : float
    corrected_spt_number : float

    Notes
    -----
    Dilatancy correction is given by the formula:

    .. math::

        (N_1)_{60} &= 15 + \dfrac{1}{2}((N_1)_{60} - 15) \, , \, (N_1)_{60} \gt 15

        (N_1)_{60} &= (N_1)_{60} \, , \, (N_1)_{60} \le 15

    Examples
    --------
    >>> from geolysis.spt import DilatancyCorrection
    >>> dil_cor = DilatancyCorrection(spt_number=22.5)
    >>> dil_cor.corrected_spt_number
    18.75
    """

    spt_number: float

    @property
    @round_(ndigits=2)
    def corrected_spt_number(self) -> float:
        if self.spt_number <= 15:
            return self.spt_number

        return 15 + 0.5 * (self.spt_number - 15)
