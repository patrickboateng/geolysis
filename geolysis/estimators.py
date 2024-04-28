from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from geolysis.constants import ERROR_TOL

# from geolysis.constants import UnitRegistry as ureg
from geolysis.utils import arctan, isclose, round_

# from typing import Optional


__all__ = [
    "SoilUnitWeight",
    "TerzaghiCompressionIndex",
    "SkemptonCompressionIndex",
    "HoughCompressionIndex",
    "WolffSoilFrictionAngle",
    "KullhawyMayneSoilFrictionAngle",
    "StroudUndrainedShearStrength",
    "SkemptonUndrainedShearStrength",
]


class EstimatorError(ValueError):
    pass


@dataclass
class SoilUnitWeight:
    r"""Estimates the ``moist``, ``saturated`` and ``submerged`` unit weight of
    soil sample from ``SPT N60``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures considering 60% energy.

    Attributes
    ----------
    std_spt_number : float
    moist_wgt : float
    saturated_wgt : float
    submerged_wgt : float

    Notes
    -----
    The following formulae below are used for estimating the ``moist``, ``saturated``,
    and ``submerged`` unit weight respectively.

    .. math::

        \gamma_{moist} &= 16.0 + 0.1 \cdot N_{60}

        \gamma_{sat} &= 16.8 + 0.15 \cdot N_{60}

        \gamma_{sub} &= 8.8 + 0.01 \cdot N_{60}

    Examples
    --------
    >>> from geolysis.estimators import SoilUnitWeight

    >>> suw_est = SoilUnitWeight(std_spt_number=15)
    >>> suw_est.moist_wgt
    17.5
    >>> suw_est.saturated_wgt
    19.05
    >>> suw_est.submerged_wgt
    8.95
    """

    def __init__(self, std_spt_number) -> None:
        self.std_spt_number = std_spt_number

    @property
    @round_
    def moist_wgt(self) -> float:
        """Return the ``moist unit weight`` for cohesionless soils.
        |rarr| :math:`kN/m^3`"""
        return 16.0 + 0.1 * self.std_spt_number

    @property
    @round_
    def saturated_wgt(self) -> float:
        """Return the ``saturated unit weight`` for cohesive soils.
        |rarr| :math:`kN/m^3`
        """
        return 16.8 + 0.15 * self.std_spt_number

    @property
    @round_
    def submerged_wgt(self) -> float:
        """Return the ``submerged unit weight`` for cohesionless soils.
        |rarr| :math:`kN/m^3`
        """
        return 8.8 + 0.01 * self.std_spt_number


class _CompressionIndexEst(Protocol):

    @property
    @abstractmethod
    def compression_index(self) -> float: ...


@dataclass
class TerzaghiCompressionIndex:
    """Compression Index of soil according to ``Terzaghi et al (1967)``.

    Parameters
    ----------
    liquid_limit : float
        Water content beyond which soils flow under their own weight.

    Attributes
    ----------
    liquid_limit : float
    compression_index : float

    Notes
    -----
    Compression index is given by the formula:

    .. math:: C_i = 0.009 (LL - 10)

    Examples
    --------
    >>> from geolysis.estimators import TerzaghiCompressionIndex
    >>> comp_idx_est = TerzaghiCompressionIndex(liquid_limit=40.0)
    >>> comp_idx_est.compression_index
    0.27
    """

    liquid_limit: float

    @property
    @round_(ndigits=3)
    def compression_index(self) -> float:
        """Return the compression index of soil."""
        return 0.009 * (self.liquid_limit - 10.0)


@dataclass
class SkemptonCompressionIndex:
    """Compression Index of soil according to ``Skempton (1994)``.

    Parameters
    ----------
    liquid_limit : float
        Water content beyond which soils flow under their own weight.

    Attributes
    ----------
    liquid_limit : float
    compression_index : float

    Notes
    -----
    Compression index is given by the formula:

    .. math:: C_i = 0.007 (LL - 10)

    Examples
    --------
    >>> from geolysis.estimators import SkemptonCompressionIndex
    >>> comp_idx_est = SkemptonCompressionIndex(liquid_limit=40.0)
    >>> comp_idx_est.compression_index
    0.21
    """

    liquid_limit: float

    @property
    @round_(ndigits=3)
    def compression_index(self) -> float:
        """Return the compression index of soil from ``Skempton's`` correlation."""
        return 0.007 * (self.liquid_limit - 10.0)


@dataclass
class HoughCompressionIndex:
    """Compression Index of soil according to ``Hough (1957)``.

    Parameters
    ----------
    void_ratio : float
        Ratio of the volume of voids to the volume of solids.

    Attributes
    ----------
    void_ratio : float
    compression_index : float

    Notes
    -----
    Compression index is given by the formula:

    .. math:: C_i = 0.29 (e_o - 0.27)

    Examples
    --------
    >>> from geolysis.estimators import HoughCompressionIndex
    >>> comp_idx_est = HoughCompressionIndex(void_ratio=0.78)
    >>> comp_idx_est.compression_index
    0.148
    """

    void_ratio: float

    @property
    @round_(ndigits=3)
    def compression_index(self) -> float:
        return 0.29 * (self.void_ratio - 0.27)


class _SoilFrictionAngleEst(Protocol):

    @property
    @abstractmethod
    def soil_friction_angle(self) -> float: ...


