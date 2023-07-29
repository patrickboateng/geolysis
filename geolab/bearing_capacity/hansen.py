"""Hansen Bearing Capacity Analysis."""

from typing import Optional

from geolab.bearing_capacity import (
    FootingShape,
    FootingSize,
    FoundationSize,
    _check_footing_dimension,
    _check_footing_shape,
)
from geolab.utils import PI, exp, mul, round_, tan


def _nc(friction_angle: float) -> float:
    return (1 / tan(friction_angle)) * (_nq(friction_angle) - 1)


def _nq(friction_angle: float) -> float:
    return tan(45 + friction_angle / 2) ** 2 * exp(PI * tan(friction_angle))


def _ngamma(friction_angle: float) -> float:
    return 1.8 * (_nq(friction_angle) - 1) * tan(friction_angle)


def _sc(
    footing_shape: FootingShape,
    footing_size: Optional[FootingSize] = None,
) -> float:
    if footing_shape is FootingShape.STRIP_FOOTING:
        return 1.0

    if (
        footing_shape is FootingShape.SQUARE_FOOTING
        or footing_shape is FootingShape.CIRCULAR_FOOTING
    ):
        return 1.3

    if footing_shape is FootingShape.RECTANGULAR_FOOTING:
        _check_footing_dimension(footing_size.width, footing_size.length)

        return 1 + 0.2 * (footing_size.width / footing_size.length)


def _sq(
    footing_shape: FootingShape,
    footing_size: Optional[FootingSize] = None,
) -> float:
    if footing_shape is FootingShape.STRIP_FOOTING:
        return 1.0

    if (
        footing_shape is FootingShape.SQUARE_FOOTING
        or footing_shape is FootingShape.CIRCULAR_FOOTING
    ):
        return 1.2

    if footing_shape is FootingShape.RECTANGULAR_FOOTING:
        _check_footing_dimension(footing_size.width, footing_size.length)

        return 1 + 0.2 * (footing_size.width / footing_size.length)


def _sgamma(
    footing_shape: FootingShape,
    footing_size: Optional[FootingSize] = None,
) -> float:
    if footing_shape is FootingShape.STRIP_FOOTING:
        return 1.0

    if footing_shape is FootingShape.SQUARE_FOOTING:
        return 0.8

    if footing_shape is FootingShape.CIRCULAR_FOOTING:
        return 0.6

    if footing_shape is FootingShape.RECTANGULAR_FOOTING:
        _check_footing_dimension(footing_size.width, footing_size.length)

        return 1 - 0.4 * (footing_size.width / footing_size.length)


def _dc(foundation_size: FoundationSize) -> float:
    return 1 + 0.35 * (
        foundation_size.depth / foundation_size.footing_size.width
    )


def _dq(foundation_size: FoundationSize) -> float:
    return 1 + 0.35 * (
        foundation_size.depth / foundation_size.footing_size.width
    )


def _dgamma() -> float:
    return 1.0


def _ic(
    cohesion: float,
    footing_size: FootingSize,
    beta: float,
) -> float:
    return 1 - (beta) / (
        2 * cohesion * footing_size.width * footing_size.length
    )


def _iq(total_vertical_load: float, beta: float) -> float:
    return 1 - (1.5 * beta) / total_vertical_load


def _igamma(total_vertical_load: float, beta: float) -> float:
    return _iq(total_vertical_load, beta) ** 2


