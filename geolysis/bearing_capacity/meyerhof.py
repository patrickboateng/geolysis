from typing import ClassVar

from geolysis import ERROR_TOLERANCE
from geolysis.bearing_capacity import FoundationSize
from geolysis.exceptions import AllowableSettlementError
from geolysis.utils import PI, arctan, cot, exp, prod, round_, sin, tan


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
        return cot(self.soil_friction_angle) * (self.nq - 1)

    @property
    def nq(self) -> float:
        """Return ``Meyerhof`` bearing capacity factor :math:`N_q`."""
        expr_1 = tan(45 + self.soil_friction_angle / 2) ** 2
        expr_2 = exp(PI * tan(self.soil_friction_angle))
        return prod(expr_1, expr_2)

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

        return 1 + 0.4 * arctan(self._d2w) * (PI / 180)

    @property
    def dq(self) -> float:
        """Return ``Meyerhof`` depth factor :math:`d_q`."""

        if self._d2w <= 1:
            expr_1 = 2 * tan(self.soil_friction_angle)
            expr_2 = (1 - sin(self.soil_friction_angle)) ** 2

            return 1 + prod(expr_1, expr_2, self._d2w)

        first_expr = 1 + (2 * tan(self.soil_friction_angle))
        mid_expr = (1 - sin(self.soil_friction_angle)) ** 2
        last_expr = arctan(self._d2w) * (PI / 180)

        return prod(first_expr, mid_expr, last_expr)

    @property
    def dgamma(self) -> float:
        r"""Return ``Meyerhof`` depth factor :math:`d_\gamma`."""
        return 1

    @property
    def _w2l(self) -> float:
        return self.foundation_size.w2l

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
    ALLOWABLE_SETTLEMENT: ClassVar[float] = 25.4

    def __init__(
        self,
        cohesion: float,
        soil_unit_weight: float,
        soil_friction_angle: float,
        actual_settlement: float,
        beta: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.cohesion = cohesion
        self.soil_unit_weight = soil_unit_weight
        self.soil_friction_angle = soil_friction_angle
        self.actual_settlement = actual_settlement
        self.beta = beta
        self.foundation_size = foundation_size

        self._meyerhof_factors = MeyerhofFactors(
            soil_friction_angle=self.soil_friction_angle,
            beta=self.beta,
            foundation_size=self.foundation_size,
        )

    @property
    def fd(self) -> float:
        r"""Return the depth factor (:math:`f_d`).

        .. math::

            f_d = 1 + 0.33 \cdot \frac{D_f}{B}

        """
        return min(1 + 0.33 * self.foundation_size.d2w, 1.33)

    @round_(precision=2)
    def net_allowable_bearing_capacity(self, n_design: float) -> float:
        r"""Return the net allowable bearing capacity.

        .. math::

            q_{a(net)} &= 19.16 \cdot N_{des} \cdot f_d \cdot \dfrac{S_e}{25.4} \, , \, B \le 1.22

            q_{a(net)} &= 11.98 \cdot N_{des} \cdot \left(\dfrac{3.28B + 1}{3.28B} \right)^2
                          \cdot f_d \cdot \dfrac{S_e}{25.4} \, , \, B \gt 1.22


        :raises AllowableSettlementError: If actual settlement is greater than
                                          allowable settement
        """

        settlement_ratio = self.actual_settlement / self.ALLOWABLE_SETTLEMENT
        if settlement_ratio > (1 + ERROR_TOLERANCE):
            msg = f"Settlement: {self.actual_settlement}should be less than or equal \
                  Allowable Settlement: {self.ALLOWABLE_SETTLEMENT}"
            raise AllowableSettlementError(msg)

        if self.foundation_size.width <= 1.22:
            return 19.16 * n_design * self.fd * settlement_ratio

        a = 3.28 * self.foundation_size.width + 1
        b = 3.28 * self.foundation_size.width

        return n_design * self.fd * settlement_ratio * (11.98 * (a / b)) ** 2

    @round_(precision=2)
    def allowable_bearing_capacity_1956(self, spt_n60: float) -> float:
        if self.foundation_size.width <= 1.2:
            return 12 * spt_n60 * self.fd

        expr = (self.foundation_size.width + 0.3) / self.foundation_size.width
        return 8 * spt_n60 * expr**2 * self.fd

    @property
    def _first_expr(self) -> float:
        return self.cohesion * self.nc * self.sc * self.dc * self.ic

    @property
    def _mid_expr(self) -> float:
        return prod(
            self.soil_unit_weight,
            self.foundation_size.depth,
            self.nq,
            self.sq,
            self.dq,
            self.iq,
        )

    @property
    def _last_expr(self) -> float:
        return prod(
            self.soil_unit_weight,
            self.foundation_size.width,
            self.ngamma,
            self.sgamma,
            self.dgamma,
            self.igamma,
        )

    @round_(precision=2)
    def ultimate_bearing_capacity(self) -> float:
        r"""Return the ultimate bearing capacity according to ``Meyerhof``."""
        return self._first_expr + self._mid_expr + 0.5 * self._last_expr

    @property
    def nc(self) -> float:
        return self._meyerhof_factors.nc

    @property
    def nq(self) -> float:
        return self._meyerhof_factors.nq

    @property
    def ngamma(self) -> float:
        return self._meyerhof_factors.ngamma

    @property
    def dc(self) -> float:
        return self._meyerhof_factors.dc

    @property
    def dq(self) -> float:
        return self._meyerhof_factors.dq

    @property
    def dgamma(self) -> float:
        return self._meyerhof_factors.dgamma

    @property
    def sc(self) -> float:
        return self._meyerhof_factors.sc

    @property
    def sq(self) -> float:
        return self._meyerhof_factors.sq

    @property
    def sgamma(self) -> float:
        return self._meyerhof_factors.sgamma

    @property
    def ic(self) -> float:
        return self._meyerhof_factors.ic

    @property
    def iq(self) -> float:
        return self._meyerhof_factors.iq

    @property
    def igamma(self) -> float:
        return self._meyerhof_factors.igamma
