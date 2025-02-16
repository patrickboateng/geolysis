from geolysis.bearing_capacity import get_footing_params
from geolysis.bearing_capacity.ubc import UltimateBearingCapacity
from geolysis.foundation import FoundationSize, Shape
from geolysis.utils import cos, cot, exp, isclose, pi, round_, sin, tan

__all__ = ["HansenBearingCapacityFactor",
           "HansenShapeFactor",
           "HansenDepthFactor",
           "HansenInclinationFactor",
           "HansenDepthFactor",
           "HansenUltimateBearingCapacity"]


class HansenBearingCapacityFactor:
    r"""Bearing capacity factors for ultimate bearing capacity according to
    ``Hansen (1961)``.

    .. math::

           N_c &= \cot(\phi) \left(N_q - 1\right)

           N_q &= \tan^2\left(45 + \frac{\phi}{2}\right) \cdot
                  e^{\pi \tan(\phi)}

           N_{\gamma} &= 1.8 \left(N_q - 1\right) \tan(\phi)
    """

    @classmethod
    @round_
    def n_c(cls, friction_angle: float) -> float:
        """Bearing capacity factor :math:`N_c`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float
        """
        if isclose(friction_angle, 0.0):
            return 5.14
        return cot(friction_angle) * (cls.n_q(friction_angle) - 1.0)

    @classmethod
    @round_
    def n_q(cls, friction_angle: float) -> float:
        """Bearing capacity factor :math:`N_q`.

        :param friction_angle: Angle of internal friction of the soil (degrees).
        :type friction_angle: float
        """
        return (tan(45.0 + friction_angle / 2.0) ** 2.0
                * exp(pi * tan(friction_angle)))

    @classmethod
    @round_
    def n_gamma(cls, friction_angle: float) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.

        :param friction_angle: Angle of internal friction of the soil (degrees). 
        :type friction_angle: float
        """
        return 1.8 * (cls.n_q(friction_angle) - 1.0) * tan(friction_angle)


class HansenShapeFactor:
    r"""Shape factors for ultimate bearing capacity according to
    ``Hansen (1961)``.

    .. math::

            s_c &= 1.0 \rightarrow \text{Strip footing}

            s_c &= 1.0 + 0.2 \frac{B}{L} \rightarrow \text{Rectangular footing}

            s_c &= 1.3 \rightarrow \text{Square or circular footing}

    .. math::

            s_q &= 1.0 \rightarrow \text{Strip footing}

            s_q &= 1.0 + 0.2 \frac{B}{L} \rightarrow \text{Rectangular footing}

            s_q &= 1.2 \rightarrow \text{Square or circular footing}

    .. math::

            s_{\gamma} &= 1.0 \rightarrow \text{Strip footing}

            s_{\gamma} &= 1.0 - 0.4 \frac{B}{L} \rightarrow
                          \text{Rectangular footing}

            s_{\gamma} &= 0.8 \rightarrow \text{Square footing}

            s_{\gamma} &= 0.6 \rightarrow \text{Circular footing}
    """

    @classmethod
    @round_
    def s_c(cls, foundation_size: FoundationSize) -> float:
        """Shape factor :math:`S_c`.
        
        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        :raises ValueError: If foundation has an invalid footing shape.
        """
        width, length, shape = get_footing_params(foundation_size)

        if shape == Shape.STRIP:
            shape_factor = 1.0
        elif shape == Shape.RECTANGLE:
            shape_factor = 1.0 + 0.2 * width / length
        elif shape in (Shape.SQUARE, Shape.CIRCLE):
            shape_factor = 1.3
        else:
            raise ValueError("Invalid footing shape.")

        return shape_factor

    @classmethod
    @round_
    def s_q(cls, foundation_size: FoundationSize) -> float:
        """Shape factor :math:`S_q`.

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        :raises ValueError: If foundation has an invalid footing shape.
        """
        width, length, shape = get_footing_params(foundation_size)

        if shape == Shape.STRIP:
            shape_factor = 1.0
        elif shape == Shape.RECTANGLE:
            shape_factor = 1.0 + 0.2 * width / length
        elif shape in (Shape.SQUARE, Shape.CIRCLE):
            shape_factor = 1.2
        else:
            raise ValueError("Invalid footing shape.")

        return shape_factor

    @classmethod
    @round_
    def s_gamma(cls, foundation_size: FoundationSize) -> float:
        r"""Shape factor :math:`S_{\gamma}`.
        
        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize

        :raises ValueError: If foundation has an invalid footing shape.
        """
        width, length, shape = get_footing_params(foundation_size)

        if shape == Shape.STRIP:
            shape_factor = 1.0
        elif shape == Shape.RECTANGLE:
            shape_factor = 1.0 - 0.4 * width / length
        elif shape == Shape.SQUARE:
            shape_factor = 0.8
        elif shape == Shape.CIRCLE:
            shape_factor = 0.6
        else:
            raise ValueError("Invalid footing shape.")

        return shape_factor


class HansenDepthFactor:
    r"""Depth factors for ultimate bearing capacity according to
    ``Hansen (1961)``.

    .. math::

            d_c &= 1.0 + 0.35 \cdot \frac{D_f}{B}

            d_q &= 1.0 + 0.35 \cdot \frac{D_f}{B}

            d_{\gamma} &= 1.0
    """

    @classmethod
    @round_
    def d_c(cls, foundation_size: FoundationSize) -> float:
        """Depth factor :math:`D_c`.
        
        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize
        """
        depth = foundation_size.depth
        width = foundation_size.width

        return 1.0 + 0.35 * depth / width

    @classmethod
    @round_
    def d_q(cls, foundation_size: FoundationSize) -> float:
        """Depth factor :math:`D_q`.

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize
        """
        return cls.d_c(foundation_size)

    @classmethod
    @round_
    def d_gamma(cls) -> float:
        r"""Depth factor :math:`D_{\gamma}`."""
        return 1.0


class HansenInclinationFactor:
    r"""Inclination factors for ultimate bearing capacity according to
    ``Hansen (1961)``.

    .. math::

            I_c &= 1 - \frac{\sin(\alpha)}{2cBL}

            I_q &= 1 - \frac{1.5 \sin(\alpha)}{\cos(\alpha)}

            I_{\gamma} &= I_q^2
    """

    @classmethod
    @round_
    def i_c(cls, cohesion: float, load_angle: float,
            foundation_size: FoundationSize) -> float:
        """Inclination factor :math:`I_c`.
        
        :param cohesion: Cohesion of the soil between footing and soil (kPa).
        :type cohesion: float

        :param load_angle: Inclination of the applied load with the vertical 
                           (degrees)
        :type load_angle: float

        :param foundation_size: Size of the foundation.
        :type foundation_size: FoundationSize
        """
        width = foundation_size.width
        length = foundation_size.length

        return 1.0 - sin(load_angle) / (2.0 * cohesion * width * length)

    @classmethod
    @round_
    def i_q(cls, load_angle: float) -> float:
        """Inclination factor :math:`I_q`.

        :param load_angle: Inclination of the applied load with the vertical
                           (degrees).
        :type load_angle: float
        """
        return 1.0 - (1.5 * sin(load_angle)) / cos(load_angle)

    @classmethod
    @round_
    def i_gamma(cls, load_angle: float) -> float:
        r"""Inclination factor :math:`I_{\gamma}`.

        :param load_angle: Inclination of the applied load with the vertical
                           (degrees).
        :type load_angle: float
        """
        return cls.i_q(load_angle) ** 2.0


class HansenUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for soils according to ``Hansen (1961)``.

    .. math::

            q_u = cN_c s_c d_c i_c + qN_q s_q d_q i_q
                  + 0.5 \gamma B N_{\gamma} s_{\gamma} d_{\gamma}
    """

    @property
    def n_c(self) -> float:
        return HansenBearingCapacityFactor.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        return HansenBearingCapacityFactor.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        return HansenBearingCapacityFactor.n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        return HansenShapeFactor.s_c(self.foundation_size)

    @property
    def s_q(self) -> float:
        return HansenShapeFactor.s_q(self.foundation_size)

    @property
    def s_gamma(self) -> float:
        return HansenShapeFactor.s_gamma(self.foundation_size)

    @property
    def d_c(self) -> float:
        return HansenDepthFactor.d_c(self.foundation_size)

    @property
    def d_q(self) -> float:
        return HansenDepthFactor.d_q(self.foundation_size)

    @property
    def d_gamma(self) -> float:
        return HansenDepthFactor.d_gamma()

    @property
    def i_c(self) -> float:
        return HansenInclinationFactor.i_c(self.cohesion,
                                           self.load_angle,
                                           self.foundation_size)

    @property
    def i_q(self) -> float:
        return HansenInclinationFactor.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        return HansenInclinationFactor.i_gamma(self.load_angle)

    @round_
    def bearing_capacity(self) -> float:
        """Calculates ultimate bearing capacity."""
        return super().bearing_capacity()
