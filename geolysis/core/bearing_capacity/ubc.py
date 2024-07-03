from abc import ABC, abstractmethod

from ..constants import UNIT, SoilProperties
from ..foundation import (
    FoundationSize,
    Shape,
    _FootingShape,
)
from ..utils import (
    INF,
    PI,
    arctan,
    cos,
    cot,
    deg2rad,
    exp,
    isclose,
    round_,
    sin,
    tan,
)

__all__ = [
    "TerzaghiUBC4StripFooting",
    "TerzaghiUBC4SquareFooting",
    "TerzaghiUBC4CircFooting",
    "TerzaghiUBC4RectFooting",
    "HansenUBC",
    "VesicUBC",
]

#: Unit for bearing capacity
kPa = UNIT.kPa


def _get_footing_info(obj) -> tuple:
    B = obj.f_width
    L = obj.f_length
    f_type = obj.foundation_size.footing_type

    if not isclose(B, L) and f_type != Shape.STRIP:
        f_type = Shape.RECTANGLE

    return (B, L, f_type)


# depth to width ratio
def d2w_r(d: float, w: float) -> float:
    ratio = d / w

    if ratio > 1:
        ratio = arctan(ratio)

    return ratio


class TerzaghiBCF:
    @classmethod
    @round_(ndigits=2)
    def n_c(cls, sfa: float) -> float:
        return 5.7 if isclose(sfa, 0.0) else cot(sfa) * (cls.n_q(sfa) - 1)

    @classmethod
    @round_(ndigits=2)
    def n_q(cls, sfa: float) -> float:
        return exp((3 * PI / 2 - deg2rad(sfa)) * tan(sfa)) / (
            2 * (cos(45 + sfa / 2)) ** 2
        )

    @classmethod
    @round_(ndigits=2)
    def n_gamma(cls, sfa: float) -> float:
        return (cls.n_q(sfa) - 1) * tan(1.4 * sfa)


class TerzaghiShapeFactors:
    @staticmethod
    def s_c() -> float:
        return 1.0

    @staticmethod
    def s_q() -> float:
        return 1.0

    @staticmethod
    def s_gamma() -> float:
        return 1.0


class TerzaghiDepthFactors:
    @staticmethod
    def d_c() -> float:
        return 1.0

    @staticmethod
    def d_q() -> float:
        return 1.0

    @staticmethod
    def d_gamma() -> float:
        return 1.0


class TerzaghiInclFactors:
    @staticmethod
    def i_c() -> float:
        return 1.0

    @staticmethod
    def i_q() -> float:
        return 1.0

    @staticmethod
    def i_gamma() -> float:
        return 1.0


class HansenBCF:
    @classmethod
    @round_(ndigits=2)
    def n_c(cls, sfa: float) -> float:
        return 5.14 if isclose(sfa, 0.0) else cot(sfa) * (cls.n_q(sfa) - 1)

    @classmethod
    @round_(ndigits=2)
    def n_q(cls, sfa: float) -> float:
        return (tan(45 + sfa / 2)) ** 2 * (exp(PI * tan(sfa)))

    @classmethod
    @round_(ndigits=2)
    def n_gamma(cls, sfa) -> float:
        return 1.8 * (cls.n_q(sfa) - 1) * tan(sfa)


class HansenShapeFactors:
    @classmethod
    @round_(ndigits=2)
    def s_c(cls, f_w, f_l, footing_type: Shape) -> float:
        match footing_type:
            case Shape.STRIP:
                f = 10
            case Shape.RECTANGLE:
                f = 1 + 0.2 * f_w / f_l
            case Shape.SQUARE | Shape.CIRCLE:
                f = 1.3
            case _:
                raise ValueError

        return f

    @classmethod
    @round_(ndigits=2)
    def s_q(cls, f_w, f_l, footing_type: Shape) -> float:
        match footing_type:
            case Shape.STRIP:
                f = 1.0
            case Shape.RECTANGLE:
                f = 1 + 0.2 * f_w / f_l
            case Shape.SQUARE | Shape.CIRCLE:
                f = 1.2
            case _:
                raise ValueError

        return f

    @classmethod
    @round_(ndigits=2)
    def s_gamma(cls, f_w, f_l, footing_type: Shape) -> float:
        match footing_type:
            case Shape.STRIP:
                f = 1.0
            case Shape.RECTANGLE:
                f = 1 - 0.4 * f_w / f_l
            case Shape.SQUARE:
                f = 0.8
            case Shape.CIRCLE:
                f = 0.6
            case _:
                raise ValueError

        return f


