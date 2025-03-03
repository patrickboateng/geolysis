""" Hansen ultimate bearing capacity module.

Classes
=======

.. autosummary::
    :toctree: _autosummary

    HansenUltimateBearingCapacity

Functions
=========

.. autosummary::
    :toctree: _autosummary

    n_c
    n_q
    n_gamma
    s_c
    s_q
    s_gamma
    d_c
    d_q
    d_gamma
    i_c
    i_q
    i_gamma
"""
from geolysis.bearing_capacity.ubc import UltimateBearingCapacity
from geolysis.foundation import FoundationSize, Shape
from geolysis.utils import cos, cot, exp, isclose, pi, round_, sin, tan

__all__ = ["HansenUltimateBearingCapacity"]


@round_
def n_c(friction_angle: float) -> float:
    r"""Bearing capacity factor :math:`N_c`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :Equation:

    .. math:: N_c = \cot(\phi) \left(N_q - 1\right)
    """
    if isclose(friction_angle, 0.0):
        return 5.14
    return cot(friction_angle) * (n_q(friction_angle) - 1.0)


@round_
def n_q(friction_angle: float) -> float:
    r"""Bearing capacity factor :math:`N_q`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :Equation:

    .. math::

        N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot e^{\pi \tan(\phi)}
    """
    return (tan(45.0 + friction_angle / 2.0) ** 2.0
            * exp(pi * tan(friction_angle)))


@round_
def n_gamma(friction_angle: float) -> float:
    r"""Bearing capacity factor :math:`N_{\gamma}`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :Equation:

    .. math:: N_{\gamma} = 1.8 \left(N_q - 1\right) \tan(\phi)
    """
    return 1.8 * (n_q(friction_angle) - 1.0) * tan(friction_angle)


@round_
def s_c(foundation_size: FoundationSize) -> float:
    r"""Shape factor :math:`S_c`.

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math::

        s_c &= 1.0 \rightarrow \text{Strip footing}

        s_c &= 1.0 + 0.2 \frac{B}{L} \rightarrow \text{Rectangular footing}

        s_c &= 1.3 \rightarrow \text{Square or circular footing}
    """
    width, length, shape = foundation_size.footing_params()

    if shape == Shape.STRIP:
        return 1.0
    elif shape == Shape.RECTANGLE:
        return 1.0 + 0.2 * width / length
    else:
        # SQUARE & CIRCLE
        return 1.3


@round_
def s_q(foundation_size: FoundationSize) -> float:
    r"""Shape factor :math:`S_q`.

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math::

        s_q &= 1.0 \rightarrow \text{Strip footing}

        s_q &= 1.0 + 0.2 \frac{B}{L} \rightarrow \text{Rectangular footing}

        s_q &= 1.2 \rightarrow \text{Square or circular footing}
    """
    width, length, shape = foundation_size.footing_params()

    if shape == Shape.STRIP:
        return 1.0
    elif shape == Shape.RECTANGLE:
        return 1.0 + 0.2 * width / length
    else:
        # SQUARE & CIRCLE
        return 1.2


@round_
def s_gamma(foundation_size: FoundationSize) -> float:
    r"""Shape factor :math:`S_{\gamma}`.

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math::

        s_{\gamma} &= 1.0 \rightarrow \text{Strip footing}

        s_{\gamma} &= 1.0 - 0.4 \frac{B}{L} \rightarrow
                      \text{Rectangular footing}

        s_{\gamma} &= 0.8 \rightarrow \text{Square footing}

        s_{\gamma} &= 0.6 \rightarrow \text{Circular footing}
    """
    width, length, shape = foundation_size.footing_params()

    if shape == Shape.STRIP:
        return 1.0
    elif shape == Shape.RECTANGLE:
        return 1.0 - 0.4 * width / length
    elif shape == Shape.SQUARE:
        return 0.8
    else:
        # CIRCLE
        return 0.6


@round_
def d_c(foundation_size: FoundationSize) -> float:
    r"""Depth factor :math:`D_c`.

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math:: d_c = 1.0 + 0.35 \cdot \frac{D_f}{B}
    """
    depth = foundation_size.depth
    width = foundation_size.width

    return 1.0 + 0.35 * depth / width


@round_
def d_q(foundation_size: FoundationSize) -> float:
    r"""Depth factor :math:`D_q`.

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math:: d_q = 1.0 + 0.35 \cdot \frac{D_f}{B}
    """
    return d_c(foundation_size)


@round_
def d_gamma() -> float:
    r"""Depth factor :math:`D_{\gamma}`.

    :Equation:

    .. math:: d_{\gamma} = 1.0
    """
    return 1.0


@round_
def i_c(cohesion: float,
        load_angle: float,
        foundation_size: FoundationSize) -> float:
    r"""Inclination factor :math:`I_c`.

    :param cohesion: Cohesion of the soil between footing and soil (kPa).
    :type cohesion: float

    :param load_angle: Inclination of the applied load with the vertical
                       (degrees)
    :type load_angle: float

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math:: I_c = 1 - \frac{\sin(\alpha)}{2cBL}
    """
    width = foundation_size.width
    length = foundation_size.length

    return 1.0 - sin(load_angle) / (2.0 * cohesion * width * length)


@round_
def i_q(load_angle: float) -> float:
    r"""Inclination factor :math:`I_q`.

    :param load_angle: Inclination of the applied load with the vertical
                       (degrees).
    :type load_angle: float

    :Equation:

    .. math:: I_q = 1 - \frac{1.5 \sin(\alpha)}{\cos(\alpha)}
    """
    return 1.0 - (1.5 * sin(load_angle)) / cos(load_angle)


@round_
def i_gamma(load_angle: float) -> float:
    r"""Inclination factor :math:`I_{\gamma}`.

    :param load_angle: Inclination of the applied load with the vertical
                       (degrees).
    :type load_angle: float

    :Equation:

    .. math:: I_{\gamma} = I_q^2
    """
    return i_q(load_angle) ** 2.0


class HansenUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for soils according to ``Hansen (1961)``.

    .. math::

            q_u = cN_c s_c d_c i_c + qN_q s_q d_q i_q
                  + 0.5 \gamma B N_{\gamma} s_{\gamma} d_{\gamma}
    """

    @property
    def n_c(self) -> float:
        return n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        return n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        return n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        return s_c(self.foundation_size)

    @property
    def s_q(self) -> float:
        return s_q(self.foundation_size)

    @property
    def s_gamma(self) -> float:
        return s_gamma(self.foundation_size)

    @property
    def d_c(self) -> float:
        return d_c(self.foundation_size)

    @property
    def d_q(self) -> float:
        return d_q(self.foundation_size)

    @property
    def d_gamma(self) -> float:
        return d_gamma()

    @property
    def i_c(self) -> float:
        return i_c(self.cohesion, self.load_angle, self.foundation_size)

    @property
    def i_q(self) -> float:
        return i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        return i_gamma(self.load_angle)

    @round_
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity."""
        return super().bearing_capacity()
