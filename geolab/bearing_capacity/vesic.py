"""Vesic Bearing Capacity Analysis."""

from typing import Optional

from geolab.bearing_capacity import (
    BearingCapacity,
    FootingShape,
    FootingSize,
    FoundationSize,
    _check_footing_dimension,
)
from geolab.utils import PI, exp, mul, round_, sin, tan


def _nc(friction_angle: float) -> float:
    return (1 / tan(friction_angle)) * (_nq(friction_angle) - 1)


def _nq(friction_angle: float) -> float:
    return tan(45 + friction_angle / 2) ** 2 * exp(PI * tan(friction_angle))


def _ngamma(friction_angle: float) -> float:
    return 2 * (_nq(friction_angle) + 1) * tan(friction_angle)


def _sc(
    friction_angle: float,
    footing_shape: FootingShape,
    footing_size: Optional[FootingSize] = None,
) -> float:
    if footing_shape is FootingShape.STRIP_FOOTING:
        return 1.0

    if (
        footing_shape is FootingShape.SQUARE_FOOTING
        or footing_shape is FootingShape.CIRCULAR_FOOTING
    ):
        return 1 + _nq(friction_angle) / _nc(friction_angle)

    if footing_shape is FootingShape.RECTANGULAR_FOOTING:
        _check_footing_dimension(footing_size.width, footing_size.length)

        return 1 + (footing_size.width / footing_size.length) * (
            _nq(friction_angle) / _nc(friction_angle)
        )


def _sq(
    friction_angle: float,
    footing_shape: FootingShape,
    footing_size: Optional[FootingSize] = None,
) -> float:
    if footing_shape is FootingShape.STRIP_FOOTING:
        return 1.0

    if (
        footing_shape is FootingShape.SQUARE_FOOTING
        or footing_shape is FootingShape.CIRCULAR_FOOTING
    ):
        return 1 + tan(friction_angle)

    if footing_shape is FootingShape.RECTANGULAR_FOOTING:
        _check_footing_dimension(footing_size.width, footing_size.length)

        return 1 + (footing_size.width / footing_size.length) * tan(
            friction_angle
        )


def _sgamma(
    footing_shape: FootingShape,
    footing_size: Optional[FootingSize] = None,
) -> float:
    if footing_shape is FootingShape.STRIP_FOOTING:
        return 1.0

    if (
        footing_shape is FootingShape.SQUARE_FOOTING
        or footing_shape is FootingShape.CIRCULAR_FOOTING
    ):
        return 0.6

    if footing_shape is FootingShape.RECTANGULAR_FOOTING:
        _check_footing_dimension(footing_size.width, footing_size.length)

        return 1 - 0.4 * (footing_size.width / footing_size.length)


def _dc(foundation_size: FoundationSize) -> float:
    return 1 + 0.4 * (
        foundation_size.depth / foundation_size.footing_size.width
    )


def _dq(friction_angle, foundation_size: FoundationSize) -> float:
    return 1 + mul(
        2,
        tan(friction_angle),
        pow(1 - sin(friction_angle), 2),
        foundation_size.depth / foundation_size.footing_size.width,
    )


def _dgamma() -> float:
    return 1.0


def _ic(beta: float) -> float:
    return pow((1 - beta / 90), 2)


def _iq(beta: float) -> float:
    return _ic(beta)


def _igamma(friction_angle: float, beta: float) -> float:
    return pow((1 - beta / friction_angle), 2)


class VesicBearingCapacity(BearingCapacity):
    """Vesic Bearing Capacity.

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
    :param total_vertical_load: total vertical load on foundation
    :type total_vertical_load: float
    :param footing_shape: Shape of the footing
    :type footing_shape: float
    """

    def __init__(
        self,
        cohesion: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        friction_angle: float,
        beta: float,
        footing_shape: FootingShape = FootingShape.SQUARE_FOOTING,
    ) -> None:
        super().__init__(
            cohesion,
            soil_unit_weight,
            foundation_size,
            friction_angle,
            beta,
            footing_shape,
        )

    def ultimate_bearing_capacity(self) -> float:
        r"""Ultimate bearing capacity according to ``Vesic``.

        .. math::

            q_u = c N_c S_c d_c i_c + q N_q S_q d_q i_q + 0.5 \gamma B N_\gamma S_\gamma d_\gamma i_\gamma

        :return: ultimate bearing capacity
        :rtype: float
        """
        return super().ultimate_bearing_capacity()

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

            N_\gamma = 2(N_q + 1) \tan \phi

        :return: A `float` representing the bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        return _ngamma(self.friction_angle)

    @property
    @round_
    def dc(self) -> float:
        r"""Depth factor :math:`d_c`.

        .. math::

            d_q = 1 + 0.4 (\frac{D_f}{B})

        :return: A `float` representing the depth factor :math:`d_c`
        :rtype: float
        """
        return _dc(self.foundation_size)

    @property
    @round_
    def dq(self) -> float:
        r"""Depth factor :math:`d_q`.

        .. math::

            d_q = 1 + 2 \tan \phi (1 - \sin \phi)^2 \frac{D_f}{B}

        :return: A `float` representing the depth factor :math:`d_q`
        :rtype: float
        """
        return _dq(self.friction_angle, self.foundation_size)

    @property
    @round_
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
                S_c = 1 + \frac{B}{L} \frac{N_q}{N_c}

            if \, footing \, shape \, is \, square \, or \, circular:
                S_c = 1 + (\frac{N_q}{N_c})

        :return: A `float` representing the shape factor :math:`S_c`
        :rtype: float
        """
        return _sc(
            self.friction_angle,
            self.footing_shape,
            self.foundation_size.footing_size,
        )

    @property
    @round_
    def sq(self) -> float:
        r"""Shape factor :math:`S_q`.

        .. math::

            if \, footing \, shape \, is \, continuous(strip):
                S_q = 1

            if \, footing \, shape \, is \, rectangular:
                S_q = 1 + \frac{B}{L} \tan \phi

            if \, footing \, shape \, is \, square \, or \, circular:
                S_c = 1 + \tan \phi

        :return: A `float` representing the shape factor :math:`S_q`
        :rtype: float
        """
        return _sq(
            self.friction_angle,
            self.footing_shape,
            self.foundation_size.footing_size,
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

            if \, footing \, shape \, is \, square \, or \, circular:
                S_\gamma = 0.6

        :return: A `float` representing the shape factor :math:`S_\gamma`
        :rtype: float
        """
        return _sgamma(self.friction_angle, self.foundation_size.footing_size)

    @property
    @round_
    def ic(self) -> float:
        r"""Inclination factor :math:`i_c`.

        .. math::

            i_c = (1 - \frac{\beta}{90})^2

        :return: A `float` representing the inclination factor :math:`i_c`
        :rtype: float
        """
        return _ic(self.beta)

    @property
    @round_
    def iq(self) -> float:
        r"""Inclination factor :math:`i_q`.

        .. math::

            i_q = (1 - \frac{\beta}{90})^2

        :return: A `float` representing the inclination factor :math:`i_q`
        :rtype: float
        """
        return _iq(self.beta)

    @property
    @round_
    def igamma(self) -> float:
        r"""Inclination factor :math:`i_\gamma`.

        .. math::

            i_\gamma = (1 - \frac{\beta}{\phi})^2

        :return: A `float` representing the inclination factor :math:`i_\gamma`
        :rtype: float
        """
        return _igamma(self.friction_angle, self.beta)
