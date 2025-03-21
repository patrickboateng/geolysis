from geolysis.foundation import Shape
from geolysis.utils import cos, cot, exp, isclose, pi, round_, sin, tan

from ._core import UltimateBearingCapacity

__all__ = ["HansenUltimateBearingCapacity"]


@round_
def n_c(friction_angle: float) -> float:
    if isclose(friction_angle, 0.0):
        return 5.14
    return cot(friction_angle) * (n_q(friction_angle) - 1.0)


@round_
def n_q(friction_angle: float) -> float:
    return (tan(45.0 + friction_angle / 2.0) ** 2.0
            * exp(pi * tan(friction_angle)))


@round_
def n_gamma(friction_angle: float) -> float:
    return 1.8 * (n_q(friction_angle) - 1.0) * tan(friction_angle)


@round_
def s_c(f_width: float, f_length: float, f_shape: Shape) -> float:
    if f_shape == Shape.STRIP:
        return 1.0
    elif f_shape == Shape.RECTANGLE:
        return 1.0 + 0.2 * f_width / f_length
    else:  # SQUARE & CIRCLE
        return 1.3


@round_
def s_q(f_width: float, f_length: float, f_shape: Shape) -> float:
    if f_shape == Shape.STRIP:
        return 1.0
    elif f_shape == Shape.RECTANGLE:
        return 1.0 + 0.2 * f_width / f_length
    else:  # SQUARE & CIRCLE
        return 1.2


@round_
def s_gamma(f_width: float, f_length: float, f_shape: Shape) -> float:
    if f_shape == Shape.STRIP:
        return 1.0
    elif f_shape == Shape.RECTANGLE:
        return 1.0 - 0.4 * f_width / f_length
    elif f_shape == Shape.SQUARE:
        return 0.8
    else:  # CIRCLE
        return 0.6


@round_
def d_c(f_depth: float, f_width: float) -> float:
    return 1.0 + 0.35 * f_depth / f_width


@round_
def d_q(f_depth: float, f_width: float) -> float:
    return d_c(f_depth, f_width)


@round_
def d_gamma() -> float:
    return 1.0


@round_
def i_c(cohesion: float,
        load_angle: float,
        f_width: float,
        f_length: float) -> float:
    return 1.0 - sin(load_angle) / (2.0 * cohesion * f_width * f_length)


@round_
def i_q(load_angle: float) -> float:
    return 1.0 - (1.5 * sin(load_angle)) / cos(load_angle)


@round_
def i_gamma(load_angle: float) -> float:
    return i_q(load_angle) ** 2.0


class HansenUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for soils according to ``Hansen (1961)``.

    :Equation:

    .. math::

            q_u = cN_c s_c d_c i_c + qN_q s_q d_q i_q
                  + 0.5 \gamma B N_{\gamma} s_{\gamma} d_{\gamma} i_{\gamma}

    .. list-table::
       :widths: auto
       :header-rows: 1

       * - Symbol
         - Description
         - Unit
       * - :math:`q_u`
         - Ultimate bearing capacity
         - :math:`kPa`
       * - :math:`c`
         - Cohesion of soil
         - :math:`kPa`
       * - :math:`q`
         - Overburden pressure of soil
         - :math:`kPa`
       * - :math:`\gamma`
         - Unit weight of soil
         - :math:`kN/m^3`
       * - :math:`B`
         - Width of foundation footing
         - :math:`m`
       * - :math:`N_c`, :math:`N_q`, :math:`N_{\gamma}`
         - Bearing capacity factors
         - —
       * - :math:`s_c`, :math:`s_q`, :math:`s_{\gamma}`
         - Shape factors
         - —
       * - :math:`d_c`, :math:`d_q`, :math:`d_{\gamma}`
         - Depth factors
         - —
       * - :math:`i_c`, :math:`i_q`, :math:`i_{\gamma}`
         - Inclination factors
         - —
    """

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor :math:`N_c`.

        :Equation:

        .. math:: N_c = \cot(\phi) \left(N_q - 1\right)
        """
        return n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor :math:`N_q`.

        :Equation:

        .. math::

            N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot e^{\pi \tan(\phi)}
        """
        return n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.

        :Equation:

        .. math:: N_{\gamma} = 1.8 \left(N_q - 1\right) \tan(\phi)
        """
        return n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        r"""Shape factor :math:`S_c`.

        :Equation:

        .. math::

            s_c &= 1.0 \rightarrow \text{Strip footing}

            s_c &= 1.0 + 0.2 \frac{B}{L} \rightarrow \text{Rectangular footing}

            s_c &= 1.3 \rightarrow \text{Square or circular footing}
        """
        width, length, shape = self.foundation_size.footing_params()
        return s_c(width, length, shape)

    @property
    def s_q(self) -> float:
        r"""Shape factor :math:`S_q`.

        :Equation:

        .. math::

            s_q &= 1.0 \rightarrow \text{Strip footing}

            s_q &= 1.0 + 0.2 \frac{B}{L} \rightarrow \text{Rectangular footing}

            s_q &= 1.2 \rightarrow \text{Square or circular footing}
        """
        width, length, shape = self.foundation_size.footing_params()
        return s_q(width, length, shape)

    @property
    def s_gamma(self) -> float:
        r"""Shape factor :math:`S_{\gamma}`.

        :Equation:

        .. math::

            s_{\gamma} &= 1.0 \rightarrow \text{Strip footing}

            s_{\gamma} &= 1.0 - 0.4 \frac{B}{L} \rightarrow
                          \text{Rectangular footing}

            s_{\gamma} &= 0.8 \rightarrow \text{Square footing}

            s_{\gamma} &= 0.6 \rightarrow \text{Circular footing}
        """
        width, length, shape = self.foundation_size.footing_params()
        return s_gamma(width, length, shape)

    @property
    def d_c(self) -> float:
        r"""Depth factor :math:`D_c`.

        :Equation:

        .. math:: d_c = 1.0 + 0.35 \cdot \frac{D_f}{B}
        """
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        return d_c(depth, width)

    @property
    def d_q(self) -> float:
        r"""Depth factor :math:`D_q`.

        :Equation:

        .. math:: d_q = 1.0 + 0.35 \cdot \frac{D_f}{B}
        """
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        return d_q(depth, width)

    @property
    def d_gamma(self) -> float:
        r"""Depth factor :math:`D_{\gamma}`.

        :Equation:

        .. math:: d_{\gamma} = 1.0
        """
        return d_gamma()

    @property
    def i_c(self) -> float:
        r"""Inclination factor :math:`I_c`.

        :Equation:

        .. math:: I_c = 1 - \frac{\sin(\alpha)}{2cBL}
        """
        width, length = self.foundation_size.width, self.foundation_size.length
        return i_c(self.cohesion, self.load_angle, width, length)

    @property
    def i_q(self) -> float:
        r"""Inclination factor :math:`I_q`.

        :Equation:

        .. math:: I_q = 1 - \frac{1.5 \sin(\alpha)}{\cos(\alpha)}
        """
        return i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor :math:`I_{\gamma}`.

        :Equation:

        .. math:: I_{\gamma} = I_q^2
        """
        return i_gamma(self.load_angle)
