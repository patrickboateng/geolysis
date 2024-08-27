from geolysis.core.bearing_capacity.ubc_4_soils import (
    UltimateBearingCapacity,
    _get_footing_info,
    d2w,
)
from geolysis.core.bearing_capacity.ubc_4_soils.hansen_ubc import (
    HansenBearingCapacityFactor,
    HansenDepthFactor,
)
from geolysis.core.foundation import FoundationSize, Shape
from geolysis.core.utils import (
    INF,
    isclose,
    round_,
    sin,
    tan,
)


class VesicBearingCapacityFactor:
    @classmethod
    @round_
    def n_c(cls, sfa: float) -> float:
        return HansenBearingCapacityFactor.n_c(sfa)

    @classmethod
    @round_
    def n_q(cls, sfa: float) -> float:
        return HansenBearingCapacityFactor.n_q(sfa)

    @classmethod
    @round_
    def n_gamma(cls, sfa: float) -> float:
        return 2 * (cls.n_q(sfa) + 1) * tan(sfa)


class VesicShapeFactor:
    @classmethod
    @round_
    def s_c(
        cls,
        sfa: float,
        f_w: float,
        f_l: float,
        footing_type: Shape,
    ) -> float:
        n_q = VesicBearingCapacityFactor.n_q(sfa=sfa)
        n_c = VesicBearingCapacityFactor.n_c(sfa=sfa)

        match footing_type:
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
    def s_q(cls, sfa: float, f_w, f_l, footing_type: Shape) -> float:
        match footing_type:
            case Shape.STRIP:
                sf = 1.0
            case Shape.RECTANGLE:
                sf = 1 + (f_w / f_l) * tan(sfa)
            case Shape.SQUARE | Shape.CIRCLE:
                sf = 1 + tan(sfa)
            case _:
                raise ValueError

        return sf

    @classmethod
    @round_
    def s_gamma(cls, f_w, f_l, footing_type: Shape) -> float:
        match footing_type:
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
    def d_c(cls, f_d: float, f_w: float) -> float:
        return HansenDepthFactor.d_c(f_d, f_w)

    @classmethod
    @round_
    def d_q(cls, sfa: float, f_d: float, f_w: float) -> float:
        k = d2w(f_d, f_w)
        return 1 + 2 * tan(sfa) * (1 - sin(sfa)) ** 2 * k

    @classmethod
    @round_
    def d_gamma(cls) -> float:
        return 1.0


class VesicInclinationFactor:
    @classmethod
    def i_c(cls, load_angle: float) -> float:
        return (1 - load_angle / 90) ** 2

    @classmethod
    def i_q(cls, load_angle: float) -> float:
        return cls.i_c(load_angle=load_angle)

    @classmethod
    def i_gamma(cls, sfa: float, load_angle: float) -> float:
        return 1.0 if isclose(sfa, 0.0) else (1 - load_angle / sfa) ** 2


class VesicUBC(UltimateBearingCapacity):
    r"""Ultimate bearing capacity for footings on cohesionless soils
    according to ``Vesic 1973``.

    Parameters
    ----------
    soil_friction_angle : float
        Internal angle of friction of soil material.
    cohesion : float
        Cohesion of soil material.
    moist_unit_wgt : float
        Moist (Bulk) unit weight of soil material.
    foundation_size : FoundationSize
        Size of foundation.
    water_level : float
        Depth of water below the ground surface.
    local_shear_failure : float
        Indicates if local shear failure is likely to occur therefore
        modifies the soil_friction_angle and cohesion of the soil
        material.
    e : float
        Deviation of the applied load from the center of the footing
        also know as eccentricity.

    Attributes
    ----------
    n_c
    n_q
    n_gamma

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
        soil_properties: dict,
        foundation_size: FoundationSize,
        water_level: float = INF,
        local_shear_failure: bool = False,
        load_angle_incl: float = 0.0,
        e: float = 0,
    ) -> None:
        super().__init__(
            soil_properties,
            foundation_size,
            water_level,
            local_shear_failure,
            e,
        )

        self.load_angle = load_angle_incl

        # bearing capacity factors
        self.bcf = VesicBearingCapacityFactor()

        # shape factors
        self.shape_factor = VesicShapeFactor()

        # depth factors
        self.depth_factor = VesicDepthFactor()

        # inclination factors
        self.incl_factor = VesicInclinationFactor()

    @property
    def n_c(self) -> float:
        return self.bcf.n_c(self.sfa)

    @property
    def n_q(self) -> float:
        return self.bcf.n_q(self.sfa)

    @property
    def n_gamma(self) -> float:
        return self.bcf.n_gamma(self.sfa)

    @property
    def s_c(self) -> float:
        B, L, f_type = _get_footing_info(self)
        return self.shape_factor.s_c(self.sfa, B, L, f_type)

    @property
    def s_q(self) -> float:
        B, L, f_type = _get_footing_info(self)
        return self.shape_factor.s_q(self.sfa, B, L, f_type)

    @property
    def s_gamma(self) -> float:
        B, L, f_type = _get_footing_info(self)
        return self.shape_factor.s_gamma(B, L, f_type)

    @property
    def d_c(self) -> float:
        return self.depth_factor.d_c(self.foundation_size)

    @property
    def d_q(self) -> float:
        return self.depth_factor.d_q(self.sfa, self.foundation_size)

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
        return self.incl_factor.i_gamma(self.sfa, self.load_angle)

    @round_
    def bearing_capacity(self) -> float:
        """Ultimate bearing capacity of soil."""
        _emb_t = 0.5 * self._emb_expr()
        return self._coh_expr() + self._surcharge_expr() + _emb_t
