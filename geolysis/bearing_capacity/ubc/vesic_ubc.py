"""Vesic ultimate bearing capacity module.

Classes
=======

.. autosummary::
    :toctree: _autosummary

    VesicUltimateBearingCapacity

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
from geolysis.bearing_capacity.ubc import hansen_ubc
from geolysis.foundation import FoundationSize, Shape
from geolysis.utils import isclose, round_, sin, tan

__all__ = ["VesicUltimateBearingCapacity"]


@round_
def n_c(friction_angle: float) -> float:
    r"""Bearing capacity factor :math:`N_c`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :Equation:

    .. math:: N_c = \cot(\phi) \left(N_q - 1\right)
    """
    return hansen_ubc.n_c(friction_angle)


@round_
def n_q(friction_angle: float) -> float:
    r"""Bearing capacity factor :math:`N_q`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :Equation:

    .. math:: N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot
                  e^{\pi \tan(\phi)}
    """
    return hansen_ubc.n_q(friction_angle)


@round_
def n_gamma(friction_angle: float) -> float:
    r"""Bearing capacity factor :math:`N_{\gamma}`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :Equation:

    .. math:: N_{\gamma} = 2(N_q + 1) \tan(\phi)
    """
    return 2.0 * (n_q(friction_angle) + 1.0) * tan(friction_angle)


@round_
def s_c(friction_angle: float, foundation_size: FoundationSize) -> float:
    r"""Shape factor :math:`S_c`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math::

            s_c &= 1.0 \rightarrow \text{Strip footing}

            s_c &= 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c} \rightarrow
                    \text{Rectangular footing}

            s_c &= 1 + \dfrac{N_q}{N_c} \rightarrow
                   \text{Square or circular footing}
    """
    width, length, shape = foundation_size.footing_params()

    _n_q = n_q(friction_angle)
    _n_c = n_c(friction_angle)

    if shape == Shape.STRIP:
        return 1.0
    elif shape == Shape.RECTANGLE:
        return 1.0 + (width / length) * (_n_q / _n_c)
    else:  # SQUARE, CIRCLE
        return 1.0 + (_n_q / _n_c)


@round_
def s_q(friction_angle: float, foundation_size: FoundationSize) -> float:
    r"""Shape factor :math:`S_q`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math::

            s_q &= 1.0 \rightarrow \text{Strip footing}

            s_q &= 1 + \dfrac{B}{L} \cdot \tan(\phi) \rightarrow
                   \text{Rectangular footing}

            s_q &= 1 + \tan(\phi) \rightarrow \text{Square or circular footing}
    """
    width, length, shape = foundation_size.footing_params()

    if shape == Shape.STRIP:
        return 1.0
    elif shape == Shape.RECTANGLE:
        return 1.0 + (width / length) * tan(friction_angle)
    else:  # SQUARE, CIRCLE
        return 1.0 + tan(friction_angle)


@round_
def s_gamma(foundation_size: FoundationSize) -> float:
    r"""Shape factor :math:`S_{\gamma}`.

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math::

            s_{\gamma} &= 1.0 \rightarrow \text{Strip footing}

            s_{\gamma} &= 1.0 - 0.4 \dfrac{B}{L} \rightarrow
                         \text{Rectangular footing}

            s_{\gamma} &= 0.6 \rightarrow \text{Square or circular footing}
    """
    width, length, shape = foundation_size.footing_params()

    if shape == Shape.STRIP:
        return 1.0
    elif shape == Shape.RECTANGLE:
        return 1.0 - 0.4 * (width / length)
    else:  # SQUARE, CIRCLE
        return 0.6


@round_
def d_c(foundation_size: FoundationSize) -> float:
    r"""Depth factor :math:`D_c`.

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math:: d_c = 1 + 0.4 \dfrac{D_f}{B}
    """
    depth = foundation_size.depth
    width = foundation_size.width
    return 1.0 + 0.4 * depth / width


@round_
def d_q(friction_angle: float, foundation_size: FoundationSize) -> float:
    r"""Depth factor :math:`D_q`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :param foundation_size: Size of the foundation.
    :type foundation_size: FoundationSize

    :Equation:

    .. math::

        d_q = 1 + 2 \tan(\phi) \cdot (1 - \sin(\phi))^2
              \cdot \dfrac{D_f}{B}

    """
    depth = foundation_size.depth
    width = foundation_size.width

    return (1.0 + 2.0 * tan(friction_angle)
            * (1.0 - sin(friction_angle)) ** 2.0
            * (depth / width))


@round_
def d_gamma() -> float:
    r"""Depth factor :math:`D_{\gamma}`.

    :Equation:

    .. math:: d_{\gamma} = 1.0
    """
    return 1.0


@round_
def i_c(load_angle: float) -> float:
    r"""Inclination factor :math:`I_c`.

    :param load_angle: Inclination of the applied load with the  vertical
                       (degrees).
    :type load_angle: float

    :Equation:

    .. math:: i_c = (1 - \dfrac{\alpha}{90})^2
    """
    return (1.0 - load_angle / 90.0) ** 2.0


@round_
def i_q(load_angle: float) -> float:
    r"""Inclination factor :math:`I_q`.

    :param load_angle: Inclination of the applied load with the  vertical
                       (degrees).
    :type load_angle: float

    :Equation:

    .. math:: i_q = (1 - \dfrac{\alpha}{90})^2
    """
    return i_c(load_angle=load_angle)


@round_
def i_gamma(friction_angle: float, load_angle: float) -> float:
    r"""Inclination factor :math:`I_{\gamma}`.

    :param friction_angle: Angle of internal friction of the soil (degrees).
    :type friction_angle: float

    :param load_angle: Inclination of the applied load with the  vertical
                       (degrees).
    :type load_angle: float

    :Equation:

    .. math:: i_{\gamma} = \left(1 - \dfrac{\alpha}{\phi} \right)^2
    """
    if isclose(friction_angle, 0.0):
        return 1.0
    return (1.0 - load_angle / friction_angle) ** 2.0


class VesicUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for soils according to ``Vesic (1973)``.

    :Equation:

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
        return s_c(self.friction_angle, self.foundation_size)

    @property
    def s_q(self) -> float:
        return s_q(self.friction_angle, self.foundation_size)

    @property
    def s_gamma(self) -> float:
        return s_gamma(self.foundation_size)

    @property
    def d_c(self) -> float:
        return d_c(self.foundation_size)

    @property
    def d_q(self) -> float:
        return d_q(self.friction_angle, self.foundation_size)

    @property
    def d_gamma(self) -> float:
        return d_gamma()

    @property
    def i_c(self) -> float:
        return i_c(self.load_angle)

    @property
    def i_q(self) -> float:
        return i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        return i_gamma(self.friction_angle, self.load_angle)