class HansenDepthFactors:
    @classmethod
    @round_(ndigits=2)
    def d_c(cls, foundation_size: FoundationSize) -> float:
        Df = foundation_size.depth
        B = foundation_size.width
        k = d2w_r(Df, B)
        return 1 + 0.4 * k

    @classmethod
    @round_(ndigits=2)
    def d_q(cls, sfa: float, foundation_size: FoundationSize) -> float:
        if sfa > 25.0:
            return cls.d_c(foundation_size)
        else:
            Df = foundation_size.depth
            B = foundation_size.width
            k = d2w_r(Df, B)
            return 1 + 2 * tan(sfa) * (1 - sin(sfa)) ** 2 * k

    @staticmethod
    @round_(ndigits=2)
    def d_gamma() -> float:
        return 1.0


class HansenInclFactors:
    @classmethod
    @round_(ndigits=2)
    def i_c(
        cls,
        cohesion: float,
        load_angle: float,
        footing_shape: _FootingShape,
    ) -> float:
        H = cos(load_angle)
        B = footing_shape.width
        L = footing_shape.length
        return 1 - H / (2 * cohesion * B * L)

    @classmethod
    def i_q(cls, load_angle: float) -> float:
        H = cos(load_angle)
        V = sin(load_angle)
        return 1 - (1.5 * H) / V

    @classmethod
    def i_gamma(cls, load_angle: float) -> float:
        return cls.i_q(load_angle) ** 2


class VesicBCF:
    @classmethod
    @round_(ndigits=2)
    def n_c(cls, sfa: float) -> float:
        return HansenBCF.n_c(sfa)

    @classmethod
    @round_(ndigits=2)
    def n_q(cls, sfa: float) -> float:
        return HansenBCF.n_q(sfa)

    @classmethod
    @round_(ndigits=2)
    def n_gamma(cls, sfa: float) -> float:
        return 2 * (cls.n_q(sfa) + 1) * tan(sfa)


class VesicShapeFactors:
    @classmethod
    @round_(ndigits=2)
    def s_c(cls, sfa: float, f_w, f_l, footing_type: Shape) -> float:
        n_q = VesicBCF.n_q(sfa=sfa)
        n_c = VesicBCF.n_c(sfa=sfa)

        match footing_type:
            case Shape.STRIP:
                f = 1.0
            case Shape.RECTANGLE:
                f = 1 + (f_w / f_l) * (n_q / n_c)
            case Shape.SQUARE | Shape.CIRCLE:
                f = 1 + (n_q / n_c)
            case _:
                raise ValueError

        return f

    @classmethod
    @round_(ndigits=2)
    def s_q(cls, sfa: float, f_w, f_l, footing_type: Shape) -> float:
        match footing_type:
            case Shape.STRIP:
                f = 1.0
            case Shape.RECTANGLE:
                f = 1 + (f_w / f_l) * tan(sfa)
            case Shape.SQUARE | Shape.CIRCLE:
                f = 1 + tan(sfa)
            case _:
                raise ValueError

        return f

    @classmethod
    @round_(ndigits=2)
    def s_gamma(cls, f_w, f_l, footing_type: Shape) -> float:
        match footing_type:
            case Shape.STRIP:
                f = 1.0
            case Shape.RECTANGLE:
                f = 1 - 0.4 * (f_w / f_l)
            case Shape.SQUARE | Shape.CIRCLE:
                f = 0.6
            case _:
                raise ValueError

        return f


class VesicDepthFactors:
    @classmethod
    @round_(ndigits=2)
    def d_c(cls, foundation_size: FoundationSize) -> float:
        return HansenDepthFactors.d_c(foundation_size)

    @classmethod
    @round_(ndigits=2)
    def d_q(cls, sfa: float, foundation_size: FoundationSize) -> float:
        Df = foundation_size.depth
        B = foundation_size.width
        k = d2w_r(Df, B)
        return 1 + 2 * tan(sfa) * (1 - sin(sfa)) ** 2 * k

    @staticmethod
    @round_(ndigits=2)
    def d_gamma() -> float:
        return 1.0


class VesicInclFactors:
    @classmethod
    def i_c(cls, load_angle: float) -> float:
        return (1 - load_angle / 90) ** 2

    @classmethod
    def i_q(cls, load_angle: float) -> float:
        return cls.i_c(load_angle=load_angle)

    @classmethod
    def i_gamma(cls, sfa: float, load_angle: float) -> float:
        return 1.0 if isclose(sfa, 0.0) else (1 - load_angle / sfa) ** 2


