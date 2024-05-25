from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from .constants import ERROR_TOL, UNIT
from .utils import arctan, isclose, round_

__all__ = [
    "MoistUnitWeight",
    "SaturatedUnitWeight",
    "SubmergedUnitWeight",
    "TerzaghiCompressionIndex",
    "SkemptonCompressionIndex",
    "HoughCompressionIndex",
    "WolffSoilFrictionAngle",
    "KullhawyMayneSoilFrictionAngle",
    "StroudUndrainedShearStrength",
    "SkemptonUndrainedShearStrength",
]

deg = UNIT.deg
kN_m3 = UNIT.kN_m3
kPa = UNIT.kPa


class EstimatorError(ValueError):
    pass


# Protocols


class _UnitWeight(Protocol):
    @property
    @abstractmethod
    def unit_wgt(self): ...


class _CompressionIndexEst(Protocol):
    @property
    @abstractmethod
    def compression_index(self) -> float: ...


class _SoilFrictionAngleEst(Protocol):
    @property
    @abstractmethod
    def soil_friction_angle(self) -> float: ...


class _UndrainedShearStrengthEst(Protocol):
    @property
    @abstractmethod
    def undrained_shear_strength(self) -> float: ...


@dataclass
class MoistUnitWeight:
    r"""Estimates the moist unit weight of soil from SPT N-value.

    Parameters
    ----------
     std_spt_number : float
        SPT N-value standardized for field procedures considering 60%
        energy. This is also known as SPT :math:`N_{60}`.

    Attributes
    ----------
    unit_wgt : float

    Notes
    -----
    Moist unit weight is given by the formula:

    .. math:: \gamma_{moist} = 16.0 + 0.1 \cdot N_{60}

    Examples
    --------
    >>> from geolysis.core.estimators import MoistUnitWeight
    >>> suw_est = MoistUnitWeight(std_spt_number=15.0)
    >>> suw_est.unit_wgt
    17.5
    """

    std_spt_number: float

    _unit = kN_m3

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
    def unit_wgt(self) -> float:
        """Return the ``moist unit weight`` for cohesionless soils.
        |rarr| :math:`kN/m^3`"""
        return 16.0 + 0.1 * self.std_spt_number


@dataclass
class SaturatedUnitWeight:
    r"""Estimates the saturated unit weight of soil from SPT N-value.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures considering 60%
        energy. This is also known as SPT :math:`N_{60}`.

    Attributes
    ----------
    unit_wgt : float

    Notes
    -----
    Saturated unit weight is given by the formula:

    .. math:: \gamma_{sat} = 16.8 + 0.15 \cdot N_{60}

    Examples
    --------
    >>> from geolysis.core.estimators import SaturatedUnitWeight
    >>> suw_est = SaturatedUnitWeight(std_spt_number=15.0)
    >>> suw_est.unit_wgt
    19.05
    """

    std_spt_number: float

    _unit = kN_m3

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
    def unit_wgt(self) -> float:
        """Return the ``saturated unit weight`` for cohesive soils.
        |rarr| :math:`kN/m^3`
        """
        return 16.8 + 0.15 * self.std_spt_number


@dataclass
class SubmergedUnitWeight:
    r"""Estimates the submerged unit weight of soil from SPT N-value.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures considering 60%
        energy. This is also known as SPT :math:`N_{60}`.

    Attributes
    ----------
    unit_wgt : float

    Notes
    -----
    Submerged unit weight is given by the formula:

    .. math:: \gamma_{sub} = 8.8 + 0.01 \cdot N_{60}

    Examples
    --------
    >>> from geolysis.core.estimators import SubmergedUnitWeight
    >>> suw_est = SubmergedUnitWeight(std_spt_number=15.0)
    >>> suw_est.unit_wgt
    8.95
    """

    std_spt_number: float

    _unit = kN_m3

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
    def unit_wgt(self) -> float:
        """Return the ``submerged unit weight`` for cohesionless soils.
        |rarr| :math:`kN/m^3`
        """
        return 8.8 + 0.01 * self.std_spt_number


@dataclass
class TerzaghiCompressionIndex:
    """Compression Index of soil according to ``Terzaghi et al (1967)``.

    Parameters
    ----------
    liquid_limit : float
        Water content beyond which soils flow under their own weight.

    Attributes
    ----------
    compression_index : float

    Notes
    -----
    Compression index is given by the formula:

    .. math:: C_i = 0.009 (LL - 10)

    Examples
    --------
    >>> from geolysis.core.estimators import TerzaghiCompressionIndex
    >>> comp_idx_est = TerzaghiCompressionIndex(liquid_limit=40.0)
    >>> comp_idx_est.compression_index
    0.27
    """

    liquid_limit: float

    _unit = ""

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
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
    compression_index : float

    Notes
    -----
    Compression index is given by the formula:

    .. math:: C_i = 0.007 (LL - 10)

    Examples
    --------
    >>> from geolysis.core.estimators import SkemptonCompressionIndex
    >>> comp_idx_est = SkemptonCompressionIndex(liquid_limit=40.0)
    >>> comp_idx_est.compression_index
    0.21
    """

    liquid_limit: float

    _unit = ""

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
    def compression_index(self) -> float:
        """Return the compression index of soil."""
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
    compression_index : float

    Notes
    -----
    Compression index is given by the formula:

    .. math:: C_i = 0.29 (e_o - 0.27)

    Examples
    --------
    >>> from geolysis.core.estimators import HoughCompressionIndex
    >>> comp_idx_est = HoughCompressionIndex(void_ratio=0.78)
    >>> comp_idx_est.compression_index
    0.1479
    """

    void_ratio: float

    _unit = ""

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
    def compression_index(self) -> float:
        """Return the compression index of soil."""
        return 0.29 * (self.void_ratio - 0.27)


