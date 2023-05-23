"""This module provides functions for estimating soil engineering parameters."""

from typing import Optional

import numpy as np

from geolab import DECIMAL_PLACES, deg2rad


def skempton_compression_index(liquid_limit: float) -> float:
    r"""The compression index of the soil estimated from ``Skempton`` (1994)
    relation.

    .. math::

        C_c = 0.007 \left(LL - 10 \right)

    :Example:

        >>> skempton_compression_index(30)
        0.14
        >>> skempton_compression_index(50)
        0.28
        >>> skempton_compression_index(20)
        0.07

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :return: compression index of soil (unitless)
    :rtype: float
    """
    compression_index = 0.007 * (liquid_limit - 10)
    return np.round(compression_index, DECIMAL_PLACES)


def terzaghi_compression_index(liquid_limit: float) -> float:
    r"""The compression index of the soil estimated from ``Terzagi`` and
    ``Peck`` (1967) relation.

    .. math::

        C_c = 0.009 \left(LL - 10 \right)

    :Example:

        >>> terzaghi_compression_index(30)
        0.18
        >>> terzaghi_compression_index(50)
        0.36
        >>> terzaghi_compression_index(20)
        0.09

    :param liquid_limit: Water content beyond which soils flows under their own weight (%)
    :type liquid_limit: float
    :return: compression index of soil (unitless)
    :rtype: float
    """
    compression_index = 0.009 * (liquid_limit - 10)
    return np.round(compression_index, DECIMAL_PLACES)


