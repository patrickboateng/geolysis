"""This module provides functions for estimating soil engineering parameters."""

from typing import Any, Optional

from geolab import DECIMAL_PLACES, GeotechEng
from geolab.utils import sin, arctan


class unit_weight:
    def __init__(self, spt_n60: float) -> None:
        self.spt_n60 = spt_n60

    def __call__(self, *args: Any, **kwargs: Any) -> float:
        return self.moist()

    def moist(self) -> float:
        return round(16.0 + 0.1 * self.spt_n60, DECIMAL_PLACES)

    def saturated(self) -> float:
        return round(16.8 + 0.15 * self.spt_n60, DECIMAL_PLACES)

    def submerged(self) -> float:
        return round(8.8 + 0.01 * self.spt_n60, DECIMAL_PLACES)


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

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :param void_ratio: Volume of voids divided by volume of solids (unitless)
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
        _ci = 0.007 * (liquid_limit - 10)
        return round(_ci, DECIMAL_PLACES)

    if eng is GeotechEng.TERZAGHI:
        _ci = 0.009 * (liquid_limit - 10)
        return round(_ci, DECIMAL_PLACES)

    if eng is GeotechEng.HOUGH:
        _ci = 0.29 * (void_ratio - 0.27)
        return round(_ci, DECIMAL_PLACES)

    msg = f"{eng} is not a valid type for compression index"
    raise TypeError(msg)


def elastic_modulus(spt_n60: float) -> float:
    r"""Elastic modulus of soil estimated from ``Joseph Bowles`` correlation.

    .. math::

        E_s = 320\left(N_{60} + 15 \right)

    :Example:
        >>> elastic_modulus(20)
        11200
        >>> elastic_modulus(30)
        14400
        >>> elastic_modulus(10)
        8000

    :param spt_n60: SPT N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :return: Elastic modulus of the soil :math:`kN/m^2`
    :rtype: float
    """
    _elastic_modulus = 320 * (spt_n60 + 15)
    return round(_elastic_modulus, DECIMAL_PLACES)


def foundation_depth(
    allow_bearing_capacity: float,
    unit_weight_of_soil: float,
    friction_angle: float,
) -> float:
    r"""Depth of foundation estimated using ``Rankine's`` formula.

    .. math::

        D_f=\dfrac{Q_{all}}{\gamma}\left(\dfrac{1 - \sin \phi}{1 + \sin \phi}\right)^2

    :param allow_bearing_capacity: Allowable bearing capacity
    :type allow_bearing_capaciy: float
    :param unit_weight_of_soil: Unit weight of soil :math:`kN/m^3`
    :type unit_weight_of_soil: float
    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    :return: Depth of foundation
    :rtype: float
    """
    q_all = allow_bearing_capacity
    gamma = unit_weight_of_soil
    phi = friction_angle
    _foundation_depth = (q_all / gamma) * ((1 - sin(phi)) / (1 + sin(phi))) ** 2

    return round(_foundation_depth, DECIMAL_PLACES)


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

    :param spt_n60: The SPT N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :param eop: Effective overburden pressure :math:`kN/m^2`, defaults to None
    :type eop: float, optional
    :param atm_pressure: Atmospheric pressure :math:`kN/m^2`, defaults to None
    :type atm_pressure: float, optional
    :return: The internal angle of friction in degrees
    :rtype: float
    """
    if (eop is not None) and (atm_pressure is not None):
        expr = spt_n60 / (12.2 + 20.3 * (eop / atm_pressure))
        phi = arctan(expr**0.34)
        return round(phi, DECIMAL_PLACES)

    phi = 27.1 + (0.3 * spt_n60) - (0.00054 * (spt_n60**2))

    # rounded to 2 d.p for consistency with eng. practices
    return round(phi, DECIMAL_PLACES)


def _stroud_undrained_shear_strength(spt_n60, k):
    if not (3.5 <= k <= 6.5):
        msg = f"k should be 3.5 <= k <= 6.5 not {k}"
        raise ValueError(msg)

    return round(k * spt_n60, DECIMAL_PLACES)


def _skempton_undrained_strength(eop, plasticity_index):
    return round(eop * (0.11 + 0.0037 * plasticity_index), DECIMAL_PLACES)


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
        return _skempton_undrained_strength(eop, plasticity_index)

    msg = f"{eng} is not a valid type for undrained shear strength"
    raise TypeError(msg)
