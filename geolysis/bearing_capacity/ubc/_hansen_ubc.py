from geolysis.foundation import Shape
from geolysis.utils import (
    cosdeg,
    cotdeg,
    exp,
    isclose,
    pi,
    round_,
    sindeg,
    tandeg,
    add_repr,
)

from ._core import UltimateBearingCapacity

__all__ = ["HansenUltimateBearingCapacity"]


class HansenBearingCapacityFactors:

    @staticmethod
    @round_(ndigits=2)
    def n_c(friction_angle: float) -> float:
        if isclose(friction_angle, 0.0):
            return 5.14
        return cotdeg(friction_angle) * (
                HansenBearingCapacityFactors.n_q(friction_angle) - 1.0
        )

    @staticmethod
    @round_(ndigits=2)
    def n_q(friction_angle: float) -> float:
        return tandeg(45.0 + friction_angle / 2.0) ** 2.0 * exp(
            pi * tandeg(friction_angle)
        )

    @staticmethod
    @round_(ndigits=2)
    def n_gamma(friction_angle: float) -> float:
        return (
                1.8
                * (HansenBearingCapacityFactors.n_q(friction_angle) - 1.0)
                * tandeg(friction_angle)
        )


class HansenShapeFactors:

    @staticmethod
    @round_(ndigits=2)
    def s_c(f_width: float, f_length: float, f_shape: Shape) -> float:
        if f_shape == Shape.STRIP:
            return 1.0
        elif f_shape == Shape.RECTANGLE:
            return 1.0 + 0.2 * f_width / f_length
        else:  # SQUARE & CIRCLE
            return 1.3

    @staticmethod
    @round_(ndigits=2)
    def s_q(f_width: float, f_length: float, f_shape: Shape) -> float:
        if f_shape == Shape.STRIP:
            return 1.0
        elif f_shape == Shape.RECTANGLE:
            return 1.0 + 0.2 * f_width / f_length
        else:  # SQUARE & CIRCLE
            return 1.2

    @staticmethod
    @round_(ndigits=2)
    def s_gamma(f_width: float, f_length: float, f_shape: Shape) -> float:
        if f_shape == Shape.STRIP:
            return 1.0
        elif f_shape == Shape.RECTANGLE:
            return 1.0 - 0.4 * f_width / f_length
        elif f_shape == Shape.SQUARE:
            return 0.8
        else:  # CIRCLE
            return 0.6


class HansenDepthFactors:

    @staticmethod
    @round_(ndigits=2)
    def d_c(f_depth: float, f_width: float) -> float:
        return 1.0 + 0.35 * f_depth / f_width

    @staticmethod
    @round_(ndigits=2)
    def d_q(f_depth: float, f_width: float) -> float:
        return HansenDepthFactors.d_c(f_depth, f_width)

    @staticmethod
    @round_(ndigits=2)
    def d_gamma() -> float:
        return 1.0


class HansenInclinationFactors:

    @staticmethod
    @round_(ndigits=2)
    def i_c(
            cohesion: float,
            load_angle: float,
            f_width: float,
            f_length: float,
    ) -> float:
        return 1.0 - sindeg(load_angle) / (2.0 * cohesion * f_width * f_length)

    @staticmethod
    @round_(ndigits=2)
    def i_q(load_angle: float) -> float:
        return 1.0 - (1.5 * sindeg(load_angle)) / cosdeg(load_angle)

    @staticmethod
    @round_(ndigits=2)
    def i_gamma(load_angle: float) -> float:
        return HansenInclinationFactors.i_q(load_angle) ** 2.0


@add_repr
class HansenUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for soils according to `Hansen (1961)`.

    See [implementation](../formulas/ultimate-bearing-capacity.md/#hansen-bearing-capacity)
    for more details on bearing capacity equation used.

    """

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor $N_c$."""
        return HansenBearingCapacityFactors.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor $N_q$."""
        return HansenBearingCapacityFactors.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor $N_{\gamma}$."""
        return HansenBearingCapacityFactors.n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        r"""Shape factor $S_c$."""
        width, length, shape = self.foundation_size.footing_params()
        return HansenShapeFactors.s_c(width, length, shape)

    @property
    def s_q(self) -> float:
        r"""Shape factor $S_q$."""
        width, length, shape = self.foundation_size.footing_params()
        return HansenShapeFactors.s_q(width, length, shape)

    @property
    def s_gamma(self) -> float:
        r"""Shape factor $S_{\gamma}$."""
        width, length, shape = self.foundation_size.footing_params()
        return HansenShapeFactors.s_gamma(width, length, shape)

    @property
    def d_c(self) -> float:
        r"""Depth factor $D_c$."""
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        return HansenDepthFactors.d_c(depth, width)

    @property
    def d_q(self) -> float:
        r"""Depth factor $D_q$."""
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        return HansenDepthFactors.d_q(depth, width)

    @property
    def d_gamma(self) -> float:
        r"""Depth factor $D_{\gamma}$."""
        return HansenDepthFactors.d_gamma()

    @property
    def i_c(self) -> float:
        r"""Inclination factor $I_c$."""
        width, length = self.foundation_size.width, self.foundation_size.length
        return HansenInclinationFactors.i_c(
            self.cohesion, self.load_angle, width, length
        )

    @property
    def i_q(self) -> float:
        r"""Inclination factor $I_q$."""
        return HansenInclinationFactors.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor $I_{\gamma}$."""
        return HansenInclinationFactors.i_gamma(self.load_angle)
