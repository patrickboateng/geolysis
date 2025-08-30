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

        | SYMBOL                        | DESCRIPTION                  | UNIT       |
        |--------------------------------|------------------------------|------------|
        | $q_u$                          | Ultimate bearing capacity    | $kPa$     |
        | $c$                            | Cohesion of soil             | $kPa$     |
        | $q$                            | Overburden pressure of soil  | $kPa$     |
        | $\gamma$                        | Unit weight of soil          | $kN/m^3$  |
        | $B$                            | Width of foundation footing  | $m$       |
        |$L$                             | Length of foundation footing     | $m$       |
        | $N_c$, $N_q$, $N_{\gamma}$     | Bearing capacity factors     | —          |


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
        r"""Bearing capacity factor $N_c$.

        $$N_c = \cot(\phi) \cdot (N_q - 1)$$
        """
        return TerzaghiBearingCapacityFactors.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor $N_q$.

        $$
        N_q = \dfrac{e^{(\frac{3\pi}{2} - \phi)\tan\phi}}
                    {2\cos^2(45 + \frac{\phi}{2})}
        $$
        """
        return TerzaghiBearingCapacityFactors.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor $N_{\gamma}$.

        $$N_{\gamma} =  (N_q - 1) \cdot \tan(1.4\phi)$$
        """
        return TerzaghiBearingCapacityFactors.n_gamma(self.friction_angle)


class TerzaghiUBC4StripFooting(TerzaghiUltimateBearingCapacity):
    r"""Ultimate bearing capacity for strip footing according to
    `Terzaghi 1943`.

    $$q_u = cN_c + qN_q + 0.5 \gamma BN_{\gamma}$$
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
    r"""Ultimate bearing capacity for circular footing according to
    `Terzaghi 1943`.

    $$q_u = 1.3cN_c + qN_q + 0.3 \gamma BN_{\gamma}$$
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

    $$
    q_u = \left(1 + 0.3 \dfrac{B}{L} \right) c N_c + qN_q
          + \left(1 - 0.2 \dfrac{B}{L} \right) 0.5 B \gamma N_{\gamma}
    $$
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
    r"""Ultimate bearing capacity for square footing according to
    `Terzaghi 1943``.

    $$q_u = 1.3cN_c + qN_q + 0.4 \gamma BN_{\gamma}$$
    """

    def bearing_capacity(self):
        """Calcalates ultimate bearing capacity for square footing."""
        return super().bearing_capacity()
