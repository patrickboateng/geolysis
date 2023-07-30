"""Terzaghi Bearing Capacity Analysis."""

from geolab import GeotechEng
from geolab.bearing_capacity import FootingShape, FoundationSize, _check_footing_shape
from geolab.utils import PI, cos, deg2rad, exp, mul, round_, tan


def _nc(friction_angle: float) -> float:
    num = exp(((3 * PI) / 2 - deg2rad(friction_angle)) * tan(friction_angle))
    den = 2 * (cos(45 + (friction_angle / 2)) ** 2)

    return num / den


def _nq(friction_angle: float) -> float:
    return (1 / tan(friction_angle)) * (_nq(friction_angle) - 1)


def _ngamma(friction_angle: float, eng: GeotechEng = GeotechEng.MEYERHOF):
    if eng is GeotechEng.MEYERHOF:
        return (_nq(friction_angle) - 1) * tan(1.4 * friction_angle)
    if eng is GeotechEng.HANSEN:
        return 1.8 * (_nq(friction_angle) - 1) * tan(friction_angle)
    msg = f"Available types are {GeotechEng.MEYERHOF} or {GeotechEng.HANSEN}"
    raise TypeError(msg)


CONSTANTS = {
    FootingShape.STRIP: 0.5,
    FootingShape.SQUARE: 0.4,
    FootingShape.CIRCULAR: 0.3,
}


class TerzaghiBearingCapacity:
    """Terzaghi Bearing Capacity.

    :param cohesion: cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param friction_angle: internal angle of friction (degrees)
    :type friction_angle: float
    :param soil_unit_weight: unit weight of soil :math:`(kN/m^3)`
    :type soil_unit_weight: float
    :param foundation_depth: depth of foundation :math:`d_f` (m)
    :type foundation_depth: float
    :param foundation_width: width of foundation (**B**) (m)
    :type foundation_width: float
    :param eng: specifies the type of ngamma formula to use. Available
                values are geolab.MEYERHOF and geolab.HANSEN
    :type eng: GeotechEng
    """

    def __init__(
        self,
        cohesion: float,
        friction_angle: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        footing_shape: FootingShape = FootingShape.SQUARE,
        eng: GeotechEng = GeotechEng.MEYERHOF,
    ) -> None:
        _check_footing_shape(footing_shape)

        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.friction_angle = friction_angle
        self.footing_shape = footing_shape
        self.eng = eng

        self.const = 1 if footing_shape is FootingShape.STRIP else 1.2

    @property
    @round_
    def nc(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_c`.

        .. math::

            N_c = \cot \phi \left(N_q - 1 \right)

        :return: The bearing capacity factor :math:`N_c`
        :rtype: float
        """
        return _nc(self.friction_angle)

    @property
    @round_
    def nq(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_q`.

        .. math::

            N_q=\dfrac{e^{(\frac{3\pi}{2}-\phi)\tan\phi}}{2\cos^2\left(45^{\circ}+\frac{\phi}{2}\right)}

        :return: The bearing capacity factor :math:`N_q`
        :rtype: float
        """
        return _nq(self.friction_angle)

    @property
    @round_
    def ngamma(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_\gamma`.

        .. note::

            Exact values of :math:`N_\gamma` are not directly obtainable; values have
            been proposed by ``Brinch Hansen (1968)`` which are widely used in Europe,
            and also by ``Meyerhof (1963)``, which have been adopted in North America.

        The formulas shown below are ``Brinch Hansen`` and ``Meyerhof`` respectively.

        .. math::

            N_\gamma = 1.8 \left(N_q - 1 \right) \tan \phi

            N_\gamma = \left(N_q -1 \right)\tan(1.4\phi)

        :return: The bearing capacity factor :math:`N_\gamma`
        :rtype: float
        """
        return _ngamma(self.friction_angle, self.eng)

    @round_
    def ultimate_bearing_capacity(self) -> float:
        r"""Ultimate bearing capacity according to ``Terzaghi`` for ``strip footing``, ``square footing``
        and ``circular footing``.

        STRIP FOOTING
        -------------

        .. math::

            q_u = cN_c + \gamma D_f N_q + 0.5 \gamma B N_\gamma

        SQUARE FOOTING
        --------------

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.4 \gamma B N_\gamma

        CIRCULAR FOOTING
        ----------------

        .. math::

            q_u = 1.2cN_c + \gamma D_f N_q + 0.3 \gamma B N_{\gamma}

        :return: ultimate bearing capacity of the soil :math:`(q_{ult})`
        :rtype: float
        """

        return (
            mul(self.const, self.cohesion, self.nc)
            + mul(self.soil_unit_weight, self.foundation_size.depth, self.nq)
            + mul(
                CONSTANTS[self.footing_shape],
                self.soil_unit_weight,
                self.foundation_size.footing_size.width,
                self.ngamma,
            )
        )
