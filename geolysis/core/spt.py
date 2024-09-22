from abc import abstractmethod
from dataclasses import KW_ONLY, dataclass, field
from numbers import Number
from typing import Final, Optional, Protocol, Sequence

from geolysis.core.utils import isclose, log10, mean, round_, sqrt

__all__ = [
    "weighted_spt_n_design",
    "average_spt_n_design",
    "minimum_spt_n_design",
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


class SPTCorrection(Protocol):
    @property
    @abstractmethod
    def corrected_spt_number(self) -> float: ...


class OPC(Protocol):
    std_spt_number: float
    eop: float

    @property
    @abstractmethod
    def correction(self) -> float: ...

    @property
    @round_(0)
    def corrected_spt_number(self) -> float:
        """Corrected SPT N-value."""
        corrected_spt = self.correction * self.std_spt_number
        return min(corrected_spt, 2 * self.std_spt_number)


@round_(0)
def weighted_spt_n_design(spt_numbers: Sequence[float]):
    r"""Calculates the weighted average of the corrected SPT N-values within the
    foundation influence zone.

    Due to uncertainty in field procedure in standard penetration test and also
    to consider all the N-value in the influence zone of a foundation, a method
    was suggested to calculate the design N-value which should be used in
    calculating the allowable bearing capacity of shallow foundation rather than
    using a particular N-value. All the N-value from the influence zone is taken
    under consideration by giving the highest weightage to the closest N-value
    from the base.

    Parameters
    ----------
    spt_numbers : Sequence[float]
        SPT N-values within the foundation influence zone. ``spt_numbers`` can
        either be **corrected** or **uncorrected** SPT N-values.

    Notes
    -----
    Weighted average is given by the formula:

    .. math::

        N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}
                      {\sum_{i=1}^{n}\frac{1}{i^2}}

    Examples
    --------
    >>> from geolysis.core.spt import weighted_spt_n_design
    >>> weighted_spt_n_design([7.0, 15.0, 18.0])
    9.0
    """

    sum_total = 0.0
    total_wgts = 0.0

    for i, corrected_spt in enumerate(spt_numbers, start=1):
        wgt = 1 / i**2
        sum_total += wgt * corrected_spt
        total_wgts += wgt

    return sum_total / total_wgts


@round_(0)
def average_spt_n_design(spt_numbers: Sequence[float]):
    r"""Calculates the average of the corrected SPT N-values within the
    foundation influence zone.

    Parameters
    ----------
    spt_numbers : Sequence[float]
        SPT N-values within the foundation influence zone. ``spt_numbers`` can
        either be **corrected** or **uncorrected** SPT N-values.

    Examples
    --------
    >>> from geolysis.core.spt import average_spt_n_design
    >>> average_spt_n_design([7.0, 15.0, 18.0])
    13.0
    """
    return mean(spt_numbers)


@round_(0)
def minimum_spt_n_design(spt_numbers: Sequence[float]):
    """The lowest N-value within the influence zone can be taken as the
    :math:`N_{design}` as suggested by ``Terzaghi & Peck (1948)``.

    Parameters
    ----------
    spt_numbers : Sequence[float]
        SPT N-values within the foundation influence zone. i.e. ``spt_numbers``
        can either be **corrected** or **uncorrected** SPT N-values.

    Examples
    --------
    >>> from geolysis.core.spt import minimum_spt_n_design
    >>> minimum_spt_n_design([7.0, 15.0, 18.0])
    7.0
    """
    return min(spt_numbers)


@dataclass
class EnergyCorrection:
    r"""SPT N-value standardized for field procedures.

    On the basis of field observations, it appears reasonable to standardize the
    field SPT N-value as a function of the input driving energy and its
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
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Energy correction is given by the formula:

    .. math::

        N_{ENERGY} = \dfrac{E_H \cdot C_B \cdot C_S \cdot C_R \cdot N}{ENERGY}

    ``ENERGY``: 0.6, 0.55, etc

    Examples
    --------
    >>> from geolysis.core.spt import EnergyCorrection
    >>> energy_cor = EnergyCorrection(recorded_spt_number=30)
    >>> energy_cor.corrected_spt_number
    22.0
    """

    recorded_spt_number: float

    _: KW_ONLY

    rod_length: Optional[float] = None
    energy_percentage: float = 0.6
    hammer_efficiency: float = 0.6
    borehole_diameter_correction: float = 1.0
    sampler_correction: float = 1.0
    rod_length_correction: float = 0.75

    def __post_init__(self):
        if isinstance(self.rod_length, Number):
            if 3.0 < self.rod_length <= 4.0:
                self.rod_length_correction = 0.75
            elif 4.0 < self.rod_length <= 6.0:
                self.rod_length_correction = 0.85
            elif 6.0 < self.rod_length <= 10.0:
                self.rod_length_correction = 0.95
            else:
                self.rod_length_correction = 1.00

    @property
    def correction(self) -> float:
        """SPT Correction."""
        return (
            self.hammer_efficiency
            * self.borehole_diameter_correction
            * self.sampler_correction
            * self.rod_length_correction
        ) / self.energy_percentage

    @property
    @round_(0)
    def corrected_spt_number(self) -> float:
        """Corrected SPT N-value."""
        return self.correction * self.recorded_spt_number


@dataclass
class GibbsHoltzOPC(OPC):
    r"""Overburden Pressure Correction according to ``Gibbs & Holtz (1957)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \dfrac{350}{\sigma_o + 70} \, \sigma_o \le 280kN/m^2

    :math:`\frac{N_c}{N_{60}}` should lie between 0.45 and 2.0, if
    :math:`\frac{N_c}{N_{60}}` is greater than 2.0, :math:`N_c` should be
    divided by 2.0 to obtain the design value used in finding the bearing
    capacity of the soil.

    Examples
    --------
    >>> from geolysis.core.spt import GibbsHoltzOPC
    >>> opc_cor = GibbsHoltzOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.corrected_spt_number
    23.0
    """

    #: Maximum effective overburden pressure. |rarr| :math:`kN/m^2`
    STD_PRESSURE: Final = 280.0

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
        if __val <= 0 or __val > self.STD_PRESSURE:
            err_msg = f"eop = {__val} cannot be <= 0 or > 280 kPa"
            raise OPCError(err_msg)

        self._eop = __val

    @property
    def correction(self) -> float:
        """SPT Correction."""
        corr = 350.0 / (self.eop + 70)
        if corr > 2.0:
            corr /= 2
        return corr


@dataclass
class BazaraaPeckOPC(OPC):
    r"""Overburden Pressure Correction according to ``Bazaraa (1967)``, and
    also by ``Peck and Bazaraa (1969)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math::

        C_N &= \dfrac{4}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2

        C_N &= \dfrac{4}{3.25 + 0.0104 \cdot \sigma_o}, \, \sigma_o \gt 71.8kN/m^2

        C_N &= 1 \, , \, \sigma_o = 71.8kN/m^2

    Examples
    --------
    >>> from geolysis.core.spt import BazaraaPeckOPC
    >>> opc_cor = BazaraaPeckOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.corrected_spt_number
    21.0
    """

    #: Maximum effective overburden pressure. |rarr| :math:`kN/m^2`
    STD_PRESSURE: Final = field(default=71.8, init=False)

    std_spt_number: float
    eop: float

    @property
    def correction(self) -> float:
        """SPT Correction."""
        if isclose(self.eop, self.STD_PRESSURE, rel_tol=0.01):
            corr = 1.0
        elif self.eop < self.STD_PRESSURE:
            corr = 4 / (1 + 0.0418 * self.eop)
        else:
            corr = 4 / (3.25 + 0.0104 * self.eop)

        return corr


@dataclass
class PeckOPC(OPC):
    r"""Overburden Pressure Correction according to ``Peck et al (1974)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = 0.77 \log \left( \dfrac{2000}{\sigma_o} \right)

    Examples
    --------
    >>> from geolysis.core.spt import PeckOPC
    >>> opc_cor = PeckOPC(std_spt_number=23.0, eop=100.0)
    >>> opc_cor.corrected_spt_number
    23.0
    """

    #: Maximum effective overburden pressure. |rarr| :math:`kN/m^2`
    STD_PRESSURE: Final = 24.0

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
    def correction(self) -> float:
        """SPT Correction."""
        return 0.77 * log10(2000 / self.eop)


@dataclass
class LiaoWhitmanOPC(OPC):
    r"""Overburden Pressure Correction according to ``Liao & Whitman (1986)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \sqrt{\dfrac{100}{\sigma_o}}

    Examples
    --------
    >>> from geolysis.core.spt import LiaoWhitmanOPC
    >>> opc_cor = LiaoWhitmanOPC(std_spt_number=23.0, eop=100.0)
    >>> opc_cor.corrected_spt_number
    23.0
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
    def correction(self) -> float:
        """SPT Correction."""
        return sqrt(100 / self.eop)


@dataclass
class SkemptonOPC(OPC):
    r"""Overburden Pressure Correction according to ``Skempton (1986)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, :math:`kN/m^2`
        Effective overburden pressure.

    Attributes
    ----------
    correction : float
    corrected_spt_number : float

    Notes
    -----
    Overburden Pressure Correction is given by the formula:

    .. math:: C_N = \dfrac{2}{1 + 0.01044 \cdot \sigma_o}

    Examples
    --------
    >>> from geolysis.core.spt import SkemptonOPC
    >>> opc_cor = SkemptonOPC(std_spt_number=22.5, eop=100.0)
    >>> opc_cor.corrected_spt_number
    22.0
    """

    std_spt_number: float
    eop: float

    @property
    def correction(self) -> float:
        """SPT Correction."""
        return 2 / (1 + 0.01044 * self.eop)


@dataclass
class DilatancyCorrection:
    r"""Dilatancy SPT Correction according to ``Terzaghi & Peck (1948)``.

    For coarse sand, this correction is not required. In applying this
    correction, overburden pressure correction is applied first and then
    dilatancy correction is applied.

    Parameters
    ----------
    spt_number : float
        SPT N-value standardized for field procedures and/or corrected for
        overburden pressure.

    Attributes
    ----------
    corrected_spt_number : float

    Notes
    -----
    Dilatancy correction is given by the formula:

    .. math::

        (N_1)_{60} &= 15 + \dfrac{1}{2}((N_1)_{60} - 15) \, , \,
                      (N_1)_{60} \gt 15

        (N_1)_{60} &= (N_1)_{60} \, , \, (N_1)_{60} \le 15

    Examples
    --------
    >>> from geolysis.core.spt import DilatancyCorrection
    >>> dil_cor = DilatancyCorrection(spt_number=23)
    >>> dil_cor.corrected_spt_number
    19.0
    """

    spt_number: float

    @property
    @round_
    def corrected_spt_number(self) -> float:
        """Corrected SPT N-value."""
        if self.spt_number <= 15:
            return self.spt_number

        return 15 + 0.5 * (self.spt_number - 15)
