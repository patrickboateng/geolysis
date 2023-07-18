"""This module provides functions for estimating soil engineering parameters."""

from typing import Optional

from geolab import GeotechEng
from geolab.utils import arctan, round_, sin


class soil_unit_weight:
    """Calculates the moist, saturated and submerged unit weight of soil.

    :param spt_n60: spt N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    """

    def __init__(self, spt_n60: float) -> None:
        self.spt_n60 = spt_n60

    def __call__(self) -> float:
        return self.moist

    @property
    @round_
    def moist(self) -> float:
        return 16.0 + 0.1 * self.spt_n60

    @property
    @round_
    def saturated(self) -> float:
        return 16.8 + 0.15 * self.spt_n60

    @property
    @round_
    def submerged(self) -> float:
        return 8.8 + 0.01 * self.spt_n60


def _terzaghi_peck_compression_idx(liquid_limit: float) -> float:
    return 0.009 * (liquid_limit - 10)


def _skempton_compression_idx(liquid_limit: float) -> float:
    return 0.007 * (liquid_limit - 10)


def _hough_compression_idx(void_ratio: float) -> float:
    return 0.29 * (void_ratio - 0.27)


@round_
def compression_index(
    liquid_limit: Optional[float] = None,
    void_ratio: Optional[float] = None,
    eng: GeotechEng = GeotechEng.SKEMPTON,
) -> float:
    r"""The compression index of the soil estimated from ``liquid limit`` or ``void_ratio``.

    The available correlations used are defined below; They are in the order ``Skempton (1994)``,
    ``Terzaghi and Peck (1967)`` and ``Hough (1957)``.

    .. math::

        C_c = 0.007 \left(LL - 10 \right)

        C_c = 0.009 \left(LL - 10 \right)

        C_c = 0.29 \left(e_o - 0.27 \right)

    :Example:

    :param liquid_limit: water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :param void_ratio: volume of voids divided by volume of solids (unitless)
    :type void_ratio: float
    :param eng: specifies the type of compression index formula to use. Available
                values are geolab.SKEMPTON, geolab.TERZAGHI and geolab.HOUGH
    :type eng: GeotechEng
    :return: compression index of soil (unitless)
    :rtype: float
    """

    if (liquid_limit is None) and (void_ratio is None):
        msg = "both liquid limit and void ratio cannot be None"
        raise ValueError(msg)

    if eng is GeotechEng.SKEMPTON:
        return _skempton_compression_idx(liquid_limit)

    if eng is GeotechEng.TERZAGHI:
        return _terzaghi_peck_compression_idx(liquid_limit)

    if eng is GeotechEng.HOUGH:
        return _hough_compression_idx(void_ratio)

    msg = f"{eng} is not a valid type for compression index"
    raise TypeError(msg)


@round_
def soil_elastic_modulus(spt_n60: float) -> float:
    r"""Elastic modulus of soil estimated from ``Joseph Bowles`` correlation.

    .. math::

        E_s = 320\left(N_{60} + 15 \right)

    :Example:
        >>> soil_elastic_modulus(20)
        11200
        >>> soil_elastic_modulus(30)
        14400
        >>> soil_elastic_modulus(10)
        8000

    :param spt_n60: spt N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :return: Elastic modulus of the soil :math:`kN/m^2`
    :rtype: float
    """
    return 320 * (spt_n60 + 15)


@round_
def foundation_depth(
    allow_bearing_capacity: float,
    unit_weight_of_soil: float,
    friction_angle: float,
) -> float:
    r"""Depth of foundation estimated using ``Rankine's`` formula.

    .. math::

        D_f=\dfrac{Q_{all}}{\gamma}\left(\dfrac{1 - \sin \phi}{1 + \sin \phi}\right)^2

    :param allow_bearing_capacity: allowable bearing capacity
    :type allow_bearing_capaciy: float
    :param unit_weight_of_soil: unit weight of soil :math:`kN/m^3`
    :type unit_weight_of_soil: float
    :param friction_angle: internal angle of friction (degrees)
    :type friction_angle: float
    :return: depth of foundation
    :rtype: float
    """
    return (allow_bearing_capacity / unit_weight_of_soil) * (
        (1 - sin(friction_angle)) / (1 + sin(friction_angle))
    ) ** 2


def _peck_et_al_friction_angle(spt_n60: float) -> float:
    return 27.1 + (0.3 * spt_n60) - (0.00054 * (spt_n60**2))


