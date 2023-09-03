import statistics
from typing import Iterable

from geolab import GeotechEng
from geolab.bearing_capacity import FootingShape, FoundationSize
from geolab.bearing_capacity.spt import spt_corrections
from geolab.utils import PI, cos, deg2rad, exp, sin, tan


class terzaghi_bearing_capacity:
    r"""Ultimate bearing capacity according to ``Terzaghi`` for ``strip footing``,
    ``square footing`` and ``circular footing``.



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

    FOOTING_SHAPES_CONSTS = {
        FootingShape.STRIP: 0.5,
        FootingShape.SQUARE: 0.4,
        FootingShape.CIRCULAR: 0.3,
    }

    def __init__(
        self,
        cohesion: float,
        friction_angle: float,
        soil_unit_weight: float,
        foundation_size: FoundationSize,
        footing_shape: FootingShape = FootingShape.SQUARE,
        eng: GeotechEng = GeotechEng.MEYERHOF,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.friction_angle = friction_angle
        self.footing_shape = footing_shape
        self.eng = eng

        self.const = 1 if footing_shape is FootingShape.STRIP else 1.2

    def __call__(self) -> float:
        return self.ultimate_bearing_capacity()

    def ultimate_bearing_capacity(self) -> float:
        """Returns the ultimate bearing capacity according to ``Terzaghi``."""
        x1 = self.const * self.cohesion * self.nc
        x2 = self.soil_unit_weight * self.foundation_size.depth * self.nq
        x3 = self.soil_unit_weight * self.foundation_size.width * self.ngamma

        return x1 + x2 + self.FOOTING_SHAPES_CONSTS[self.footing_shape] * x3

    @property
    def nc(self) -> float:
        """Returns Terzaghi Bearing Capacity factor :math:`N_c`."""
        x1 = (3 * PI) / 2 - deg2rad(self.friction_angle)
        x2 = 2 * (cos(45 + (self.friction_angle / 2)) ** 2)

        return exp(x1 * tan(self.friction_angle)) / x2

    @property
    def nq(self) -> float:
        """Returns Terzaghi Bearing Capacity factor :math:`N_q`."""
        x1 = 1 / tan(self.friction_angle)
        x2 = self.nq - 1

        return x1 * x2

    @property
    def ngamma(self) -> float:
        r"""Terzaghi Bearing Capacity factor :math:`N_\gamma`."""
        _ngamma: float

        if self.eng is GeotechEng.MEYERHOF:
            _ngamma = (self.nq - 1) * tan(1.4 * self.friction_angle)

        elif self.eng is GeotechEng.HANSEN:
            _ngamma = 1.8 * (self.nq - 1) * tan(self.friction_angle)

        else:
            msg = f"Available types are {GeotechEng.MEYERHOF} or {GeotechEng.HANSEN}"
            raise TypeError(msg)

        return _ngamma


class meyerhof_bearing_capacity:
    def nc(self):
        ...

    def nq(self):
        ...

    def ngamma(self):
        ...


class hansen_bearing_capacity:
    r"""Ultimate bearing capacity according to ``Hansen``.

    :param cohesion: Cohesion of foundation soil :math:`(kN/m^2)`
    :type cohesion: float
    :param soil_unit_weight: Unit weight of soil :math:`(kN/m^3)`
    :type soil_unit_weight: float
    :param foundation_size: Size of foundation
    :param friction_angle: Internal angle of friction (degrees)
    :type friction_angle: float
    :param beta: Inclination of the load on the foundation with respect to the vertical (degrees)
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
        friction_angle: float,
        beta: float,
        total_vertical_load: float,
        footing_shape: FootingShape = FootingShape.SQUARE,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.friction_angle = friction_angle
        self.beta = beta
        self.footing_shape = footing_shape
        self.total_vertical_load = total_vertical_load

    def __call__(self) -> float:
        return self.ultimate_bearing_capacity()

    def ultimate_bearing_capacity(self) -> float:
        r"""Returns the ultimate bearing capacity according to ``Hansen``."""
        x1 = self.cohesion * self.nc * self.sc * self.dc * self.ic
        x2 = self.soil_unit_weight * self.foundation_size.depth
        x3 = self.nq * self.sq * self.dq * self.iq
        x4 = self.soil_unit_weight * self.foundation_size.width
        x5 = self.ngamma * self.sgamma * self.dgamma * self.igamma

        return x1 + (x2 * x3) + (0.5 * x4 * x5)

    @property
    def nc(self) -> float:
        """"""
        x1 = 1 / tan(self.friction_angle)
        x2 = self.nq - 1.0

        return x1 * x2

    @property
    def nq(self) -> float:
        """"""
        x1 = tan(45 + self.friction_angle / 2) ** 2
        x2 = exp(PI * tan(self.friction_angle))

        return x1 * x2

    @property
    def ngamma(self) -> float:
        """"""
        return 1.8 * (self.nq - 1.0) * tan(self.friction_angle)

    @property
    def dc(self) -> float:
        """"""
        x1 = (
            self.foundation_size.depth
            / self.foundation_size.footing_size.width
        )

        return 1 + 0.35 * x1

    @property
    def dq(self) -> float:
        """"""
        return self.dc

    @property
    def dgamma(self) -> float:
        """"""
        return 1.0

    @property
    def sc(self) -> float:
        """"""
        _sc: float

        if self.footing_shape is FootingShape.STRIP:
            _sc = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sc = 1.3

        elif self.footing_shape is FootingShape.RECTANGULAR:
            x1 = self.foundation_size.width / self.foundation_size.length

            _sc = 1 + 0.2 * x1

        else:
            msg = ""
            raise TypeError(msg)

        return _sc

    @property
    def sq(self) -> float:
        """"""
        _sq: float

        if self.footing_shape is FootingShape.STRIP:
            _sq = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sq = 1.2

        elif self.footing_shape is FootingShape.RECTANGULAR:
            x1 = self.foundation_size.width / self.foundation_size.length

            _sq = 1 + 0.2 * x1

        else:
            msg = ""
            raise TypeError(msg)

        return _sq

    @property
    def sgamma(self) -> float:
        """"""
        _sgamma: float

        if self.footing_shape is FootingShape.STRIP:
            _sgamma = 1.0

        elif self.footing_shape is FootingShape.SQUARE:
            _sgamma = 0.8

        elif self.footing_shape is FootingShape.CIRCULAR:
            _sgamma = 0.6

        elif self.footing_shape is FootingShape.RECTANGULAR:
            x1 = self.foundation_size.width / self.foundation_size.length
            _sgamma = 1 - 0.4 * x1

        else:
            msg = ""
            raise TypeError(msg)

        return _sgamma

    @property
    def ic(self) -> float:
        """"""
        x1 = (
            2
            * self.cohesion
            * self.foundation_size.width
            * self.foundation_size.length
        )
        return 1 - self.beta / x1

    @property
    def iq(self) -> float:
        """"""
        return 1 - (1.5 * self.beta) / self.total_vertical_load

    @property
    def igamma(self) -> float:
        """"""
        return self.iq**2


