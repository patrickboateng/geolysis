from operator import truediv as div
from typing import Sequence

from .foundation import (
    CircularFooting,
    FoundationSize,
    RectangularFooting,
    SquareFooting,
    _FootingShape,
)
from .utils import PI, FloatOrInt, log, log10, round_, sqrt


@round_(ndigits=2)
def influence_factor(footing_shape: _FootingShape) -> float:
    r"""Influence factor.

    :param _FootingShape footing_shape: Shape of foundation footing.

    .. math::

        I = \frac{1}{\pi}\left[\ln(\frac{\sqrt{1 + m^2} + m}{\sqrt{1 + m^2} - m})
            + m \cdot \ln(\frac{\sqrt{1 + m^2} + 1}{\sqrt{1 + m^2} - 1})\right]
    """
    m = footing_shape.length / footing_shape.width
    root = sqrt(1 + m**2)
    return (1 / PI) * (
        log(div(root + m, root - m)) + m * log(div(root + 1, root - 1))
    )


@round_(ndigits=3)
def corr_factor_4_depth(
    surcharge: FloatOrInt, pressure_at_foundation_level: FloatOrInt
) -> float:
    return 1 - 0.5 * div(surcharge, pressure_at_foundation_level - surcharge)


@round_(ndigits=3)
def corr_factor_4_creep(time: FloatOrInt):
    return 1 + 0.2 * log10(time / 0.1)


@round_(ndigits=2)
def immediate_settlement_coh(
    udl: FloatOrInt,
    elastic_mod: FloatOrInt,
    poisson_ratio: float,
    foundation_size: FoundationSize,
    embedded=False,
) -> float:
    r"""
    Immediate settlement for cohesive soils by ``Schleicher (1926)``.

    :param FloatOrInt udl: Uniformly distributed load. (kN/m2)
    :param FloatOrInt elastic_mod: Elastic modulus of soil. (kN/m2)
    :param float poisson_ratio: Poisson ratio
    :param FoundationSize foundation_size: Size of foundation.
    :param bool embedded: Indicates whether footing is embedded in the
                          soil or not. Defaults to False.

    :return: Settlement. (mm)
    :rtype: float

    .. math::

        S_i = qB\left(\dfrac{1 - \mu^2}{E_s} \right) I

    The equation above is applicable for footings located at the surface.
    For footings embedded in soil, the settlement would be less than the
    computed values. ``Fox (1948)`` gave correction curves. The settlement
    is obtained by multiplying the computed settlements by a depth factor
    which depends upon (:math:`\frac{D_f}{\sqrt{L \times B}}`) ratio.
    """
    I = influence_factor(foundation_size.footing_size)
    B = foundation_size.footing_size.width
    settlement = udl * B * div(1 - poisson_ratio**2, elastic_mod) * I

    if embedded:
        L = foundation_size.footing_size.length
        settlement *= foundation_size.depth / sqrt(L * B)

    return settlement * 1000


def immediate_settlement_cohl(
    surcharge: FloatOrInt,
    pressure_at_foundation_level: FloatOrInt,
    time: FloatOrInt,
    elastic_mods: Sequence[float],
    strain_influence_factors: Sequence[float],
    footing_shape: _FootingShape,
):
    r"""
    Immediate settlement for cohesionless soils.

    :param surcharge: Weight of the soil above the foundation base. This is
                     equivalent to :math:`\gamma D_f`.
    :param FloatOrInt pressure_at_foundation_level: Pressure exerted on the soil
                                                    at the foundation base.
    :param Sequence[float] elastic_mods: Variation of elastic modulus with depth.
    :param Sequence[float] strain_influence_factors: Variation of Strain influence
                                                     factors with depth.
    :param FloatOrInt time: Time in years to determine the settlement.

    :return: Settlement. (mm)
    :rtype: float

    .. note::

        ``elastic_mods`` and ``strain_influence_factors`` should have the same
        length and the length should be equal to ``2B`` for square footings and
        ``4B`` for rectangular footings.

    .. math::

        S_i = C_1 C_2 (\overline{q} - q) \sum^{2B}_{z=0} \frac{I_z}{E_s}\Delta z
    """

    C_1 = corr_factor_4_depth(surcharge, pressure_at_foundation_level)
    C_2 = corr_factor_4_creep(time)

    coef = C_1 * C_2 * (pressure_at_foundation_level - surcharge)
    total = 0.0

    if isinstance(footing_shape, (SquareFooting, CircularFooting)):
        stop = 2 * footing_shape.width
    elif isinstance(footing_shape, RectangularFooting):
        stop = 4 * footing_shape.width
    else:
        raise

    try:
        for idx in range(round(stop)):
            total += strain_influence_factors[idx] / elastic_mods[idx]
    except IndexError as e:
        raise

    return coef * total * 1000
