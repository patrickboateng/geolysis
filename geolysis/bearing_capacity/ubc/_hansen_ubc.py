from geolysis.foundation import Shape
from geolysis.utils import cos, cot, exp, isclose, pi, round_, sin, tan

from ._core import UltimateBearingCapacity

__all__ = ["HansenUltimateBearingCapacity"]


class HansenBearingCapacityFactors:

    @staticmethod
    @round_(ndigits=2)
    def n_c(friction_angle: float) -> float:
        if isclose(friction_angle, 0.0):
            return 5.14
        return cot(friction_angle) * (
            HansenBearingCapacityFactors.n_q(friction_angle) - 1.0
        )

    @staticmethod
    @round_(ndigits=2)
    def n_q(friction_angle: float) -> float:
        return tan(45.0 + friction_angle / 2.0) ** 2.0 * exp(pi * tan(friction_angle))

    @staticmethod
    @round_(ndigits=2)
    def n_gamma(friction_angle: float) -> float:
        return (
            1.8
            * (HansenBearingCapacityFactors.n_q(friction_angle) - 1.0)
            * tan(friction_angle)
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
        return 1.0 - sin(load_angle) / (2.0 * cohesion * f_width * f_length)

    @staticmethod
    @round_(ndigits=2)
    def i_q(load_angle: float) -> float:
        return 1.0 - (1.5 * sin(load_angle)) / cos(load_angle)

    @staticmethod
    @round_(ndigits=2)
    def i_gamma(load_angle: float) -> float:
        return HansenInclinationFactors.i_q(load_angle) ** 2.0


class HansenUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for soils according to `Hansen (1961)`."""

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor $N_c$.

        $$
        N_c = \cot(\phi) \left(N_q - 1\right)
        $$
        """
        return HansenBearingCapacityFactors.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor $N_q$.

        $$
        N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot e^{\pi \tan(\phi)}
        $$
        """
        return HansenBearingCapacityFactors.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor $N_{\gamma}$.

        $$
        N_{\gamma} = 1.8 \left(N_q - 1\right) \tan(\phi)
        $$
        """
        return HansenBearingCapacityFactors.n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        r"""Shape factor $S_c$.

        $$
        s_c = 1.0 \rightarrow \text{Strip footing}
        $$

        $$
        s_c = 1.0 + 0.2 \frac{B}{L} \rightarrow \text{Rectangular footing}
        $$

        $$
        s_c = 1.3 \rightarrow \text{Square or circular footing}
        $$
        """
        width, length, shape = self.foundation_size.footing_params()
        return HansenShapeFactors.s_c(width, length, shape)

    @property
    def s_q(self) -> float:
        r"""Shape factor $S_q$.

        $$
        s_q = 1.0 \rightarrow \text{Strip footing}
        $$

        $$
        s_q = 1.0 + 0.2 \cdot \frac{B}{L} \rightarrow \text{Rectangular footing}
        $$

        $$
        s_q = 1.2 \rightarrow \text{Square or circular footing}
        $$
        """
        width, length, shape = self.foundation_size.footing_params()
        return HansenShapeFactors.s_q(width, length, shape)

    @property
    def s_gamma(self) -> float:
        r"""Shape factor $S_{\gamma}$.

        $$
        s_{\gamma} = 1.0 \rightarrow \text{Strip footing}
        $$

        $$
        s_{\gamma} = 1.0 - 0.4 \frac{B}{L} \rightarrow
                      \text{Rectangular footing}
        $$

        $$
        s_{\gamma} = 0.8 \rightarrow \text{Square footing}
        $$

        $$
        s_{\gamma} = 0.6 \rightarrow \text{Circular footing}
        $$
        """
        width, length, shape = self.foundation_size.footing_params()
        return HansenShapeFactors.s_gamma(width, length, shape)

    @property
    def d_c(self) -> float:
        r"""Depth factor $D_c$.

        $$
        d_c = 1.0 + 0.35 \cdot \frac{D_f}{B}
        $$
        """
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        return HansenDepthFactors.d_c(depth, width)

    @property
    def d_q(self) -> float:
        r"""Depth factor $D_q$.

        $$
        d_q = 1.0 + 0.35 \cdot \frac{D_f}{B}
        $$
        """
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        return HansenDepthFactors.d_q(depth, width)

    @property
    def d_gamma(self) -> float:
        r"""Depth factor $D_{\gamma}$.

        $$
        d_{\gamma} = 1.0
        $$
        """
        return HansenDepthFactors.d_gamma()

    @property
    def i_c(self) -> float:
        r"""Inclination factor $I_c$.

        $$
        I_c = 1 - \frac{\sin(\alpha)}{2cBL}
        $$
        """
        width, length = self.foundation_size.width, self.foundation_size.length
        return HansenInclinationFactors.i_c(
            self.cohesion, self.load_angle, width, length
        )

    @property
    def i_q(self) -> float:
        r"""Inclination factor $I_q$.

        $$
        I_q = 1 - \frac{1.5 \sin(\alpha)}{\cos(\alpha)}
        $$
        """
        return HansenInclinationFactors.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor $I_{\gamma}$.

        $$
        I_{\gamma} = I_q^2
        $$
        """
        return HansenInclinationFactors.i_gamma(self.load_angle)