class vesic_bearing_capacity:
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
        friction_angle: float,
        beta: float,
        footing_shape: FootingShape = FootingShape.SQUARE,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.foundation_size = foundation_size
        self.friction_angle = friction_angle
        self.beta = beta
        self.footing_shape = footing_shape

    def __call__(self) -> float:
        return self.ultimate_bearing_capacity()

    def ultimate_bearing_capacity(self) -> float:
        r"""Returns the ultimate bearing capacity according to ``Hansen``."""
        x1 = self.cohesion * self.nc * self.sc * self.dc * self.ic
        x2 = self.soil_unit_weight * self.foundation_size.depth
        x3 = self.nq * self.sq * self.dq * self.iq
        x4 = self.soil_unit_weight * self.foundation_size.width
        x5 = self.ngamma * self.sgamma * self.dgamma() * self.igamma

        return x1 + (x2 * x3) + (0.5 * x4 * x5)

    @property
    def nc(self) -> float:
        """"""
        return (1 / tan(self.friction_angle)) * (self.nq - 1)

    @property
    def nq(self) -> float:
        """"""
        x1 = tan(45 + self.friction_angle / 2)
        x2 = exp(PI * tan(self.friction_angle))

        return (x1**2) * (x2)

    @property
    def ngamma(self) -> float:
        """"""
        return 2 * (self.nq + 1) * tan(self.friction_angle)

    @property
    def dc(self) -> float:
        x1 = self.foundation_size.depth / self.foundation_size.width

        return 1 + 0.4 * x1

    @property
    def dq(self) -> float:
        x1 = 2 * tan(self.friction_angle)
        x2 = (1 - sin(self.friction_angle)) ** 2
        x3 = self.foundation_size.depth / self.foundation_size.width

        return 1 + (x1 * x2 * x3)

    @staticmethod
    def dgamma() -> float:
        return 1.0

    @property
    def sc(self) -> float:
        _sc: float

        if self.footing_shape is FootingShape.STRIP:
            _sc = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sc = 1 + (self.nq / self.nc)

        elif self.footing_shape is FootingShape.RECTANGULAR:
            x1 = self.foundation_size.width / self.foundation_size.length

            _sc = 1 + x1 * (self.nq / self.nc)

        else:
            msg = ""
            raise TypeError(msg)

        return _sc

    @property
    def sq(self) -> float:
        _sq: float

        if self.footing_shape is FootingShape.STRIP:
            _sq = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sq = 1 + tan(self.friction_angle)

        elif self.footing_shape is FootingShape.RECTANGULAR:
            x1 = self.foundation_size.width / self.foundation_size.length
            _sq = 1 + x1 * tan(self.friction_angle)

        else:
            msg = ""
            raise TypeError(msg)

        return _sq

    @property
    def sgamma(self) -> float:
        _sgamma: float

        if self.footing_shape is FootingShape.STRIP:
            _sgamma = 1.0

        elif (
            self.footing_shape is FootingShape.SQUARE
            or self.footing_shape is FootingShape.CIRCULAR
        ):
            _sgamma = 0.6

        elif self.footing_shape is FootingShape.RECTANGULAR:
            x1 = self.foundation_size.width / self.foundation_size.length
            _sgamma = 1 - 0.4 * (x1)

        else:
            msg = ""
            raise TypeError(msg)

        return _sgamma

    @property
    def ic(self) -> float:
        return (1 - self.beta / 90) ** 2

    @property
    def iq(self) -> float:
        return self.ic

    @property
    def igamma(self) -> float:
        return (1 - self.beta / self.friction_angle) ** 2
