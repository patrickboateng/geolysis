from dataclasses import dataclass

from geolysis import GeotechEng
from geolysis.bearing_capacity import FootingShape, FootingSize, FoundationSize
from geolysis.utils import PI, arctan, cos, deg2rad, exp, round_, sin, tan


@dataclass
class TerzaghiBearingCapacityFactors:
    soil_friction_angle: float
    eng: GeotechEng = GeotechEng.MEYERHOF

    @property
    @round_(precision=2)
    def nc(self) -> float:
        r"""Return ``Terzaghi`` bearing capacity factor :math:`N_c`.

        .. math::

            N_c = \cot \phi \left(N_q - 1 \right)

        """
        x_1 = 1 / tan(self.soil_friction_angle)
        x_2 = self.nq - 1

        return x_1 * x_2

    @property
    @round_(precision=2)
    def nq(self) -> float:
        r"""Return ``Terzaghi`` bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \dfrac{e^{(\frac{3\pi}{2}-\phi)\tan\phi}}
                  {2\cos^2\left(45^{\circ}+\frac{\phi}{2}\right)}

        """
        x_1 = (3 * PI) / 2 - deg2rad(self.soil_friction_angle)
        x_2 = 2 * (cos(45 + (self.soil_friction_angle / 2)) ** 2)

        return exp(x_1 * tan(self.soil_friction_angle)) / x_2

    @property
    @round_(precision=2)
    def ngamma(self) -> float:
        r"""Return ``Terzaghi`` bearing capacity factor :math:`N_\gamma`.

        .. note::

            Exact values of :math:`N_\gamma` are not directly obtainable; values have
            been proposed by ``Brinch Hansen (1968)`` which are widely used in Europe,
            and also by ``Meyerhof (1963)``, which have been adopted in North America.

        The formulas shown below are ``Brinch Hansen`` and ``Meyerhof`` respectively.

        .. math::

            N_\gamma &= 1.8 \left(N_q - 1 \right) \tan \phi

            N_\gamma &= \left(N_q -1 \right)\tan(1.4\phi)

        """
        _ngamma: float

        if self.eng is GeotechEng.MEYERHOF:
            _ngamma = (self.nq - 1) * tan(1.4 * self.soil_friction_angle)

        elif self.eng is GeotechEng.HANSEN:
            _ngamma = 1.8 * (self.nq - 1) * tan(self.soil_friction_angle)

        else:
            msg = f"Available types are {GeotechEng.MEYERHOF} or {GeotechEng.HANSEN}"
            raise TypeError(msg)

        return _ngamma


