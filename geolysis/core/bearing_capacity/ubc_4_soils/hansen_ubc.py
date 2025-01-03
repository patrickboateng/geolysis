from geolysis.core._config.config import UnitReg
from geolysis.core.bearing_capacity.ubc_4_soils import (
    DP,
    Soil,
    UltimateBearingCapacity,
    k,
)
from geolysis.core.foundation import FoundationSize, Shape
from geolysis.core.utils import (
    INF,
    PI,
    cos,
    cot,
    exp,
    isclose,
    quantity,
    round_,
    sin,
    tan,
)

__all__ = ["HansenUltimateBearingCapacity"]


class HansenBearingCapacityFactor:
    @classmethod
    @round_(DP)
    def n_c(cls, f_angle: float) -> float:
        return (
            5.14
            if isclose(f_angle, 0.0)
            else cot(f_angle) * (cls.n_q(f_angle) - 1)
        )

    @classmethod
    @round_(DP)
    def n_q(cls, f_angle: float) -> float:
        return (tan(45 + f_angle / 2)) ** 2 * (exp(PI * tan(f_angle)))

    @classmethod
    @round_(DP)
    def n_gamma(cls, f_angle) -> float:
        return 1.8 * (cls.n_q(f_angle) - 1) * tan(f_angle)


class HansenShapeFactor:
    @classmethod
    @round_(DP)
    def s_c(cls, foundation_size: FoundationSize) -> float:
        f_w = foundation_size.effective_width
        f_l = foundation_size.length
        f_type = foundation_size.footing_shape

        if not isclose(f_w, f_l) and f_type != Shape.STRIP:
            f_type = Shape.RECTANGLE

        match f_type:
            case Shape.STRIP:
                sf = 10.0
            case Shape.RECTANGLE:
                sf = 1 + 0.2 * f_w / f_l
            case Shape.SQUARE | Shape.CIRCLE:
                sf = 1.3
            case _:
                raise ValueError

        return sf

    @classmethod
    @round_(DP)
    def s_q(cls, foundation_size: FoundationSize) -> float:
        f_w = foundation_size.effective_width
        f_l = foundation_size.length
        f_type = foundation_size.footing_shape

        if not isclose(f_w, f_l) and f_type != Shape.STRIP:
            f_type = Shape.RECTANGLE

        match f_type:
            case Shape.STRIP:
                sf = 1.0
            case Shape.RECTANGLE:
                sf = 1 + 0.2 * f_w / f_l
            case Shape.SQUARE | Shape.CIRCLE:
                sf = 1.2
            case _:
                raise ValueError

        return sf

    @classmethod
    @round_(DP)
    def s_gamma(cls, foundation_size: FoundationSize) -> float:
        f_w = foundation_size.effective_width
        f_l = foundation_size.length
        f_type = foundation_size.footing_shape

        if not isclose(f_w, f_l) and f_type != Shape.STRIP:
            f_type = Shape.RECTANGLE

        match f_type:
            case Shape.STRIP:
                sf = 1.0
            case Shape.RECTANGLE:
                sf = 1 - 0.4 * f_w / f_l
            case Shape.SQUARE:
                sf = 0.8
            case Shape.CIRCLE:
                sf = 0.6
            case _:
                raise ValueError

        return sf


class HansenDepthFactor:
    @classmethod
    @round_(DP)
    def d_c(cls, foundation_size: FoundationSize) -> float:
        f_d = foundation_size.depth
        f_w = foundation_size.width

        return 1 + 0.4 * k(f_d, f_w)

    @classmethod
    @round_(DP)
    def d_q(cls, f_angle: float, foundation_size: FoundationSize) -> float:
        f_d = foundation_size.depth
        f_w = foundation_size.width

        if f_angle > 25.0:
            return cls.d_c(foundation_size)

        return 1 + 2 * tan(f_angle) * (1 - sin(f_angle)) ** 2 * k(f_d, f_w)

    @classmethod
    @round_(DP)
    def d_gamma(cls) -> float:
        return 1.0


class HansenInclinationFactor:
    @classmethod
    @round_(DP)
    def i_c(
        cls,
        cohesion: float,
        load_angle: float,
        foundation_size: FoundationSize,
    ) -> float:
        f_w = foundation_size.width
        f_l = foundation_size.length
        return 1 - cos(load_angle) / (2 * cohesion * f_w * f_l)

    @classmethod
    @round_(DP)
    def i_q(cls, load_angle: float) -> float:
        return 1 - (1.5 * cos(load_angle)) / sin(load_angle)

    @classmethod
    @round_(DP)
    def i_gamma(cls, load_angle: float) -> float:
        return cls.i_q(load_angle) ** 2


class HansenUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for footings on cohesionless soils according
    to ``Hansen 1961``.

    :param float soil_friction_angle: Internal angle of friction of soil
        material.
    :param float cohesion: Cohesion of soil material.
    :param float moist_unit_wgt: Moist (Bulk) unit weight of soil material.
    :param FoundationSize foundation_size: Size of foundation.
    :param float water_level: Depth of water below the ground surface.
    :param float local_shear_failure: Indicates if local shear failure is likely
        to occur therefore modifies the soil_friction_angle and cohesion of the
        soil material.

    Notes
    -----
    Ultimate bearing capacity for circular footing is given by the formula:

    .. math::

        q_u = cN_c s_c d_c i_c + qN_q s_q d_q i_q
              + 0.5 \gamma B N_{\gamma} s_{\gamma} d_{\gamma}

    Examples
    --------

    """

    def __init__(
        self,
        soil_properties: Soil,
        foundation_size: FoundationSize,
        water_level: float = INF,
        load_angle_incl: float = 90,
        apply_local_shear: bool = False,
    ) -> None:
        super().__init__(
            soil_properties,
            foundation_size,
            water_level,
            apply_local_shear,
        )

        self.load_angle = load_angle_incl

        self.bearing_cpty_factor = HansenBearingCapacityFactor()
        self.shape_factor = HansenShapeFactor()
        self.depth_factor = HansenDepthFactor()
        self.incl_factor = HansenInclinationFactor()

    @property
    def n_c(self) -> float:
        return self.bearing_cpty_factor.n_c(self.friction_angle)

    @property
    def n_q(self) -> float:
        return self.bearing_cpty_factor.n_q(self.friction_angle)

    @property
    def n_gamma(self) -> float:
        return self.bearing_cpty_factor.n_gamma(self.friction_angle)

    @property
    def s_c(self) -> float:
        return self.shape_factor.s_c(self.foundation_size)

    @property
    def s_q(self) -> float:
        return self.shape_factor.s_q(self.foundation_size)

    @property
    def s_gamma(self) -> float:
        return self.shape_factor.s_gamma(self.foundation_size)

    @property
    def d_c(self) -> float:
        return self.depth_factor.d_c(self.foundation_size)

    @property
    def d_q(self) -> float:
        return self.depth_factor.d_q(self.friction_angle, self.foundation_size)

    @property
    def d_gamma(self) -> float:
        return self.depth_factor.d_gamma()

    @property
    def i_c(self) -> float:
        return self.incl_factor.i_c(
            self.cohesion,
            self.load_angle,
            self.foundation_size,
        )

    @property
    def i_q(self) -> float:
        return self.incl_factor.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        return self.incl_factor.i_gamma(self.load_angle)

    @quantity(unit=UnitReg.kPa)
    @round_
    def bearing_capacity(self) -> float:
        """Ultimate bearing capacity of soil."""
        return (
            self._cohesion_term(1)
            + self._surcharge_term()
            + self._embedment_term(0.5)
        )
