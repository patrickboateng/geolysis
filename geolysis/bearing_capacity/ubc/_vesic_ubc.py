from geolysis.foundation import Shape
from geolysis.utils import isclose, round_, sin, tan
from ._core import UltimateBearingCapacity
from ._hansen_ubc import HansenBearingCapacityFactors

__all__ = ["VesicUltimateBearingCapacity"]


class VesicBearingCapacityFactors:

    @staticmethod
    @round_(ndigits=2)
    def n_c(friction_angle: float) -> float:
        return HansenBearingCapacityFactors.n_c(friction_angle)

    @staticmethod
    @round_(ndigits=2)
    def n_q(friction_angle: float) -> float:
        return HansenBearingCapacityFactors.n_q(friction_angle)

    @staticmethod
    @round_(ndigits=2)
    def n_gamma(friction_angle: float) -> float:
        return (
                2.0
                * (VesicBearingCapacityFactors.n_q(friction_angle) + 1.0)
                * tan(friction_angle)
        )


class VesicShapeFactors:
    @staticmethod
    @round_(ndigits=2)
    def s_c(
            friction_angle: float,
            f_width: float,
            f_length: float,
            f_shape: Shape,
    ) -> float:
        _n_q = VesicBearingCapacityFactors.n_q(friction_angle)
        _n_c = VesicBearingCapacityFactors.n_c(friction_angle)

        if f_shape == Shape.STRIP:
            return 1.0
        elif f_shape == Shape.RECTANGLE:
            return 1.0 + (f_width / f_length) * (_n_q / _n_c)
        else:  # SQUARE, CIRCLE
            return 1.0 + (_n_q / _n_c)

    @staticmethod
    @round_(ndigits=2)
    def s_q(
            friction_angle: float,
            f_width: float,
            f_length: float,
            f_shape: Shape,
    ) -> float:
        if f_shape == Shape.STRIP:
            return 1.0
        elif f_shape == Shape.RECTANGLE:
            return 1.0 + (f_width / f_length) * tan(friction_angle)
        else:  # SQUARE, CIRCLE
            return 1.0 + tan(friction_angle)

    @staticmethod
    @round_(ndigits=2)
    def s_gamma(f_width: float, f_length: float, f_shape: Shape) -> float:
        if f_shape == Shape.STRIP:
            return 1.0
        elif f_shape == Shape.RECTANGLE:
            return 1.0 - 0.4 * (f_width / f_length)
        else:  # SQUARE, CIRCLE
            return 0.6


class VesicDepthFactors:

    @staticmethod
    @round_(ndigits=2)
    def d_c(f_depth: float, f_width: float) -> float:
        return 1.0 + 0.4 * f_depth / f_width

    @staticmethod
    @round_(ndigits=2)
    def d_q(friction_angle: float, f_depth: float, f_width: float) -> float:
        return 1.0 + 2.0 * tan(friction_angle) * (
                    1.0 - sin(friction_angle)) ** 2.0 * (
                f_depth / f_width
        )

    @staticmethod
    @round_(ndigits=2)
    def d_gamma() -> float:
        return 1.0


class VesicInclinationFactors:

    @staticmethod
    @round_(ndigits=2)
    def i_c(load_angle: float) -> float:
        return (1.0 - load_angle / 90.0) ** 2.0

    @staticmethod
    @round_(ndigits=2)
    def i_q(load_angle: float) -> float:
        return VesicInclinationFactors.i_c(load_angle)

    @staticmethod
    @round_(ndigits=2)
    def i_gamma(friction_angle: float, load_angle: float) -> float:
        if isclose(friction_angle, 0.0):
            return 1.0
        return (1.0 - load_angle / friction_angle) ** 2.0


class VesicUltimateBearingCapacity(UltimateBearingCapacity):
    """Ultimate bearing capacity for soils according to `Vesic (1973)`."""

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor $N_c$.

        $$N_c = \cot(\phi) \left(N_q - 1\right)$$
        """
        return VesicBearingCapacityFactors.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor $N_q$.

        $$
        N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot
               e^{\pi \tan(\phi)}
        $$
        """
        return VesicBearingCapacityFactors.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor $N_{\gamma}$.

        $$N_{\gamma} = 2(N_q + 1) \tan(\phi)$$
        """
        return VesicBearingCapacityFactors.n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        r"""Shape factor $S_c$.

        $$s_c = 1.0 \rightarrow \text{Strip footing}$$

        $$
        s_c = 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c} \rightarrow
                 \text{Rectangular footing}
        $$

        $$
        s_c &= 1 + \dfrac{N_q}{N_c} \rightarrow
                \text{Square or circular footing}
        $$
        """
        width, length, shape = self.foundation_size.footing_params()
        return VesicShapeFactors.s_c(self.friction_angle, width, length, shape)

    @property
    def s_q(self) -> float:
        r"""Shape factor $S_q$.


        $$s_q = 1.0 \rightarrow \text{Strip footing}$$

        $$
        s_q = 1 + \dfrac{B}{L} \cdot \tan(\phi) \rightarrow
                     \text{Rectangular footing}
        $$

        $$
        s_q = 1 + \tan(\phi) \rightarrow \text{Square or circular footing}
        $$
        """
        width, length, shape = self.foundation_size.footing_params()
        return VesicShapeFactors.s_q(self.friction_angle, width, length, shape)

    @property
    def s_gamma(self) -> float:
        r"""Shape factor $S_{\gamma}$.

        $$s_{\gamma} = 1.0 \rightarrow \text{Strip footing}$$

        $$
        s_{\gamma} = 1.0 - 0.4 \dfrac{B}{L} \rightarrow
                        \text{Rectangular footing}
        $$

        $$
        s_{\gamma} = 0.6 \rightarrow \text{Square or circular footing}
        $$
        """
        width, length, shape = self.foundation_size.footing_params()
        return VesicShapeFactors.s_gamma(width, length, shape)

    @property
    def d_c(self) -> float:
        r"""Depth factor $D_c$.

        $$d_c = 1 + 0.4 \dfrac{D_f}{B}$$
        """
        depth, width = self.foundation_size.depth, self.foundation_size.width
        return VesicDepthFactors.d_c(depth, width)

    @property
    def d_q(self) -> float:
        r"""Depth factor $D_q$.

        $$
        d_q = 1 + 2 \tan(\phi) \cdot (1 - \sin(\phi))^2
              \cdot \dfrac{D_f}{B}
        $$
        """
        depth, width = self.foundation_size.depth, self.foundation_size.width
        return VesicDepthFactors.d_q(self.friction_angle, depth, width)

    @property
    def d_gamma(self) -> float:
        r"""Depth factor $D_{\gamma}$.

        $$d_{\gamma} = 1.0$$
        """
        return VesicDepthFactors.d_gamma()

    @property
    def i_c(self) -> float:
        r"""Inclination factor $I_c$.

        $$i_c = (1 - \dfrac{\alpha}{90})^2$$
        """
        return VesicInclinationFactors.i_c(self.load_angle)

    @property
    def i_q(self) -> float:
        r"""Inclination factor $I_q$.

        $$i_q = (1 - \dfrac{\alpha}{90})^2$$
        """
        return VesicInclinationFactors.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor $I_{\gamma}$.

        $$i_{\gamma} = \left(1 - \dfrac{\alpha}{\phi} \right)^2$$
        """
        return VesicInclinationFactors.i_gamma(self.friction_angle,
                                               self.load_angle)