@dataclass
class WolffSoilFrictionAngle:
    r"""Soil Friction Angle according to ``Wolff (1989)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.

    Attributes
    ----------
    soil_friction_angle : float

    Notes
    -----
    Soil Friction Angle is given by the formula:

    .. math:: \phi = 27.1 + 0.3 \cdot N_{60} - 0.00054 \cdot (N_{60})^2

    Examples
    --------
    >>> from geolysis.core.estimators import WolffSoilFrictionAngle

    >>> sfa_est = WolffSoilFrictionAngle(std_spt_number=15.0)
    >>> sfa_est.soil_friction_angle
    31.4785
    """

    std_spt_number: float

    _unit = deg

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
    def soil_friction_angle(self) -> float:
        """Return the internal angle of friction of soil."""
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
    eop : float, :math:`kN/m^2`
        Effective overburden pressure, ``eop`` should be in the same unit as
        ``atm_pressure``.
    atm_pressure : float, :math:`kN/m^2`
        Atmospheric pressure, ``atm_pressure`` should be in the same unit as
        ``eop``.

    Attributes
    ----------
    soil_friction_angle : float

    Raises
    ------
    EstimatorError
        Raised when ``atm_pressure`` is close to zero.

    Notes
    -----
    Soil Friction Angle is given by the formula:

    .. math::

        \phi = tan^{-1}\left[\left(\dfrac{N_{60}}{12.2 + 20.3 \cdot
                    \frac{\sigma_o}{P_a}}\right)^{0.34}\right]

    Examples
    --------
    >>> from geolysis.core.estimators import KullhawyMayneSoilFrictionAngle

    >>> sfa_est = KullhawyMayneSoilFrictionAngle(std_spt_number=15.0, eop=103.8,
    ...                                          atm_pressure=101.3)
    >>> sfa_est.soil_friction_angle
    37.4103
    """

    _unit = deg

    def __init__(self, std_spt_number: float, eop: float, atm_pressure: float):
        self.std_spt_number = std_spt_number
        self.eop = eop
        self.atm_pressure = atm_pressure

    @property
    def unit(self) -> str:
        return self._unit

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
    @round_
    def soil_friction_angle(self) -> float:
        """Return the internal angle of friction of soil."""
        angle = self.std_spt_number / (
            12.2 + 20.3 * (self.eop / self.atm_pressure)
        )
        return arctan(angle**0.34)


@dataclass
class StroudUndrainedShearStrength:
    r"""Undrained Shear Strength according to ``Stroud (1974)``.

    Parameters
    ----------
    std_spt_number : float
        SPT N-value standardized for field procedures.
    k : float, default=3.5, :math:`kN/m^2`
        Stroud constant. :math:`3.5 \le k \le 6.5`

    Attributes
    ----------
    undrained_shear_strength : float

    Raises
    ------
    EstimatorError
        Raised If ``k`` is not in the specified range. :math:`3.5 \le k \le 6.5`

    Notes
    -----
    Undrained Shear Strength is given by the formula:

    .. math:: C_u = k \cdot N_{60}

    Examples
    --------
    >>> from geolysis.core.estimators import StroudUndrainedShearStrength

    >>> uss_est = StroudUndrainedShearStrength(std_spt_number=10.0)
    >>> uss_est.undrained_shear_strength
    35.0
    """

    _unit = kPa

    def __init__(self, std_spt_number: float, k=3.5) -> None:
        self.std_spt_number = std_spt_number
        self.k = k

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def k(self) -> float:
        return self._k

    @k.setter
    def k(self, __val: float):
        if not 3.5 <= __val <= 6.5:
            err_msg = "k = {__val} should be in the range 3.5 <= k <= 6.5"
            raise EstimatorError(err_msg)
        self._k = __val

    @property
    @round_
    def undrained_shear_strength(self) -> float:
        """Return the undrained shear strength of soil."""
        return self.k * self.std_spt_number


@dataclass
class SkemptonUndrainedShearStrength:
    r"""Undrained Shear Strength according to ``Skempton (1957)``.

    Parameters
    ----------
    eop : float, :math:`kN/m^2`
        Effective overburden pressure.
    plasticity_index : float
        Range of water content over which soil remains in plastic condition.

    Attributes
    ----------
    undrained_shear_strength : float

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
    >>> from geolysis.core.estimators import SkemptonUndrainedShearStrength
    >>> uss_est = SkemptonUndrainedShearStrength(eop=76.8, plasticity_index=25.7)
    >>> uss_est.undrained_shear_strength
    15.7509
    """

    eop: float
    plasticity_index: float

    _unit = kPa

    @property
    def unit(self) -> str:
        return self._unit

    @property
    @round_
    def undrained_shear_strength(self) -> float:
        """Return the undrained shear strength of soil."""
        return self.eop * (0.11 + 0.0037 * self.plasticity_index)
