from dataclasses import dataclass

from geolysis.bearing_capacity import FootingSize, FoundationSize
from geolysis.utils import PI, arctan, cos, deg2rad, exp, round_, sin, tan


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
