from abc import ABC

from geolysis.utils import cos, cot, deg2rad, exp, isclose, pi, round_, tan
from ._core import UltimateBearingCapacity

__all__ = [
    "TerzaghiUBC4StripFooting",
    "TerzaghiUBC4CircularFooting",
    "TerzaghiUBC4SquareFooting",
    "TerzaghiUBC4RectangularFooting",
]

from geolysis.foundation import Foundation


class TerzaghiBearingCapacityFactors:

    @staticmethod
    @round_(ndigits=2)
    def n_c(friction_angle: float) -> float:
        if isclose(friction_angle, 0.0):
            return 5.7
        return cot(friction_angle) * (
                TerzaghiBearingCapacityFactors.n_q(friction_angle) - 1.0
        )

    @staticmethod
    @round_(ndigits=2)
    def n_q(friction_angle: float) -> float:
        return exp((3.0 * pi / 2.0 - deg2rad(friction_angle)) * tan(
            friction_angle)) / (
                2.0 * (cos(45.0 + friction_angle / 2.0)) ** 2.0
        )

    @staticmethod
    @round_(ndigits=2)
    def n_gamma(friction_angle: float) -> float:
        return (TerzaghiBearingCapacityFactors.n_q(
            friction_angle) - 1.0) * tan(
            1.4 * friction_angle
        )


class TerzaghiUltimateBearingCapacity(UltimateBearingCapacity, ABC):

    def __init__(
            self,
            friction_angle: float,
            cohesion: float,
            moist_unit_wgt: float,
            foundation_size: Foundation,
            apply_local_shear: bool = False,
    ) -> None:
        r"""
        :param friction_angle: Internal angle of friction for general
                               shear failure (degrees).
        :param cohesion: Cohesion of soil ($kPa$).
        :param moist_unit_wgt: Moist unit weight of soil ($kN/m^3$).
        :param foundation_size: Size of the foundation.
        :param apply_local_shear: Indicate whether bearing capacity
                                  failure is general shear or local
                                  shear failure.
        """
        super().__init__(
            friction_angle=friction_angle,
            cohesion=cohesion,
            moist_unit_wgt=moist_unit_wgt,
            foundation_size=foundation_size,
            apply_local_shear=apply_local_shear,
        )

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor $N_c$."""
        return TerzaghiBearingCapacityFactors.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor $N_q$."""
        return TerzaghiBearingCapacityFactors.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor $N_{\gamma}$."""
        return TerzaghiBearingCapacityFactors.n_gamma(self.friction_angle)


class TerzaghiUBC4StripFooting(TerzaghiUltimateBearingCapacity):
    """Ultimate bearing capacity for strip footing according to
    `Terzaghi 1943`.

    See [implementation](../formulas/ultimate-bearing-capacity.md/#terzaghi-bearing-capacity-for-strip-footing)
    for more details on bearing capacity equation used.
    """

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity for strip footing."""
        return (
                self._cohesion_term(1.0)
                + self._surcharge_term()
                + self._embedment_term(0.5)
        )


class TerzaghiUBC4CircularFooting(TerzaghiUltimateBearingCapacity):
    """Ultimate bearing capacity for circular footing according to
    `Terzaghi 1943`.

    See [implementation](../formulas/ultimate-bearing-capacity.md/#terzaghi-bearing-capacity-for-circular-footing)
    for more details on bearing capacity equation used.
    """

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity for circular footing."""
        return (
                self._cohesion_term(1.3)
                + self._surcharge_term()
                + self._embedment_term(0.3)
        )


class TerzaghiUBC4RectangularFooting(TerzaghiUltimateBearingCapacity):
    r"""Ultimate bearing capacity for rectangular footing according to
    `Terzaghi 1943`.

    See [implementation](../formulas/ultimate-bearing-capacity.md/#terzaghi-bearing-capacity-for-rectangular-footing)
    for more details on bearing capacity equation used.
    """

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity for rectangular footing."""
        width = self.foundation_size.width
        length = self.foundation_size.length
        coh_coef = 1.0 + 0.3 * (width / length)
        emb_coef = (1.0 - 0.2 * (width / length)) / 2.0

        return (
                self._cohesion_term(coh_coef)
                + self._surcharge_term()
                + self._embedment_term(emb_coef)
        )


class TerzaghiUBC4SquareFooting(TerzaghiUBC4RectangularFooting):
    """Ultimate bearing capacity for square footing according to
    `Terzaghi 1943``.

    See [implementation](../formulas/ultimate-bearing-capacity.md/#terzaghi-bearing-capacity-for-square-footing)
    for more details on bearing capacity equation used.
    """

    def bearing_capacity(self):
        """Calcalates ultimate bearing capacity for square footing."""
        return super().bearing_capacity()