class AbstractUBC(ABC):
    # abstract ultimate bearing capacity class

    _unit = kPa

    def __init__(
        self,
        soil_properties: SoilProperties,
        foundation_size: FoundationSize,
        water_level: float = INF,
        local_shear_failure: bool = False,
        e: float = 0.0,
    ) -> None:
        self._f_angle = getattr(soil_properties, "soil_friction_angle")
        self._cohesion = getattr(soil_properties, "cohesion")

        self.moist_unit_wgt = getattr(soil_properties, "moist_unit_wgt")

        self.foundation_size = foundation_size

        #: local shear failure
        self._lsf = local_shear_failure

        # depth of water from the ground surface
        self.water_level = water_level

        # eccentricity
        self.e = e

    @property
    def f_depth(self) -> float:
        """Depth of foundation footing."""
        return self.foundation_size.depth

    @f_depth.setter
    def f_depth(self, __val: float):
        self.foundation_size.depth = __val

    @property
    def f_width(self) -> float:
        """Width of foundation footing."""
        effective_width = self.foundation_size.width - 2 * self.e
        return effective_width

    @f_width.setter
    def f_width(self, __val: float):
        self.foundation_size.width = __val

    @property
    def f_length(self) -> float:
        """Length of foundation footing."""
        return self.foundation_size.length

    @f_length.setter
    def f_length(self, __val: float):
        self.foundation_size.length = __val

    @round_(ndigits=2)
    def _coh_expr(self) -> float:
        return self.cohesion * self.n_c * self.s_c * self.d_c * self.i_c

    @property
    def local_shear_failure(self) -> bool:
        return self._lsf

    @local_shear_failure.setter
    def local_shear_failure(self, __val: bool):
        self._lsf = __val

    @property
    def soil_friction_angle(self) -> float:
        return self._f_angle

    @soil_friction_angle.setter
    def soil_friction_angle(self, __val: float):
        self._f_angle = __val

    @property
    @round_(ndigits=2)
    def sfa(self) -> float:
        """Soil friction angle for either general or local shear failure.

        If ``local_shear_failure`` is false, ``sfa`` is the soil friction
        angle for general shear failure otherwise ``sfa`` is the soil
        friction angle for local shear failure.
        """

        if self._lsf:
            _sfa = arctan((2 / 3) * tan(self._f_angle))
        else:
            _sfa = self._f_angle
        return _sfa

    @property
    @round_(ndigits=2)
    def cohesion(self) -> float:
        """Cohesion of soil material.

        If ``local_shear_failure`` is false, ``cohesion`` is for general
        shear failure otherwise ``cohesion`` is for local shear failure.
        """
        return (2 / 3) * self._cohesion if self._lsf else self._cohesion

    @property
    def unit(self) -> str:
        """Unit for bearing capacity of soil."""
        return self._unit

    @round_(ndigits=2)
    def _surcharge_expr(self) -> float:
        if self.water_level == INF:
            water_cor = 1.0  #: water correction
        else:
            #: a -> water level above the base of the foundation
            a = max(self.f_depth - self.water_level, 0.0)
            water_cor = min(1 - 0.5 * a / self.f_depth, 1)

        # effective overburden pressure (surcharge)
        eop = self.moist_unit_wgt * self.f_depth

        return eop * self.n_q * self.s_q * self.d_q * self.i_q * water_cor

    @round_(ndigits=2)
    def _emb_expr(self) -> float:
        if self.water_level == INF:
            # water correction
            water_cor = 1.0
        else:
            #: b -> water level below the base of the foundation
            b = max(self.water_level - self.f_depth, 0)
            water_cor = min(0.5 + 0.5 * b / self.f_width, 1)

        return (
            self.moist_unit_wgt
            * self.f_width
            * self.n_gamma
            * self.s_gamma
            * self.d_gamma
            * self.i_gamma
            * water_cor
        )

    @abstractmethod
    def bearing_capacity(self) -> float: ...

    @property
    @abstractmethod
    def n_c(self) -> float: ...

    @property
    @abstractmethod
    def n_q(self) -> float: ...

    @property
    @abstractmethod
    def n_gamma(self) -> float: ...

    @property
    @abstractmethod
    def s_c(self) -> float: ...

    @property
    @abstractmethod
    def s_q(self) -> float: ...

    @property
    @abstractmethod
    def s_gamma(self) -> float: ...

    @property
    @abstractmethod
    def d_c(self) -> float: ...

    @property
    @abstractmethod
    def d_q(self) -> float: ...

    @property
    @abstractmethod
    def d_gamma(self) -> float: ...

    @property
    @abstractmethod
    def i_c(self) -> float: ...

    @property
    @abstractmethod
    def i_q(self) -> float: ...

    @property
    @abstractmethod
    def i_gamma(self) -> float: ...