def hough_compression_index(void_ratio: float) -> float:
    r"""The compression index of the soil estimated from ``Hough`` (1957) relation.

    .. math::

        C_c = 0.29 \left(e_o - 0.27 \right)

    :Example:

        >>> hough_compression_index(0.3)
        0.01
        >>> hough_compression_index(0.5)
        0.07
        >>> hough_compression_index(0.27)
        0.0

    :param void_ratio: Volume of voids divided by volume of solids (unitless)
    :type void_ratio: float
    :return: compression index of soil (unitless)
    :rtype: float
    """
    compression_index = 0.29 * (void_ratio - 0.27)
    return np.round(compression_index, DECIMAL_PLACES)


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

    :param spt_n60: The SPT N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :return: Elastic modulus of the soil :math:`kN/m^2`
    :rtype: float
    """
    _elastic_modulus = 320 * (spt_n60 + 15)
    return np.round(_elastic_modulus, DECIMAL_PLACES)


@deg2rad("friction_angle")
def foundation_depth(
    allowable_bearing_capacity: float,
    unit_weight_of_soil: float,
    *,
    friction_angle: float,
) -> float:
    r"""Depth of foundation estimated using ``Rankine's`` formula.

    .. math::

        D_f=\dfrac{Q_{all}}{\gamma}\left(\dfrac{1 - \sin \phi}{1 + \sin \phi}\right)^2

    :param allowable_bearing_capacity: Allowable bearing capacity
    :type allowable_bearing_capaciy: float
    :param unit_weight_of_soil: Unit weight of soil :math:`kN/m^3`
    :type unit_weight_of_soil: float
    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    :return: Depth of foundation
    :rtype: float
    """
    first_expr = allowable_bearing_capacity / unit_weight_of_soil
    second_expr = (1 - np.sin(friction_angle)) / (1 + np.sin(friction_angle))
    _foundation_depth = first_expr * (second_expr**2)

    return np.round(_foundation_depth, DECIMAL_PLACES)


def friction_angle(
    spt_n60,
    effective_overburden_pressure: Optional[float] = None,
    atmospheric_pressure: Optional[float] = None,
) -> float:
    r"""Estimation of the internal angle of friction using spt_n60.

    For cohesionless soils the coefficient of internal friction :math:`\phi` was
    determined from the minimum value from ``Peck, Hanson and Thornburn (1974)``
    and ``Kullhawy and Mayne (1990)`` respectively. The correlations are shown below.

    .. math::

        \phi = 27.1 + 0.3 \times N_{60} - 0.00054 \times (N_{60})^2

        \phi = \tan^{-1}\left[\dfrac{N_{60}}{12.2 + 20.3(\frac{\sigma_o}{P_a})} \right]^0.34

    :Example:

        >>> friction_angle(20)
        32.88
        >>> friction_angle(30)
        35.61
        >>> friction_angle(30, 18, 40)
        0.98
        >>> friction_angle(20, 18, 20)
        0.83
        >>> friction_angle(40, 10, 30)
        1.04

    :param spt_n60: The SPT N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :param effective_overburden_pressure: Effective overburden pressure :math:`kN/m^2`, defaults to None
    :type effective_overburden_pressure: float, optional
    :param atmospheric_pressure: Atmospheric pressure :math:`kN/m^2`, defaults to None
    :type atmospheric_pressure: float, optional
    :return: The internal angle of friction in degrees
    :rtype: float
    """
    if (effective_overburden_pressure is not None) and (
        atmospheric_pressure is not None
    ):
        den = 12.2 + 20.3 * (effective_overburden_pressure / atmospheric_pressure)
        phi = np.arctan(spt_n60 / den) ** 0.34
        return np.round(phi, 2)

    phi = 27.1 + (0.3 * spt_n60) - (0.00054 * (spt_n60**2))

    # rounded to 2 d.p for consistency with eng. practices
    return np.round(phi, DECIMAL_PLACES)


def stroud_undrained_shear_strength(spt_n60: float, k: float = 3.5) -> float:
    r"""Undrained shear strength estimated from the correlation developed by ``Stroud``
    in 1974.

    .. math::

        C_u = K \times N_{60}

    :Example:

        >>> stroud_undrained_shear_strength(20)
        70.0
        >>> stroud_undrained_shear_strength(30, 4)
        120
        >>> stroud_undrained_shear_strength(40, 2.5)
        Traceback (most recent call last):
        ...
        ValueError: k should be 3.5 <= k <= 6.5 not 2.5
        >>> stroud_undrained_shear_strength(40, 7.5)
        Traceback (most recent call last):
        ...
        ValueError: k should be 3.5 <= k <= 6.5 not 7.5

    :param spt_n60: The SPT N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :param k: Stroud Parameter :math:`kN/m^2`, defaults to 3.5
    :type k: float, optional
    :return: undrained shear strength of the soil :math:`kN/m^2`
    :rtype: float
    """
    if not (3.5 <= k <= 6.5):
        raise ValueError(f"k should be 3.5 <= k <= 6.5 not {k}")

    shear_strength = k * spt_n60
    return np.round(shear_strength, DECIMAL_PLACES)


def skempton_undrained_shear_strength(
    effective_overburden_pressure: float, plasticity_index: float
):
    r"""Undrained shear strength estimated from the correlation developed by ``Skempton``
    in 1957.

    The ratio :math:`\frac{C_u}{\sigma_o}` is a constant for a given clay. ``Skempton``
    suggested that a similar constant ratio exists between the undrained shear strength
    of normally consolidated natural deposits and the effective overburden pressure.
    It has been established that the ratio :math:`\frac{C_u}{\sigma_o}` is constant provided the
    plasticity index (PI) of the soil remains constant.

    The relationship is expressed as:

    .. math::

        \dfrac{C_u}{\sigma_o} = 0.11 + 0.0037 \times PI

    The value of the ratio :math:`\frac{C_u}{\sigma_o}` determined in a consolidated-undrained test on
    undisturbed samples is generally greater than actual value because of anisotropic consolidation
    in the field. The actual value is best determined by `in-situ shear vane test`. (:cite:author:`2003:arora`, p. 330)

    :param effective_overburden_pressure: Effective overburden pressure :math:`kN/m^2`
    :type effective_overburden_pressure: float
    :param plasticity_index: Range of water content over which soil remains in plastic condition
    :type plasticity_index: float
    :return: undrained shear strength of the soil :math:`kN/m^2`
    :rtype: float

    References
    ----------

    .. bibliography::
    """
    shear_strength = effective_overburden_pressure * (0.11 + 0.0037 * plasticity_index)
    return np.round(shear_strength, DECIMAL_PLACES)
