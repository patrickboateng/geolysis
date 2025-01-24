from geolysis.bearing_capacity import get_footing_params
from geolysis.bearing_capacity.ubc import UltimateBearingCapacity
from geolysis.bearing_capacity.ubc.hansen_ubc import \
    HansenBearingCapacityFactor
from geolysis.foundation import FoundationSize, Shape
from geolysis.utils import isclose, round_, sin, tan

__all__ = ["VesicBearingCapacityFactor", "VesicShapeFactor",
           "VesicDepthFactor", "VesicInclinationFactor",
           "VesicUltimateBearingCapacity"]


class VesicBearingCapacityFactor:
    """Bearing capacity factors for ultimate bearing capacity according to
    ``Vesic (1973)``.
    """

    @classmethod
    @round_
    def n_c(cls, friction_angle: float) -> float:
        r"""Bearing capacity factor :math:`N_c`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        .. math:: N_c = \cot(\phi) \left(N_q - 1\right)
        """
        return HansenBearingCapacityFactor.n_c(friction_angle)

    @classmethod
    @round_
    def n_q(cls, friction_angle: float) -> float:
        r"""Bearing capacity factor :math:`N_q`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        .. math::

            N_q = \tan^2\left(45 + \frac{\phi}{2}\right) \cdot
                  e^{\pi \tan(\phi)}
        """
        return HansenBearingCapacityFactor.n_q(friction_angle)

    @classmethod
    @round_
    def n_gamma(cls, friction_angle: float) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        .. math:: N_{\gamma} = 2(N_q + 1) \tan(\phi)
        """
        return 2.0 * (cls.n_q(friction_angle) + 1.0) * tan(friction_angle)


class VesicShapeFactor:
    """Shape factors for ultimate bearing capacity according to 
    ``Vesic (1973)``.
    """

    @classmethod
    @round_
    def s_c(cls, friction_angle: float,
            foundation_size: FoundationSize) -> float:
        r"""Shape factor :math:`S_c`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        :raises ValueError: if foundation has an invalid footing shape.

        .. math::

            s_c &= 1.0 \rightarrow \text{Strip footing}

            s_c &= 1 + \dfrac{B}{L} \cdot \dfrac{N_q}{N_c} \rightarrow
                    \text{Rectangular footing}

            s_c &= 1 + \dfrac{N_q}{N_c} \rightarrow
                   \text{Square or circular footing}
        """
        width, length, shape = get_footing_params(foundation_size)

        n_q = VesicBearingCapacityFactor.n_q(friction_angle)
        n_c = VesicBearingCapacityFactor.n_c(friction_angle)

        if shape == Shape.STRIP:
            shape_factor = 1.0
        elif shape == Shape.RECTANGLE:
            shape_factor = 1.0 + (width / length) * (n_q / n_c)
        elif shape in (Shape.SQUARE, Shape.CIRCLE):
            shape_factor = 1.0 + (n_q / n_c)
        else:
            raise ValueError("Invalid footing shape.")

        return shape_factor

    @classmethod
    @round_
    def s_q(cls, friction_angle: float,
            foundation_size: FoundationSize) -> float:
        r"""Shape factor :math:`S_q`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        :raises ValueError: if foundation has an invalid footing shape.

        .. math::

            s_q &= 1.0 \rightarrow \text{Strip footing}

            s_q &= 1 + \dfrac{B}{L} \cdot \tan(\phi) \rightarrow
                   \text{Rectangular footing}

            s_q &= 1 + \tan(\phi) \rightarrow \text{Square or circular footing}

        """
        width, length, shape = get_footing_params(foundation_size)

        if shape == Shape.STRIP:
            shape_factor = 1.0
        elif shape == Shape.RECTANGLE:
            shape_factor = 1.0 + (width / length) * tan(friction_angle)
        elif shape in (Shape.SQUARE, Shape.CIRCLE):
            shape_factor = 1.0 + tan(friction_angle)
        else:
            raise ValueError("Invalid footing shape.")

        return shape_factor

    @classmethod
    @round_
    def s_gamma(cls, foundation_size: FoundationSize) -> float:
        r"""Shape factor :math:`S_{\gamma}`.

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        :raises ValueError: if foundation has an invalid footing shape.

        .. math:: 

            s_{\gamma} = 1.0 \rightarrow \text{Strip footing}

            s_{\gamma} = 1.0 - 0.4 \dfrac{B}{L} \rightarrow
                         \text{Rectangular footing}

            s_{\gamma} = 0.6 \rightarrow \text{Square or circular footing}
        """
        width, length, shape = get_footing_params(foundation_size)

        if shape == Shape.STRIP:
            shape_factor = 1.0
        elif shape == Shape.RECTANGLE:
            shape_factor = 1.0 - 0.4 * (width / length)
        elif shape in (Shape.SQUARE, Shape.CIRCLE):
            shape_factor = 0.6
        else:
            raise ValueError("Invalid footing shape.")

        return shape_factor


class VesicDepthFactor:
    """Depth factors for ultimate bearing capacity according to 
    ``Vesic (1973)``.
    """

    @classmethod
    @round_
    def d_c(cls, foundation_size: FoundationSize) -> float:
        r"""Depth factor :math:`D_c`.

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        .. math:: d_c = 1 + 0.4 \dfrac{D_f}{B}
        """
        depth = foundation_size.depth
        width = foundation_size.width

        return 1.0 + 0.4 * depth / width

    @classmethod
    @round_
    def d_q(cls, friction_angle: float,
            foundation_size: FoundationSize) -> float:
        r"""Depth factor :math:`D_q`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        .. math::

            d_q = 1 + 2 \tan(\phi) \cdot (1 - \sin(\phi))^2
                  \cdot \dfrac{D_f}{B}
        """
        depth = foundation_size.depth
        width = foundation_size.width

        return (1.0 + 2.0 * tan(friction_angle)
                * (1.0 - sin(friction_angle)) ** 2.0
                * (depth / width))

    @classmethod
    @round_
    def d_gamma(cls) -> float:
        r"""Depth factor :math:`D_{\gamma}`.

        .. math:: d_{\gamma} = 1.0
        """
        return 1.0


class VesicInclinationFactor:
    """Inclination factors for ultimate bearing capacity according to
    ``Vesic (1973)``.
    """

    @classmethod
    @round_
    def i_c(cls, load_angle: float) -> float:
        r"""Inclination factor :math:`I_c`.

        :param load_angle: Inclination of the applied load with the  vertical
                           (degrees).
        :type load_angle: float

        .. math:: i_c = (1 - \dfrac{\alpha}{90})^2
        """
        return (1.0 - load_angle / 90.0) ** 2.0

    @classmethod
    @round_
    def i_q(cls, load_angle: float) -> float:
        r"""Inclination factor :math:`I_q`.

        :param load_angle: Inclination of the applied load with the  vertical
                           (degrees).
        :type load_angle: float

        .. math:: i_q = (1 - \dfrac{\alpha}{90})^2
        """
        return cls.i_c(load_angle=load_angle)

    @classmethod
    @round_
    def i_gamma(cls, friction_angle: float, load_angle: float) -> float:
        r"""Inclination factor :math:`I_{\gamma}`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float

        :param load_angle: Inclination of the applied load with the  vertical
                           (degrees).
        :type load_angle: float

        .. math:: i_{\gamma} = \left(1 - \dfrac{\alpha}{\phi} \right)^2
        """
        if isclose(friction_angle, 0.0):
            return 1.0
        return (1.0 - load_angle / friction_angle) ** 2.0


class VesicUltimateBearingCapacity(UltimateBearingCapacity):
    """Ultimate bearing capacity for soils according to ``Vesic (1973)``."""

    @property
    def n_c(self) -> float:
        return VesicBearingCapacityFactor.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        return VesicBearingCapacityFactor.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        return VesicBearingCapacityFactor.n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        return VesicShapeFactor.s_c(self.friction_angle, self.foundation_size)

    @property
    def s_q(self) -> float:
        return VesicShapeFactor.s_q(self.friction_angle, self.foundation_size)

    @property
    def s_gamma(self) -> float:
        return VesicShapeFactor.s_gamma(self.foundation_size)

    @property
    def d_c(self) -> float:
        return VesicDepthFactor.d_c(self.foundation_size)

    @property
    def d_q(self) -> float:
        return VesicDepthFactor.d_q(self.friction_angle, self.foundation_size)

    @property
    def d_gamma(self) -> float:
        return VesicDepthFactor.d_gamma()

    @property
    def i_c(self) -> float:
        return VesicInclinationFactor.i_c(self.load_angle)

    @property
    def i_q(self) -> float:
        return VesicInclinationFactor.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        return VesicInclinationFactor.i_gamma(self.friction_angle,
                                              self.load_angle)

    @round_
    def bearing_capacity(self) -> float:
        r"""Calculates ultimate bearing capacity.
        
        .. math::

            q_u = cN_c s_c d_c i_c + qN_q s_q d_q i_q
                  + 0.5 \gamma B N_{\gamma} s_{\gamma} d_{\gamma}
        """
        return super().bearing_capacity()