class _TerzaghiUBC(AbstractUBC):
    def __init__(
        self,
        soil_properties: SoilProperties,
        foundation_size: FoundationSize,
        water_level: float = INF,
        local_shear_failure: bool = False,
        e: float = 0,
    ) -> None:
        super().__init__(
            soil_properties,
            foundation_size,
            water_level,
            local_shear_failure,
        )

        # bearing capacity factors
        self.bcf = TerzaghiBCF()

        # shape factors
        self.shape_factor = TerzaghiShapeFactors()

        # depth factors
        self.depth_factor = TerzaghiDepthFactors()

        # inclination factors
        self.incl_factor = TerzaghiInclFactors()

    @property
    def n_c(self) -> float:
        r"""Bearing capacity factor :math:`N_c`.

        .. math:: N_c = \cot \phi (N_q - 1)
        """
        return self.bcf.n_c(self.sfa)

    @property
    def n_q(self) -> float:
        r"""Bearing capacity factor :math:`N_q`.

        .. math::

            N_q = \dfrac{e^{(\frac{3\pi}{2} - \phi)\tan\phi}}
                  {2\cos^2(45 + \frac{\phi}{2})}
        """
        return self.bcf.n_q(self.sfa)

    @property
    def n_gamma(self) -> float:
        r"""Bearing capacity factor :math:`N_{\gamma}`.

        .. math:: N_{\gamma} =  (N_q - 1) \tan(1.4\phi)
        """
        return self.bcf.n_gamma(self.sfa)

    @property
    def s_c(self) -> float:
        """Shape factor :math:`s_c`."""
        return self.shape_factor.s_c()

    @property
    def s_q(self) -> float:
        """Shape factor :math:`s_q`."""
        return self.shape_factor.s_q()

    @property
    def s_gamma(self) -> float:
        r"""Shape factor :math:`s_{\gamma}`."""
        return self.shape_factor.s_gamma()

    @property
    def d_c(self) -> float:
        """Depth factor :math:`d_c`."""
        return self.depth_factor.d_c()

    @property
    def d_q(self) -> float:
        """Depth factor :math:`d_q`."""
        return self.depth_factor.d_q()

    @property
    def d_gamma(self) -> float:
        r"""Depth factor :math:`d_{\gamma}`."""
        return self.depth_factor.d_gamma()

    @property
    def i_c(self) -> float:
        """Inclination factor :math:`i_c`."""
        return self.incl_factor.i_c()

    @property
    def i_q(self) -> float:
        """Inclination factor :math:`i_q`."""
        return self.incl_factor.i_q()

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor :math:`i_{\gamma}`."""
        return self.incl_factor.i_gamma()

    @abstractmethod
    def bearing_capacity(self) -> float: ...


class TerzaghiUBC4StripFooting(_TerzaghiUBC):
    r"""Ultimate bearing capacity for strip footing on cohesionless
    soils according to ``Terzaghi 1943``.

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

    Attributes
    ----------
    f_depth
    f_width
    f_length
    cohesion
    sfa
    unit
    n_c
    n_q
    n_gamma
    s_c
    s_q
    s_gamma
    d_c
    d_q
    d_gamma
    i_c
    i_q
    i_gamma

    Notes
    -----
    Ultimate bearing capacity for strip footing is given by the formula:

    .. math:: q_u = cN_c + qN_q + 0.5 \gamma BN_{\gamma}

    Examples
    --------

    """

    @round_
    def bearing_capacity(self) -> float:
        """Ultimate bearing capacity of soil."""
        _emb_t = 0.5 * self._emb_expr()
        return self._coh_expr() + self._surcharge_expr() + _emb_t


class TerzaghiUBC4SquareFooting(_TerzaghiUBC):
    r"""Ultimate bearing capacity for square footing on cohesionless
    soils according to ``Terzaghi 1943``.

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

    Attributes
    ----------
    f_depth
    f_width
    f_length
    cohesion
    sfa
    unit
    n_c
    n_q
    n_gamma
    s_c
    s_q
    s_gamma
    d_c
    d_q
    d_gamma
    i_c
    i_q
    i_gamma

    Notes
    -----
    Ultimate bearing capacity for square footing is given by the formula:

    .. math:: q_u = 1.3cN_c + qN_q + 0.4 \gamma BN_{\gamma}

    Examples
    --------

    """

    @round_
    def bearing_capacity(self) -> float:
        _coh_t = 1.3 * self._coh_expr()
        _emb_t = 0.4 * self._emb_expr()
        return _coh_t + self._surcharge_expr() + _emb_t


class TerzaghiUBC4CircFooting(_TerzaghiUBC):
    r"""Ultimate bearing capacity for circular footing on cohesionless
    soils according to ``Terzaghi 1943``.

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

    Attributes
    ----------
    f_depth
    f_width
    f_length
    cohesion
    sfa
    unit
    n_c
    n_q
    n_gamma
    s_c
    s_q
    s_gamma
    d_c
    d_q
    d_gamma
    i_c
    i_q
    i_gamma

    Notes
    -----
    Ultimate bearing capacity for circular footing is given by the formula:

    .. math:: q_u = 1.3cN_c + qN_q + 0.3 \gamma BN_{\gamma}

    Examples
    --------

    """

    @round_
    def bearing_capacity(self) -> float:
        _coh_t = 1.3 * self._coh_expr()
        _emb_t = 0.3 * self._emb_expr()
        return _coh_t + self._surcharge_expr() + _emb_t


class TerzaghiUBC4RectFooting(_TerzaghiUBC):
    r"""Ultimate bearing capacity for rectangular footing on cohesionless
    soils according to ``Terzaghi 1943``.

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

    Attributes
    ----------
    f_depth
    f_width
    f_length
    cohesion
    sfa
    unit
    n_c
    n_q
    n_gamma
    s_c
    s_q
    s_gamma
    d_c
    d_q
    d_gamma
    i_c
    i_q
    i_gamma

    Notes
    -----
    Ultimate bearing capacity for rectangular footing is given by the formula:

    .. math::

        q_u = \left(1 + 0.3 \dfrac{B}{L} \right) c N_c
              + qN_q
              + \left(1 - 0.2 \dfrac{B}{L} \right) 0.5 B \gamma N_{\gamma}

    Examples
    --------

    """

    @round_
    def bearing_capacity(self) -> float:
        _coh_t = (1 + 0.3 * (self.f_width / self.f_length)) * self._coh_expr()
        _emb_t = (
            (1 - 0.2 * (self.f_width / self.f_length)) * 0.5 * self._emb_expr()
        )
        return _coh_t + self._surcharge_expr() + _emb_t


class HansenUBC(AbstractUBC):
    def __init__(
        self,
        soil_properties: SoilProperties,
        foundation_size: FoundationSize,
        water_level: float = INF,
        local_shear_failure: bool = False,
        load_angle_incl: float = 90,
        e: float = 0.0,
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
        self.bcf = HansenBCF()

        # shape factors
        self.shape_factor = HansenShapeFactors()

        # depth factors
        self.depth_factor = HansenDepthFactors()

        # inclination factors
        self.incl_factor = HansenInclFactors()

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
        return self.shape_factor.s_c(B, L, f_type)

    @property
    def s_q(self) -> float:
        B, L, f_type = _get_footing_info(self)
        return self.shape_factor.s_q(B, L, f_type)

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
        return self.incl_factor.i_c(
            self.cohesion,
            self.load_angle,
            self.foundation_size.footing_shape,
        )

    @property
    def i_q(self) -> float:
        return self.incl_factor.i_q(self.load_angle)

    @property
    def i_gamma(self) -> float:
        return self.incl_factor.i_gamma(self.load_angle)

    @round_
    def bearing_capacity(self) -> float:
        """Ultimate bearing capacity of soil."""
        _emb_t = 0.5 * self._emb_expr()
        return self._coh_expr() + self._surcharge_expr() + _emb_t


class VesicUBC(AbstractUBC):
    def __init__(
        self,
        soil_properties: SoilProperties,
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
        self.bcf = VesicBCF()

        # shape factors
        self.shape_factor = VesicShapeFactors()

        # depth factors
        self.depth_factor = VesicDepthFactors()

        # inclination factors
        self.incl_factor = VesicInclFactors()

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
