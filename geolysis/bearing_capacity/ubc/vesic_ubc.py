from geolysis.foundation import Shape
from geolysis.utils import isclose, round_, sin, tan

from . import hansen_ubc
from ._core import UltimateBearingCapacity

__all__ = ["VesicUltimateBearingCapacity"]


@round_(ndigits=2)
def n_c(friction_angle: float) -> float:
    return hansen_ubc.n_c(friction_angle)


@round_(ndigits=2)
def n_q(friction_angle: float) -> float:
    return hansen_ubc.n_q(friction_angle)


@round_(ndigits=2)
def n_gamma(friction_angle: float) -> float:
    return 2.0 * (n_q(friction_angle) + 1.0) * tan(friction_angle)


@round_(ndigits=2)
def s_c(friction_angle: float,
        f_width: float,
        f_length: float,
        f_shape: Shape) -> float:
    _n_q = n_q(friction_angle)
    _n_c = n_c(friction_angle)

    if f_shape == Shape.STRIP:
        return 1.0
    elif f_shape == Shape.RECTANGLE:
        return 1.0 + (f_width / f_length) * (_n_q / _n_c)
    else:  # SQUARE, CIRCLE
        return 1.0 + (_n_q / _n_c)


@round_(ndigits=2)
def s_q(friction_angle: float,
        f_width: float,
        f_length: float,
        f_shape: Shape) -> float:
    if f_shape == Shape.STRIP:
        return 1.0
    elif f_shape == Shape.RECTANGLE:
        return 1.0 + (f_width / f_length) * tan(friction_angle)
    else:  # SQUARE, CIRCLE
        return 1.0 + tan(friction_angle)


@round_(ndigits=2)
def s_gamma(f_width: float, f_length: float, f_shape: Shape) -> float:
    if f_shape == Shape.STRIP:
        return 1.0
    elif f_shape == Shape.RECTANGLE:
        return 1.0 - 0.4 * (f_width / f_length)
    else:  # SQUARE, CIRCLE
        return 0.6


@round_(ndigits=2)
def d_c(f_depth: float, f_width: float) -> float:
    return 1.0 + 0.4 * f_depth / f_width


@round_(ndigits=2)
def d_q(friction_angle: float, f_depth: float, f_width: float) -> float:
    return (1.0 + 2.0 * tan(friction_angle)
            * (1.0 - sin(friction_angle)) ** 2.0
            * (f_depth / f_width))


@round_(ndigits=2)
def d_gamma() -> float:
    return 1.0


@round_(ndigits=2)
def i_c(load_angle: float) -> float:
    return (1.0 - load_angle / 90.0) ** 2.0


@round_(ndigits=2)
def i_q(load_angle: float) -> float:
    return i_c(load_angle)


@round_(ndigits=2)
def i_gamma(friction_angle: float, load_angle: float) -> float:
    if isclose(friction_angle, 0.0):
        return 1.0
    return (1.0 - load_angle / friction_angle) ** 2.0


class VesicUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for soils according to ``Vesic (1973)``.

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

        .. math:: N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot
                      e^{\pi \tan(\phi)}
        """
        return n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.

        :Equation:

        .. math:: N_{\gamma} = 2(N_q + 1) \tan(\phi)
        """
        return n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        r"""Shape factor :math:`S_c`.

        :Equation:

        .. math::

             s_c &= 1.0 \rightarrow \text{Strip footing}

             s_c &= 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c} \rightarrow
                     \text{Rectangular footing}

             s_c &= 1 + \dfrac{N_q}{N_c} \rightarrow
                       \text{Square or circular footing}
        """
        width, length, shape = self.foundation_size.footing_params()
        return s_c(self.friction_angle, width, length, shape)

    @property
    def s_q(self) -> float:
        r"""Shape factor :math:`S_q`.

        :Equation:

        .. math::

             s_q &= 1.0 \rightarrow \text{Strip footing}

             s_q &= 1 + \dfrac{B}{L} \cdot \tan(\phi) \rightarrow
                    \text{Rectangular footing}

             s_q &= 1 + \tan(\phi) \rightarrow \text{Square or circular footing}
        """
        width, length, shape = self.foundation_size.footing_params()
        return s_q(self.friction_angle, width, length, shape)

    @property
    def s_gamma(self) -> float:
        r"""Shape factor :math:`S_{\gamma}`.

        :Equation:

        .. math::

             s_{\gamma} &= 1.0 \rightarrow \text{Strip footing}

             s_{\gamma} &= 1.0 - 0.4 \dfrac{B}{L} \rightarrow
                          \text{Rectangular footing}

             s_{\gamma} &= 0.6 \rightarrow \text{Square or circular footing}
        """
        width, length, shape = self.foundation_size.footing_params()
        return s_gamma(width, length, shape)

    @property
    def d_c(self) -> float:
        r"""Depth factor :math:`D_c`.

        :Equation:

        .. math:: d_c = 1 + 0.4 \dfrac{D_f}{B}
        """
        depth, width = self.foundation_size.depth, self.foundation_size.width
        return d_c(depth, width)

    @property
    def d_q(self) -> float:
        r"""Depth factor :math:`D_q`.

        :Equation:

        .. math::

            d_q = 1 + 2 \tan(\phi) \cdot (1 - \sin(\phi))^2
                  \cdot \dfrac{D_f}{B}
        """
        depth, width = self.foundation_size.depth, self.foundation_size.width
        return d_q(self.friction_angle, depth, width)

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

        .. math:: i_c = (1 - \dfrac{\alpha}{90})^2
        """
        return i_c(self.load_angle)

    @property
    def i_q(self) -> float:
        r"""Inclination factor :math:`I_q`.

        :Equation:

        .. math:: i_q = (1 - \dfrac{\alpha}{90})^2
        """
        return i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor :math:`I_{\gamma}`.

        :Equation:

        .. math:: i_{\gamma} = \left(1 - \dfrac{\alpha}{\phi} \right)^2
        """
        return i_gamma(self.friction_angle, self.load_angle)