class HansenBearingCapacity:
    """Hansen Bearing Capacity.

    :param cohesion: Cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param unit_weight_of_soil: Unit weight of soil :math:`(kN/m^3)`
    :type unit_weight_of_soil: float
    :param foundation_size: Size of foundation
    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    ::param beta: Inclination of the load on the foundation with
                  respect to the vertical (degrees)
    :type beta: float
    :param total_vertical_load: Total vertical load on foundation
    :type total_vertical_load: float
    :param footing_shape: Shape of the footing
    :type footing_shape: float
    """

    def __init__(
        self,
        cohesion: float,
        unit_weight_of_soil: float,
        foundation_size: FoundationSize,
        friction_angle: float,
        beta: float,
        total_vertical_load: float,
        footing_shape: FootingShape = FootingShape.SQUARE_FOOTING,
    ) -> None:
        _check_footing_shape(footing_shape)

        self.cohesion = cohesion
        self.unit_weight_of_soil = unit_weight_of_soil
        self.foundation_size = foundation_size
        self.friction_angle = friction_angle
        self.beta = beta
        self.total_vertical_load = total_vertical_load
        self.footing_shape = footing_shape

    @round_
    def ultimate_bearing_capacity(self) -> float:
        r"""Ultimate bearing capacity according to ``Hansen``.

        .. math::

            q_u = c N_c S_c d_c i_c + q N_q S_q d_q i_q + 0.5 \gamma B N_\gamma S_\gamma d_\gamma i_\gamma

        :return: ultimate bearing capacity
        :rtype: float
        """
        expr_1 = mul(self.cohesion, self.nc, self.sc, self.dc, self.ic)
        expr_2 = mul(
            self.unit_weight_of_soil,
            self.foundation_depth,
            self.nq,
            self.sq,
            self.dq,
            self.iq,
        )
        expr_3 = mul(
            self.unit_weight_of_soil,
            self.foundation_width,
            self.ngamma,
            self.sgamma,
            self.dgamma,
            self.igamma,
        )
        return expr_1 + expr_2 + (0.5 * expr_3)

    @property
    @round_
    def nc(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_c`.

        .. math::

            N_c = (N_q - 1) \cot \phi

        :return: A `float` representing the bearing capacity factor :math:`N_c`
        :rtype: float
        """
        return _nc(self.friction_angle)

    @property
    @round_
    def nq(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_q`.

        .. math::

            N_q = \tan^2 (45 + \frac{\phi}{2})(e^{\pi \tan \phi})

        :return: A `float` representing the bearing capacity factor :math:`N_q`
        :rtype: float
        """
        return _nq(self.friction_angle)

    @property
    @round_
    def ngamma(self) -> float:
        r"""Vesic Bearing Capacity factor :math:`N_\gamma`.

        .. math::

            N_\gamma = 1.8(N_q - 1) \tan \phi

        :return: A `float` representing the bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        return _ngamma(self.friction_angle)

    @property
    @round_
    def dc(self) -> float:
        r"""Depth factor :math:`d_c`.

        .. math::

            d_q = 1 + 0.35 (\frac{D_f}{B})

        :return: A `float` representing the depth factor :math:`d_c`
        :rtype: float
        """
        return _dc(self.foundation_depth, self.foundation_width)

    @property
    @round_
    def dq(self) -> float:
        r"""Depth factor :math:`d_q`.

        .. math::

            d_q = 1 + 0.35 (\frac{D_f}{B})

        :return: A `float` representing the depth factor :math:`d_q`
        :rtype: float
        """
        return _dq(self.foundation_depth, self.foundation_width)

    @property
    def dgamma(self) -> float:
        r"""Depth factor :math:`d_\gamma`.

        .. math::

            d_\gamma = 1.0

        :return: 1.0
        :rtype: float
        """
        return _dgamma()

    @property
    @round_
    def sc(self) -> float:
        r"""Shape factor :math:`S_c`.

        .. math::

            if \, footing \, shape \, is \, continuous(strip):
                S_c = 1

            if \, footing \, shape \, is \, rectangular:
                S_c = 1 + 0.2 \frac{B}{L}

            if \, footing \, shape \, is \, square:
                S_c = 1.3

            if \, footing \, shape \, is \, circular:
                S_c = 1.3

        :return: A `float` representing the shape factor :math:`S_c`
        :rtype: float
        """
        return _sc(
            self.footing_shape,
            self.foundation_width,
            self.foundation_length,
        )

    @property
    @round_
    def sq(self) -> float:
        r"""Shape factor :math:`S_q`.

        .. math::

            if \, footing \, shape \, is \, continuous(strip):
                S_q = 1

            if \, footing \, shape \, is \, rectangular:
                S_q = 1 + 0.2 \frac{B}{L}

            if \, footing \, shape \, is \, square:
                S_q = 1.2

            if \, footing \, shape \, is \, circular:
                S_q = 1.2

        :return: A `float` representing the shape factor :math:`S_q`
        :rtype: float
        """
        return _sq(
            self.footing_shape,
            self.foundation_width,
            self.foundation_length,
        )

    @property
    @round_
    def sgamma(self) -> float:
        r"""Shape factor :math:`S_\gamma`.

        .. math::

            if \, footing \, shape \, is \, continuous(strip):
                S_\gamma = 1

            if \, footing \, shape \, is \, rectangular:
                S_\gamma = 1 - 0.4 \frac{B}{L}

            if \, footing \, shape \, is \, square:
                S_\gamma = 0.8

            if \, footing \, shape \, is \, circular:
                S_q = 0.6

        :return: A `float` representing the shape factor :math:`S_\gamma`
        :rtype: float
        """
        return _sgamma(
            self.footing_shape,
            self.foundation_width,
            self.foundation_length,
        )

    @property
    @round_
    def ic(self) -> float:
        r"""Inclination factor :math:`i_c`.

        .. math::

            i_c = 1 - \frac{\beta}{2cBL}

        :return: A `float` representing the inclination factor :math:`i_c`
        :rtype: float
        """
        return _ic(
            self.cohesion,
            self.foundation_width,
            self.foundation_length,
            self.beta,
        )

    @property
    @round_
    def iq(self) -> float:
        r"""Inclination factor :math:`i_q`.

        .. math::

            i_q = 1 - 1.5 \times \frac{\beta}{V}

        :return: A `float` representing the inclination factor :math:`i_q`
        :rtype: float
        """
        return _iq(self.total_vertical_load, self.beta)

    @property
    @round_
    def igamma(self) -> float:
        r"""Inclination factor :math:`i_\gamma`.

        .. math::

            i_\gamma = (1 - 1.5 \times \frac{\beta}{V})^2

        :return: A `float` representing the inclination factor :math:`i_\gamma`
        :rtype: float
        """
        return _igamma(self.total_vertical_load, self.beta)
