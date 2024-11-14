from src._config.config import UnitReg
from src.bearing_capacity.ubc_4_soils import (
    SoilProperties,
    UltimateBearingCapacity,
    k,
)
from src.bearing_capacity.ubc_4_soils.hansen_ubc import (
    HansenBearingCapacityFactor,
    HansenDepthFactor,
)
from src.foundation import FoundationSize, Shape
from src.utils import INF, isclose, quantity, round_, sin, tan

__all__ = ["VesicUltimateBearingCapacity"]


class VesicBearingCapacityFactor:
    @classmethod
    @round_
    def n_c(cls, f_angle: float) -> float:
        return HansenBearingCapacityFactor.n_c(f_angle)

    @classmethod
    @round_
    def n_q(cls, f_angle: float) -> float:
        return HansenBearingCapacityFactor.n_q(f_angle)

    @classmethod
    @round_
    def n_gamma(cls, f_angle: float) -> float:
        return 2 * (cls.n_q(f_angle) + 1) * tan(f_angle)


class VesicShapeFactor:
    @classmethod
    @round_
    def s_c(cls, f_angle: float, foundation_size: FoundationSize) -> float:
        f_w = foundation_size.effective_width
        f_l = foundation_size.length
        f_type = foundation_size.footing_shape

        if not isclose(f_w, f_l) and f_type != Shape.STRIP:
            f_type = Shape.RECTANGLE

        n_q = VesicBearingCapacityFactor.n_q(f_angle)
        n_c = VesicBearingCapacityFactor.n_c(f_angle)

        match f_type:
            case Shape.STRIP:
                sf = 1.0
            case Shape.RECTANGLE:
                sf = 1 + (f_w / f_l) * (n_q / n_c)
            case Shape.SQUARE | Shape.CIRCLE:
                sf = 1 + (n_q / n_c)
            case _:
                raise ValueError

        return sf

    @classmethod
    @round_
    def s_q(cls, f_angle: float, foundation_size: FoundationSize) -> float:
        f_w = foundation_size.effective_width
        f_l = foundation_size.length
        f_type = foundation_size.footing_shape

        if not isclose(f_w, f_l) and f_type != Shape.STRIP:
            f_type = Shape.RECTANGLE

        match f_type:
            case Shape.STRIP:
                sf = 1.0
            case Shape.RECTANGLE:
                sf = 1 + (f_w / f_l) * tan(f_angle)
            case Shape.SQUARE | Shape.CIRCLE:
                sf = 1 + tan(f_angle)
            case _:
                raise ValueError

        return sf

    @classmethod
    @round_
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
                sf = 1 - 0.4 * (f_w / f_l)
            case Shape.SQUARE | Shape.CIRCLE:
                sf = 0.6
            case _:
                raise ValueError

        return sf


class VesicDepthFactor:
    @classmethod
    @round_
    def d_c(cls, foundation_size: FoundationSize) -> float:
        return HansenDepthFactor.d_c(foundation_size)

    @classmethod
    @round_
    def d_q(cls, f_angle: float, foundation_size: FoundationSize) -> float:
        f_d = foundation_size.depth
        f_w = foundation_size.width
        return 1 + 2 * tan(f_angle) * (1 - sin(f_angle)) ** 2 * k(f_d, f_w)

    @classmethod
    @round_
    def d_gamma(cls) -> float:
        return 1.0


class VesicInclinationFactor:
    @classmethod
    @round_
    def i_c(cls, load_angle: float) -> float:
        return (1 - load_angle / 90) ** 2

    @classmethod
    @round_
    def i_q(cls, load_angle: float) -> float:
        return cls.i_c(load_angle=load_angle)

    @classmethod
    @round_
    def i_gamma(cls, f_angle: float, load_angle: float) -> float:
        return (
            1.0 if isclose(f_angle, 0.0) else (1 - load_angle / f_angle) ** 2
        )


class VesicUltimateBearingCapacity(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for footings on cohesionless soils according
    to ``Vesic 1973``.

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
        soil_properties: SoilProperties,
        foundation_size: FoundationSize,
        load_angle_incl: float = 0.0,
        water_level: float = INF,
        apply_local_shear: bool = False,
    ) -> None:
        super().__init__(
            soil_properties,
            foundation_size,
            water_level,
            apply_local_shear,
        )

        self.load_angle = load_angle_incl

        self.bearing_cpty_factor = VesicBearingCapacityFactor()
        self.shape_factor = VesicShapeFactor()
        self.depth_factor = VesicDepthFactor()
        self.incl_factor = VesicInclinationFactor()

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
        return self.shape_factor.s_c(self.friction_angle, self.foundation_size)

    @property
    def s_q(self) -> float:
        return self.shape_factor.s_q(self.friction_angle, self.foundation_size)

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
        return self.incl_factor.i_c(self.load_angle)

    @property
    def i_q(self) -> float:
        return self.incl_factor.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        return self.incl_factor.i_gamma(self.friction_angle, self.load_angle)

    @quantity(unit=UnitReg.kPa)
    @round_
    def bearing_capacity(self) -> float:
        """Ultimate bearing capacity of soil."""
        return (
            self._cohesion_term(1)
            + self._surcharge_term()
            + self._embedment_term(0.5)
        )