class TerzaghiBearingCapacity:
    r"""Ultimate bearing capacity according to ``Terzaghi`` for ``strip``,
    ``square``, ``rectangular`` and ``circular footing``.

    :Example:


    :param cohesion: cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param friction_angle: internal angle of friction (degrees)
    :type soil_friction_angle: float
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
        *,
        cohesion: float,
        soil_friction_angle: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        eng: GeotechEng = GeotechEng.MEYERHOF,
        local_shear: bool = False,
    ) -> None:
        if local_shear:
            self.cohesion = (2 / 3) * cohesion
            self.soil_friction_angle = arctan(
                (2 / 3) * tan(soil_friction_angle)
            )
        else:
            self.cohesion = cohesion
            self.soil_friction_angle = soil_friction_angle

        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.footing_size = self.foundation_size.footing_size
        self.eng = eng

        self.bearing_capacity_factor = TerzaghiBearingCapacityFactors(
            self.soil_friction_angle, self.eng
        )

    @property
    def _x_1(self) -> float:
        return self.cohesion * self.nc

    @property
    def _x_2(self) -> float:
        return self.soil_unit_weight * self.foundation_size.depth * self.nq

    @property
    def _x_3(self) -> float:
        return self.soil_unit_weight * self.foundation_size.width * self.ngamma

    @round_
    def ultimate_4_strip_footing(self) -> float:
        r"""Return ultimate bearing capacity of strip footings.

        .. math::

            q_u = c \cdot N_c + \gamma
                  \cdot D_f \cdot N_q
                  + 0.5 \cdot \gamma \cdot B \cdot N_\gamma
        """
        return self._x_1 + self._x_2 + 0.5 * self._x_3

    @round_
    def ultimate_4_square_footing(self) -> float:
        r"""Return ultimate bearing capacity for square footings.

        .. math::

            q_u = 1.3 \cdot c \cdot N_c
                  + \gamma \cdot D_f \cdot N_q
                  + 0.4 \cdot \gamma \cdot B \cdot N_\gamma
        """
        return 1.3 * self._x_1 + self._x_2 + 0.4 * self._x_3

    @round_
    def ultimate_4_circular_footing(self) -> float:
        r"""Return ultimate bearing capacity for circular footing.

        .. math::

            q_u = 1.3 \cdot c \cdot N_c
                  + \gamma \cdot D_f \cdot N_q
                  + 0.3 \cdot \gamma \cdot B \cdot N_\gamma
        """
        return 1.3 * self._x_1 + self._x_2 + 0.3 * self._x_3

    @round_
    def ultimate_4_rectangular_footing(self) -> float:
        r"""Return the ultimate bearing for rectangular footing.

        .. math::

            q_u = \left( 1 + 0.3 \cdot \dfrac{B}{L} \right) c \cdot N_c
                  + \gamma \cdot D_f \cdot N_q
                  + \dfrac{1}{2} \left(1 - 0.2 \cdot \dfrac{B}{L} \right)
                  \cdot \gamma \cdot B \cdot N_\gamma
        """
        a = 1 + 0.3 * (self.footing_size.width / self.footing_size.length)
        b = 0.5 * (
            1 - 0.2 * self.footing_size.width / self.footing_size.length
        )

        return a * self._x_1 + self._x_2 + b * self._x_3

    @property
    def nc(self) -> float:
        return self.bearing_capacity_factor.nc

    @property
    def nq(self) -> float:
        return self.bearing_capacity_factor.nq

    @property
    def ngamma(self) -> float:
        return self.bearing_capacity_factor.ngamma


class MeyerhofBearingCapacityFactors:
    def __init__(self, soil_friction_angle: float):
        self.soil_friction_angle = soil_friction_angle

    @property
    def nc(self) -> float:
        """Return ``Meyerhof`` bearing capacity factor :math:`N_c`."""
        return (1 / tan(self.soil_friction_angle)) * (self.nq - 1)

    @property
    def nq(self) -> float:
        """Return ``Meyerhof`` bearing capacity factor :math:`N_q`."""
        x_1 = tan(45 + self.soil_friction_angle / 2) ** 2
        x_2 = exp(PI * tan(self.soil_friction_angle))

        return x_1 * x_2

    @property
    def ngamma(self) -> float:
        r"""Return ``Meyerhof`` bearing capacity factor :math:`N_\gamma`."""
        return 2 * (self.nq + 1) * tan(self.soil_friction_angle)


@dataclass
class MeyerhofDepthFactors:
    soil_friction_angle: float
    foundation_size: FoundationSize

    @property
    def d2w(self) -> float:
        return self.foundation_size.d2w

    @property
    def dc(self) -> float:
        """Return ``Meyerhof`` depth factor :math:`d_c`."""
        _dc: float

        if self.d2w <= 1:
            _dc = 1 + 0.4 * self.d2w

        else:
            x_1 = 0.4 * arctan(self.d2w)
            _dc = 1 + x_1 * (PI / 180)

        return _dc

    @property
    def dq(self) -> float:
        """Return ``Meyerhof`` depth factor :math:`d_q`."""
        _dq: float

        x_2 = (1 - sin(self.soil_friction_angle)) ** 2

        if self.d2w <= 1:
            x_1 = 2 * tan(self.soil_friction_angle)
            _dq = 1 + x_1 * x_2 * self.d2w

        else:
            x_1 = 2 * tan(self.soil_friction_angle)
            x_3 = arctan(self.d2w)
            _dq = 1 + x_1 * x_2 * x_3 * (PI / 180)

        return _dq

    @property
    def dgamma(self) -> float:
        r"""Return ``Meyerhof`` depth factor :math:`d_\gamma`."""
        return 1


@dataclass
class MeyerhofShapeFactors:
    soil_friction_angle: float
    footing_size: FootingSize
    nq: float
    nc: float

    @property
    def w2l(self) -> float:
        return self.footing_size.w2l

    @property
    def sc(self) -> float:
        """Return ``Meyerhof`` shape factor :math:`s_c`."""
        return 1 + self.w2l * (self.nq / self.nc)

    @property
    def sq(self) -> float:
        """Return ``Meyerhof`` shape factor :math:`s_q`."""
        return 1 + self.w2l * tan(self.soil_friction_angle)

    @property
    def sgamma(self) -> float:
        r"""Return ``Meyerhof`` shape factor :math:`s_\gamma`."""
        return 1 - 0.4 * self.w2l


@dataclass
class MeyerhofInclinationFactors:
    soil_friction_angle: float
    beta: float

    @property
    def ic(self) -> float:
        """Return ``Meyerhof`` inclination factor :math:`i_c`."""
        return (1 - self.beta / 90) ** 2

    @property
    def iq(self) -> float:
        """Return ``Meyerhof`` inclination factor :math:`i_q`."""
        return self.ic

    @property
    def igamma(self) -> float:
        r"""Return ``Meyerhof`` inclination factor :math:`i_\gamma`."""
        return (1 - self.beta / self.soil_friction_angle) ** 2


class MeyerhofBearingCapacity:
    def __init__(
        self,
        cohesion: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        soil_friction_angle: float,
        beta: float,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta

        self.bearing_capacity_factor = MeyerhofBearingCapacityFactors(
            self.soil_friction_angle
        )
        self.depth_factor = MeyerhofDepthFactors(
            self.soil_friction_angle, self.foundation_size
        )
        self.shape_factor = MeyerhofShapeFactors(
            self.soil_friction_angle,
            self.foundation_size.footing_size,
            self.nq,
            self.nc,
        )
        self.incl_factor = MeyerhofInclinationFactors(
            self.soil_friction_angle, self.beta
        )

    def ultimate(self) -> float:
        r"""Return the ultimate bearing capacity according to ``Meyerhof``."""
        x_1 = self.cohesion * self.nc * self.sc * self.dc * self.ic
        x_2 = self.soil_unit_weight * self.foundation_size.depth
        x_3 = self.nq * self.sq * self.dq * self.iq
        x_4 = self.soil_unit_weight * self.foundation_size.width
        x_5 = self.ngamma * self.sgamma * self.dgamma * self.igamma

        return x_1 + (x_2 * x_3) + (0.5 * x_4 * x_5)

    @property
    def nc(self) -> float:
        return self.bearing_capacity_factor.nc

    @property
    def nq(self) -> float:
        return self.bearing_capacity_factor.nq

    @property
    def ngamma(self) -> float:
        return self.bearing_capacity_factor.ngamma

    @property
    def dc(self) -> float:
        return self.depth_factor.dc

    @property
    def dq(self) -> float:
        return self.depth_factor.dq

    @property
    def dgamma(self) -> float:
        return self.depth_factor.dgamma

    @property
    def sc(self) -> float:
        return self.shape_factor.sc

    @property
    def sq(self) -> float:
        return self.shape_factor.sq

    @property
    def sgamma(self) -> float:
        return self.shape_factor.sgamma

    @property
    def ic(self) -> float:
        return self.incl_factor.ic

    @property
    def iq(self) -> float:
        return self.incl_factor.iq

    @property
    def igamma(self) -> float:
        return self.incl_factor.igamma


@dataclass
class HansenBearingCapacityFactors:
    soil_friction_angle: float

    @property
    def nc(self) -> float:
        r"""Return ``Hansen`` bearing capacity factor :math:`N_c`.

        .. math::

            N_c = (N_q - 1) \cot \phi

        """
        x_1 = 1 / tan(self.soil_friction_angle)
        x_2 = self.nq - 1.0

        return x_1 * x_2

    @property
    def nq(self) -> float:
        r"""Return ``Hansen`` bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \tan^2 \left(45 + \frac{\phi}{2} \right)
                  \left(e^{\pi \tan \phi}\right)

        """
        x_1 = tan(45 + self.soil_friction_angle / 2) ** 2
        x_2 = exp(PI * tan(self.soil_friction_angle))

        return x_1 * x_2

    @property
    def ngamma(self) -> float:
        r"""Return ``Hansen`` bearing capacity factor :math:`N_q`.

        .. math::

            N_\gamma = 1.8(N_q - 1) \tan \phi
        """
        return 1.8 * (self.nq - 1.0) * tan(self.soil_friction_angle)


@dataclass
class HansenDepthFactors:
    foundation_size: FoundationSize

    @property
    def d2w(self) -> float:
        return self.foundation_size.d2w

    @property
    def dc(self) -> float:
        r"""Return ``Hansen`` depth factor :math:`d_c`.

        .. math::

            d_c = 1 + 0.35 \left(\frac{D_f}{B}\right)

        """
        return 1 + 0.35 * self.d2w

    @property
    def dq(self) -> float:
        r"""Return ``Hansen`` depth factor :math:`d_q`.

        .. math::

            d_q = 1 + 0.35 \left(\frac{D_f}{B}\right)

        """
        return self.dc

    @property
    def dgamma(self) -> float:
        r"""Return ``Hansen`` depth factor :math:`d_\gamma`.

        .. math::

            d_\gamma = 1.0

        """
        return 1.0


@dataclass
class HansenShapeFactors:
    footing_size: FootingSize
    footing_shape: FootingShape

    @property
    def w2l(self) -> float:
        return self.footing_size.w2l

    @property
    def sc(self) -> float:
        r"""Return ``Hansen`` shape factor :math:`s_c`.

        - for strip footing |rarr| :math:`s_c = 1`
        - for rectangular footing |rarr| :math:`s_c = 1 + 0.2 \left(\dfrac{B}{L}\right)`
        - for square footing |rarr| :math:`s_c = 1.3`
        - for circular footing |rarr| :math:`s_c = 1.3`

        """
        _sc: float

        if self.footing_shape is FootingShape.STRIP:
            _sc = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sc = 1.3

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sc = 1 + 0.2 * self.w2l

        else:
            msg = ""
            raise TypeError(msg)

        return _sc

    @property
    def sq(self) -> float:
        r"""Return ``Hansen`` shape factor :math:`s_q`.

        - for strip footing |rarr| :math:`s_q = 1`
        - for rectangular footing |rarr| :math:`s_q = 1 + 0.2 \left(\dfrac{B}{L}\right)`
        - for square footing |rarr| :math:`s_q = 1.2`
        - for circular footing |rarr| :math:`s_q = 1.2`

        """
        _sq: float

        if self.footing_shape is FootingShape.STRIP:
            _sq = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sq = 1.2

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sq = 1 + 0.2 * self.w2l

        else:
            msg = ""
            raise TypeError(msg)

        return _sq

    @property
    def sgamma(self) -> float:
        r"""Return ``Hansen`` shape factor :math:`s_\gamma`.

        - for strip footing |rarr| :math:`s_\gamma = 1`
        - for rectangular footing |rarr| :math:`s_\gamma = 1 - 0.4 \left(\dfrac{B}{L}\right)`
        - for square footing |rarr| :math:`s_\gamma = 0.8`
        - for circular footing |rarr| :math:`s_\gamma = 0.6`

        """
        _sgamma: float

        if self.footing_shape is FootingShape.STRIP:
            _sgamma = 1.0

        elif self.footing_shape is FootingShape.SQUARE:
            _sgamma = 0.8

        elif self.footing_shape is FootingShape.CIRCULAR:
            _sgamma = 0.6

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sgamma = 1 - 0.4 * self.w2l

        else:
            msg = ""
            raise TypeError(msg)

        return _sgamma


@dataclass
class HansenInclinationFactors:
    cohesion: float
    footing_size: FootingSize
    beta: float
    total_vertical_load: float

    @property
    def ic(self) -> float:
        r"""Return ``Hansen`` inclination factor :math:`i_c`.

        .. math::

            i_c = 1 - \left(\dfrac{\beta}{2cBL}\right)

        """
        x_1 = (
            2
            * self.cohesion
            * self.footing_size.width
            * self.footing_size.length
        )
        return 1 - self.beta / x_1

    @property
    def iq(self) -> float:
        r"""Return ``Hansen`` inclination factor :math:`i_q`.

        .. math::

            i_q = 1 - 1.5 \cdot \dfrac{\beta}{V}

        """
        return 1 - (1.5 * self.beta) / self.total_vertical_load

    @property
    def igamma(self) -> float:
        r"""Return ``Hansen`` inclination factor :math:`i_\gamma`.

        .. math::

            i_\gamma = \left(1 - 1.5 \cdot \dfrac{\beta}{V} \right)^2

        """

        return self.iq**2


class HansenBearingCapacity:
    r"""Ultimate bearing capacity according to ``Hansen``.

    :param cohesion: Cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param soil_unit_weight: Unit weight of soil :math:`(kN/m^3)`
    :type soil_unit_weight: float
    :param foundation_size: Size of foundation
    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    :param beta: Inclination of the load on the foundation with respect to the
        vertical (degrees)
    :type beta: float
    :param total_vertical_load: Total vertical load on foundation
    :type total_vertical_load: float
    :param footing_shape: Shape of the footing
    :type footing_shape: float
    """

    def __init__(
        self,
        cohesion: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        soil_friction_angle: float,
        beta: float,
        total_vertical_load: float,
        footing_shape: FootingShape = FootingShape.SQUARE,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta
        self.footing_shape = footing_shape
        self.total_vertical_load = total_vertical_load

        self.bearing_capacity_factor = HansenBearingCapacityFactors(
            self.soil_friction_angle
        )
        self.depth_factor = HansenDepthFactors(self.foundation_size)
        self.shape_factor = HansenShapeFactors(
            self.foundation_size.footing_size, self.footing_shape
        )
        self.incl_factor = HansenInclinationFactors(
            self.cohesion,
            self.foundation_size.footing_size,
            self.beta,
            self.total_vertical_load,
        )

    def ultimate(self) -> float:
        r"""Return the ultimate bearing capacity according to ``Hansen``.

        .. math::

            q_u = c \cdot N_c \cdot s_c \cdot d_c \cdot i_c \,
                  + q \cdot N_q \cdot s_q \cdot d_q \cdot i_q \,
                  + 0.5 \cdot \gamma \cdot B \cdot N_\gamma
                  \cdot s_\gamma \cdot d_\gamma \cdot i_\gamma

        """
        x_1 = self.cohesion * self.nc * self.sc * self.dc * self.ic
        x_2 = self.soil_unit_weight * self.foundation_size.depth
        x_3 = self.nq * self.sq * self.dq * self.iq
        x_4 = self.soil_unit_weight * self.foundation_size.width
        x_5 = self.ngamma * self.sgamma * self.dgamma * self.igamma

        return x_1 + (x_2 * x_3) + (0.5 * x_4 * x_5)

    @property
    def nc(self) -> float:
        return self.bearing_capacity_factor.nc

    @property
    def nq(self) -> float:
        return self.bearing_capacity_factor.nq

    @property
    def ngamma(self) -> float:
        return self.bearing_capacity_factor.ngamma

    @property
    def dc(self) -> float:
        return self.depth_factor.dc

    @property
    def dq(self) -> float:
        return self.depth_factor.dq

    @property
    def dgamma(self) -> float:
        return self.depth_factor.dgamma

    @property
    def sc(self) -> float:
        return self.shape_factor.sc

    @property
    def sq(self) -> float:
        return self.shape_factor.sq

    @property
    def sgamma(self) -> float:
        return self.shape_factor.sgamma

    @property
    def ic(self) -> float:
        return self.incl_factor.ic

    @property
    def iq(self) -> float:
        return self.incl_factor.iq

    @property
    def igamma(self) -> float:
        return self.incl_factor.igamma


@dataclass
class VesicBearingCapacityFactors:
    soil_friction_angle: float

    @property
    def nc(self) -> float:
        r"""Return ``Vesic`` bearing capacity factor :math:`N_c`.

        .. math::

            N_c = (N_q - 1) \cdot \cot \phi

        """
        return (1 / tan(self.soil_friction_angle)) * (self.nq - 1)

    @property
    def nq(self) -> float:
        r"""Return ``Vesic`` bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \tan^2 \left(45 + \frac{\phi}{2} \right)
                  \cdot (e^{\pi \tan \phi})

        """
        x_1 = tan(45 + self.soil_friction_angle / 2)
        x_2 = exp(PI * tan(self.soil_friction_angle))

        return (x_1**2) * x_2

    @property
    def ngamma(self) -> float:
        r"""Return ``Vesic`` bearing capacity factor :math:`N_\gamma`.

        .. math::

            N_\gamma &= 2 \cdot (N_q + 1) \cdot \tan \phi`

        """
        return 2 * (self.nq + 1) * tan(self.soil_friction_angle)


@dataclass
class VesicDepthFactors:
    soil_friction_angle: float
    foundation_size: FoundationSize

    @property
    def d2w(self) -> float:
        return self.foundation_size.d2w

    @property
    def dc(self) -> float:
        r"""Return ``Vesic`` depth factor :math:`d_c`.

        .. math::

            d_c = 1 + 0.4 \cdot \left(\frac{D_f}{B} \right)

        """
        return 1 + 0.4 * self.d2w

    @property
    def dq(self) -> float:
        r"""Return ``Vesic`` depth factor :math:`d_q`.

        .. math::

            d_q = 1 + 2 \cdot \tan \phi
                  \cdot (1 - \sin \phi)^2
                  \cdot \dfrac{D_f}{B}

        """
        x_1 = 2 * tan(self.soil_friction_angle)
        x_2 = (1 - sin(self.soil_friction_angle)) ** 2
        x_3 = self.d2w

        return 1 + (x_1 * x_2 * x_3)

    @property
    def dgamma(self) -> float:
        r"""Return ``Vesic`` depth factor :math:`d_\gamma`.

        .. math::

            d_\gamma = 1.0`

        """
        return 1.0


@dataclass
class VesicShapeFactors:
    soil_friction_angle: float
    footing_size: FootingSize
    footing_shape: FootingShape
    nq: float
    nc: float

    @property
    def w2l(self) -> float:
        return self.footing_size.w2l

    @property
    def sc(self) -> float:
        r"""Return ``Vesic`` shape factor :math:`s_c`.

        - for strip footing |rarr| :math:`s_c = 1`
        - for rectangular footing |rarr| math:`s_c = 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c}`
        - for square or circular footing |rarr| :math:`s_c = 1 + \dfrac{N_q}{N_c}`
        """
        _sc: float

        if self.footing_shape is FootingShape.STRIP:
            _sc = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sc = 1 + (self.nq / self.nc)

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sc = 1 + self.w2l * (self.nq / self.nc)

        else:
            msg = ""
            raise TypeError(msg)

        return _sc

    @property
    def sq(self) -> float:
        r"""Return ``Vesic`` shape factor :math:`s_q`.

        - for strip footing |rarr| :math:`s_q = 1`
        - for rectangular footing |rarr| math:`s_q = 1 + \dfrac{B}{L} \cdot \tan \phi`
        - for square or circular footing |rarr| :math:`s_q = 1 + \tan \phi`
        """
        _sq: float

        if self.footing_shape is FootingShape.STRIP:
            _sq = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sq = 1 + tan(self.soil_friction_angle)

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sq = 1 + self.w2l * tan(self.soil_friction_angle)

        else:
            msg = ""
            raise TypeError(msg)

        return _sq

    @property
    def sgamma(self) -> float:
        r"""Return ``Vesic`` shape factor :math:`s_\gamma`.

        - for strip footing |rarr| :math:`s_\gamma = 1`
        - for rectangular footing |rarr| math:`s_\gamma = 1 - 0.4 \cdot \dfrac{B}{L}`
        - for square or circular footing |rarr| :math:`s_\gamma = 0.6`
        """
        _sgamma: float

        if self.footing_shape is FootingShape.STRIP:
            _sgamma = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sgamma = 0.6

        elif self.footing_shape is FootingShape.RECTANGULAR:
            _sgamma = 1 - 0.4 * (self.w2l)

        else:
            msg = ""
            raise TypeError(msg)

        return _sgamma


@dataclass
class VesicInclinationFactors:
    soil_friction_angle: float
    beta: float

    @property
    def ic(self) -> float:
        r"""Return ``Vesic`` inclination factor :math:`i_c`.

        .. math::

            i_c = \left(1 - \frac{\beta}{90} \right)^2

        """
        return (1 - self.beta / 90) ** 2

    @property
    def iq(self) -> float:
        r"""Return ``Vesic`` inclination factor :math:`i_q`.

        .. math::

            i_q = \left(1 - \frac{\beta}{90} \right)^2

        """
        return self.ic

    @property
    def igamma(self) -> float:
        r"""Return ``Vesic`` inclination factor :math:`i_\gamma`.

        .. math::

            i_\gamma = \left(1 - \dfrac{\beta}{\phi} \right)^2

        """
        return (1 - self.beta / self.soil_friction_angle) ** 2


class VesicBearingCapacity:
    r"""Ultimate bearing capacity according to ``Vesic``.

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
        soil_friction_angle: float,
        beta: float,
        footing_shape: FootingShape = FootingShape.SQUARE,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta
        self.footing_shape = footing_shape

        self.bearing_cpty_factors = VesicBearingCapacityFactors(
            self.soil_friction_angle
        )
        self.depth_factors = VesicDepthFactors(
            self.soil_friction_angle, self.foundation_size
        )
        self.shape_factors = VesicShapeFactors(
            self.soil_friction_angle,
            self.foundation_size.footing_size,
            self.footing_shape,
            self.nq,
            self.nc,
        )
        self.incl_factors = VesicInclinationFactors(
            self.soil_friction_angle, self.beta
        )

    def ultimate(self) -> float:
        r"""Return the ultimate bearing capacity according to ``Hansen``.

        .. math::

            q_u = c \cdot N_c \cdot s_c \cdot d_c \cdot i_c \,
            + q \cdot N_q \cdot s_q \cdot d_q \cdot i_q \,
            + 0.5 \cdot \gamma \cdot B \cdot N_\gamma \cdot s_\gamma \cdot d_\gamma \cdot i_\gamma

        """
        x_1 = self.cohesion * self.nc * self.sc * self.dc * self.ic
        x_2 = self.soil_unit_weight * self.foundation_size.depth
        x_3 = self.nq * self.sq * self.dq * self.iq
        x_4 = self.soil_unit_weight * self.foundation_size.width
        x_5 = self.ngamma * self.sgamma * self.dgamma * self.igamma

        return x_1 + (x_2 * x_3) + (0.5 * x_4 * x_5)

    @property
    def nc(self) -> float:
        return self.bearing_cpty_factors.nc

    @property
    def nq(self) -> float:
        return self.bearing_cpty_factors.nq

    @property
    def ngamma(self) -> float:
        return self.bearing_cpty_factors.ngamma

    @property
    def dc(self) -> float:
        return self.depth_factors.dc

    @property
    def dq(self) -> float:
        return self.depth_factors.dq

    @property
    def dgamma(self) -> float:
        return self.depth_factors.dgamma

    @property
    def sc(self) -> float:
        return self.shape_factors.sc

    @property
    def sq(self) -> float:
        return self.shape_factors.sq

    @property
    def sgamma(self) -> float:
        return self.shape_factors.sgamma

    @property
    def ic(self) -> float:
        return self.incl_factors.ic

    @property
    def iq(self) -> float:
        return self.incl_factors.iq

    @property
    def igamma(self) -> float:
        return self.incl_factors.igamma