def _kullhawy_mayne_friction_angle(
    spt_n60: float,
    eop: float,
    atm_pressure: float,
) -> float:
    expr = spt_n60 / (12.2 + 20.3 * (eop / atm_pressure))
    return arctan(expr**0.34)


@round_
def friction_angle(
    spt_n60,
    eop: Optional[float] = None,
    atm_pressure: Optional[float] = None,
) -> float:
    r"""Estimation of the internal angle of friction using spt_n60.

    For cohesionless soils the coefficient of internal friction :math:`\phi` was
    determined from the minimum value from ``Peck, Hanson and Thornburn (1974)``
    and ``Kullhawy and Mayne (1990)`` respectively. The correlations are shown below.

    .. math::

        \phi = 27.1 + 0.3 \times N_{60} - 0.00054 \times (N_{60})^2

        \phi = \tan^{-1}\left[\dfrac{N_{60}}{12.2 + 20.3(\frac{\sigma_o}{P_a})} \right]^0.34

    :Example:

    :param spt_n60: spt N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :param eop: effective overburden pressure :math:`kN/m^2`, defaults to None
    :type eop: float, optional
    :param atm_pressure: atmospheric pressure :math:`kN/m^2`, defaults to None
    :type atm_pressure: float, optional
    :return: internal angle of friction in degrees
    :rtype: float
    """
    if (eop is not None) and (atm_pressure is not None):
        return _kullhawy_mayne_friction_angle(spt_n60, eop, atm_pressure)

    return _peck_et_al_friction_angle(spt_n60)


def _stroud_undrained_shear_strength(spt_n60, k):
    if not (3.5 <= k <= 6.5):
        msg = f"k should be 3.5 <= k <= 6.5 not {k}"
        raise ValueError(msg)

    return k * spt_n60


def _skempton_undrained_shear_strength(eop, plasticity_index):
    return eop * (0.11 + 0.0037 * plasticity_index)


@round_
def undrained_shear_strength(
    spt_n60: Optional[float] = None,
    eop: Optional[float] = None,
    plasticity_index: Optional[float] = None,
    k: float = 3.5,
    eng: GeotechEng = GeotechEng.STROUD,
) -> None:
    r"""Undrained shear strength.

    The available correlations used are defined below;

    .. math::

        Stroud (1974) \, \rightarrow C_u = K \times N_{60}

        Skempton (1957) \, \rightarrow \dfrac{C_u}{\sigma_o} = 0.11 + 0.0037 \times PI

    The ratio :math:`\frac{C_u}{\sigma_o}` is a constant for a given clay. ``Skempton``
    suggested that a similar constant ratio exists between the undrained shear strength
    of normally consolidated natural deposits and the effective overburden pressure.
    It has been established that the ratio :math:`\frac{C_u}{\sigma_o}` is constant provided the
    plasticity index (PI) of the soil remains constant.

    The value of the ratio :math:`\frac{C_u}{\sigma_o}` determined in a consolidated-undrained test on
    undisturbed samples is generally greater than actual value because of anisotropic consolidation
    in the field. The actual value is best determined by `in-situ shear vane test`.
    (:cite:author:`2003:arora`, p. 330)

    :param spt_n60: SPT N-value corrected for 60% hammer efficiency, defaults to None
    :type spt_n60: Optional[float], optional
    :param eop: effective overburden pressure :math:`kN/m^2`, defaults to None
    :type eop: Optional[float], optional
    :param plasticity_index: range of water content over which soil remains in plastic condition, defaults to None
    :type plasticity_index: Optional[float], optional
    :param k: stroud parameter, defaults to 3.5
    :type k: float, optional
    :param eng: specifies the type of undrained shear strength formula to use. Available values are
                geolab.STROUD and geolab.SKEMPTON, defaults to GeotechEng.STROUD
    :type eng: GeotechEng, optional
    :raises ValueError:
    :raises TypeError:
    :return:
    :rtype: float

    References
    ----------

    .. bibliography::
    """
    if eng is GeotechEng.STROUD:
        return _stroud_undrained_shear_strength(spt_n60, k)

    if eng is GeotechEng.SKEMPTON:
        return _skempton_undrained_shear_strength(eop, plasticity_index)

    msg = f"{eng} is not a valid type for undrained shear strength"
    raise TypeError(msg)