@dataclass
class WolffSoilFrictionAngle:
    r"""Soil Friction Angle according to ``Wolff (1989)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.

    Attributes
    ----------
    std_spt_number : float
    soil_friction_angle : float

    Notes
    -----
    Soil Friction Angle is given by the formula:

    .. math:: \phi = 27.1 + 0.3 \cdot N_{60} - 0.00054 \cdot (N_{60})^2

    Examples
    --------
    >>> from geolysis.estimators import WolffSoilFrictionAngle

    >>> sfa_est = WolffSoilFrictionAngle(std_spt_number=15)
    >>> sfa_est.soil_friction_angle
    31.48
    """

    std_spt_number: float

    @property
    @round_(ndigits=2)
    def soil_friction_angle(self) -> float:
        return (
            27.1
            + (0.3 * self.std_spt_number)
            - (0.00054 * (self.std_spt_number**2))
        )


@dataclass
class KullhawyMayneSoilFrictionAngle:
    r"""Soil Friction Angle according to ``Kullhawy & Mayne (1990)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    eop : float, unit = :math:`kN/m^2`
        Effective overburden pressure, ``eop`` should be in the same unit as
        ``atm_pressure``.
    atm_pressure : float, unit = :math:`kN/m^2`
        Atmospheric pressure, ``atm_pressure`` should be in the same unit as ``eop``.

    Attributes
    ----------
    std_spt_number : float
    eop : float
    atm_pressure : float
    soil_friction_angle : float

    Notes
    -----
    Soil Friction Angle is given by the formula:

    .. math::

        \phi = tan^{-1}\left[\left(\dfrac{N_{60}}{12.2 + 20.3 \cdot
                    \frac{\sigma_o}{P_a}}\right)^{0.34}\right]

    Examples
    --------
    >>> from geolysis.estimators import KullhawyMayneSoilFrictionAngle

    >>> sfa_est = KullhawyMayneSoilFrictionAngle(std_spt_number=15, eop=103.8,
    ...                                          atm_pressure=101.3)
    >>> sfa_est.soil_friction_angle
    37.41

    >>> sfa_est.atm_pressure = 0.0
    Traceback (most recent call last):
        ...
    EstimatorError: atm_pressure = 0.0 cannot be close to 0.0
    """

    def __init__(self, std_spt_number: float, eop: float, atm_pressure: float):
        self.std_spt_number = std_spt_number
        self.eop = eop
        self.atm_pressure = atm_pressure

    @property
    def atm_pressure(self) -> float:
        return self._atm_pressure

    @atm_pressure.setter
    def atm_pressure(self, __val):
        if isclose(__val, 0, rel_tol=ERROR_TOL):
            err_msg = f"atm_pressure = {__val} cannot be close to 0.0"
            raise EstimatorError(err_msg)
        self._atm_pressure = __val

    @property
    @round_(ndigits=3)
    def soil_friction_angle(self) -> float:
        angle = self.std_spt_number / (
            12.2 + 20.3 * (self.eop / self.atm_pressure)
        )
        return arctan(angle**0.34)


class _UndrainedShearStrengthEst(Protocol):
    @property
    @abstractmethod
    def undrained_shear_strength(self) -> float: ...


@dataclass
class StroudUndrainedShearStrength:
    r"""Undrained Shear Strength according to ``Stroud (1974)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    k : float, default=3.5, unit = :math:`kN/m^2`
        Stroud constant. :math:`3.5 \le k \le 6.5`

    Attributes
    ----------
    spt_n_60 : float
    k : float
    undrained_shear_strength : float

    Raises
    ------
    EstimatorError
        If ``k`` is not in the specified range. :math:`3.5 \le k \le 6.5`

    Notes
    -----
    Undrained Shear Strength is given by the formula:

    .. math:: C_u = k \cdot N_{60}

    Examples
    --------
    >>> from geolysis.estimators import StroudUndrainedShearStrength

    >>> uss_est = StroudUndrainedShearStrength(std_spt_number=10)
    >>> uss_est.undrained_shear_strength
    35.0
    >>> uss_est.k = 7
    Traceback (most recent call last):
        ...
    EstimatorError: k = 7 should be in the range 3.5 <= k <= 6.5
    """

    def __init__(self, std_spt_number: float, k=3.5) -> None:
        self.std_spt_number = std_spt_number
        self.k = k

    @property
    def k(self) -> float:
        return self._k

    @k.setter
    def k(self, __val: float):
        if not (3.5 <= __val <= 6.5):
            err_msg = "k = {__val} should be in the range 3.5 <= k <= 6.5"
            raise EstimatorError(err_msg)
        self._k = __val

    @property
    @round_(ndigits=2)
    def undrained_shear_strength(self) -> float:
        return self.k * self.std_spt_number


@dataclass
class SkemptonUndrainedShearStrength:
    r"""Undrained Shear Strength according to ``Skempton (1957)``.

    Parameters
    ----------
    eop : float, unit = :math:`kN/m^2`
        Effective overburden pressure.
    plasticity_index : float
        Range of water content over which soil remains in plastic condition.

    Attributes
    ----------
    eop : float
    plasticity_index : float
    undrained_shear_strength : float

    Raises
    ------
    EstimatorError
        If ``k`` is not in the specified range. :math:`3.5 \le k \le 6.5`

    Notes
    -----
    Undrained Shear Strength is given by the formula:

    .. math:: C_u = \sigma_o (0.11 + 0.0037 \cdot PI)

    The value of the ratio :math:`\frac{C_u}{\sigma_o}` determined in a
    consolidated-undrained test on undisturbed samples is generally greater
    than actual value because of anisotropic consolidation in the field.
    The actual value is best determined by ``in-situ shear vane test``.

    Examples
    --------
    >>> from geolysis.estimators import SkemptonUndrainedShearStrength
    >>> uss_est = SkemptonUndrainedShearStrength(eop=76.8, plasticity_index=25.7)
    >>> uss_est.undrained_shear_strength
    15.75
    """

    eop: float
    plasticity_index: float

    @property
    @round_(ndigits=2)
    def undrained_shear_strength(self) -> float:
        return self.eop * (0.11 + 0.0037 * self.plasticity_index)
