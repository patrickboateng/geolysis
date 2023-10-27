from geolysis.bearing_capacity import FoundationSize
from geolysis.utils import PI, arctan, exp, sin, tan


class MeyerhofFactors:
    def __init__(
        self,
        soil_friction_angle: float,
        beta: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta
        self.foundation_size = foundation_size

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

    @property
    def _d2w(self) -> float:
        """Return depth to width ratio of foundation."""
        return self.foundation_size.d2w

    @property
    def dc(self) -> float:
        """Return ``Meyerhof`` depth factor :math:`d_c`."""

        if self._d2w <= 1:
            return 1 + 0.4 * self._d2w

        x_1 = 0.4 * arctan(self._d2w)
        return 1 + x_1 * (PI / 180)

    @property
    def dq(self) -> float:
        """Return ``Meyerhof`` depth factor :math:`d_q`."""
        x_2 = (1 - sin(self.soil_friction_angle)) ** 2

        if self._d2w <= 1:
            x_1 = 2 * tan(self.soil_friction_angle)
            return 1 + x_1 * x_2 * self._d2w

        x_1 = 2 * tan(self.soil_friction_angle)
        x_3 = arctan(self._d2w)
        return 1 + x_1 * x_2 * x_3 * (PI / 180)

    @property
    def dgamma(self) -> float:
        r"""Return ``Meyerhof`` depth factor :math:`d_\gamma`."""
        return 1

    @property
    def _w2l(self) -> float:
        return self.foundation_size.footing_size.w2l

    @property
    def sc(self) -> float:
        """Return ``Meyerhof`` shape factor :math:`s_c`."""
        return 1 + self._w2l * (self.nq / self.nc)

    @property
    def sq(self) -> float:
        """Return ``Meyerhof`` shape factor :math:`s_q`."""
        return 1 + self._w2l * tan(self.soil_friction_angle)

    @property
    def sgamma(self) -> float:
        r"""Return ``Meyerhof`` shape factor :math:`s_\gamma`."""
        return 1 - 0.4 * self._w2l

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
        soil_friction_angle: float,
        beta: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.soil_friction_angle = soil_friction_angle
        self.beta = beta
        self.foundation_size = foundation_size

        self.meyerhof_factors = MeyerhofFactors(
            soil_friction_angle, beta, foundation_size
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
        return self.meyerhof_factors.nc

    @property
    def nq(self) -> float:
        return self.meyerhof_factors.nq

    @property
    def ngamma(self) -> float:
        return self.meyerhof_factors.ngamma

    @property
    def dc(self) -> float:
        return self.meyerhof_factors.dc

    @property
    def dq(self) -> float:
        return self.meyerhof_factors.dq

    @property
    def dgamma(self) -> float:
        return self.meyerhof_factors.dgamma

    @property
    def sc(self) -> float:
        return self.meyerhof_factors.sc

    @property
    def sq(self) -> float:
        return self.meyerhof_factors.sq

    @property
    def sgamma(self) -> float:
        return self.meyerhof_factors.sgamma

    @property
    def ic(self) -> float:
        return self.meyerhof_factors.ic

    @property
    def iq(self) -> float:
        return self.meyerhof_factors.iq

    @property
    def igamma(self) -> float:
        return self.meyerhof_factors.igamma
