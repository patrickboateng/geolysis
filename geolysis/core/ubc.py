from abc import ABC, abstractmethod
from typing import Protocol

from .constants import UNIT
from .foundation import FoundationSize
from .utils import (
    INF,
    PI,
    arctan,
    cos,
    cot,
    deg2rad,
    exp,
    isclose,
    round_,
    tan,
)

__all__ = [
    "TerzaghiUBC4StripFooting",
    "TerzaghiUBC4SquareFooting",
    "TerzaghiUBC4CircFooting",
    "TerzaghiUBC4RectFooting",
]

#: Unit for bearing capacity
kPa = UNIT.kPa


class _BearingCapacityFactors(Protocol):
    @classmethod
    @abstractmethod
    def n_c(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def n_q(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def n_gamma(cls, *args, **kwargs) -> float: ...


class _ShapeFactors(Protocol):
    @classmethod
    @abstractmethod
    def s_c(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def s_q(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def s_gamma(cls, *args, **kwargs) -> float: ...


class _DepthFactors(Protocol):
    @classmethod
    @abstractmethod
    def d_c(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def d_q(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def d_gamma(cls, *args, **kwargs) -> float: ...


class _InclinationFactors(Protocol):
    @classmethod
    @abstractmethod
    def i_c(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def i_q(cls, *args, **kwargs) -> float: ...

    @classmethod
    @abstractmethod
    def i_gamma(cls, *args, **kwargs) -> float: ...


class TerzaghiBCF(_BearingCapacityFactors):
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
    def n_gamma(cls, sfa) -> float:
        return (cls.n_q(sfa) - 1) * tan(1.4 * sfa)


class TerzaghiSF(_ShapeFactors):
    @classmethod
    def s_c(cls) -> float:
        return 1.0

    @classmethod
    def s_q(cls) -> float:
        return 1.0

    @classmethod
    def s_gamma(cls) -> float:
        return 1.0


class TerzaghiDF(_DepthFactors):
    @classmethod
    def d_c(cls) -> float:
        return 1.0

    @classmethod
    def d_q(cls) -> float:
        return 1.0

    @classmethod
    def d_gamma(cls) -> float:
        return 1.0


class TerzaghiIF(_InclinationFactors):
    @classmethod
    def i_c(cls) -> float:
        return 1.0

    @classmethod
    def i_q(cls) -> float:
        return 1.0

    @classmethod
    def i_gamma(cls) -> float:
        return 1.0


class AbstractUBC(ABC):
    # abstract ultimate bearing capacity class

    _unit = kPa

    def __init__(
        self,
        soil_friction_angle: float,
        cohesion: float,
        moist_unit_wgt: float,
        foundation_size: FoundationSize,
        water_level: float = INF,
        local_shear_failure: bool = False,
    ) -> None:
        self._f_angle = soil_friction_angle
        self._cohesion = cohesion

        self.moist_unit_wgt = moist_unit_wgt
        self.foundation_size = foundation_size

        #: local shear failure
        self._lsf = local_shear_failure

        # depth of water from the ground surface
        self.water_level = water_level

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
        return self.foundation_size.width

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
            #: a -> water level above the base of the foundation
            a = 0
            water_cor = 1  #: water correction
        else:
            a = max(self.f_depth - self.water_level, 0)
            water_cor = min(1 - 0.5 * a / self.f_depth, 1)

        # effective overburden pressure (surcharge)
        eop = self.moist_unit_wgt * self.f_depth

        return eop * self.n_q * self.s_q * self.d_q * self.i_q * water_cor

    @round_(ndigits=2)
    def _emb_expr(self) -> float:
        if self.water_level == INF:
            #: b -> water level below the base of the foundation
            b = 0
            water_cor = 1
        else:
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
        soil_friction_angle: float,
        cohesion: float,
        moist_unit_wgt: float,
        foundation_size: FoundationSize,
        water_level: float = INF,
        local_shear_failure: bool = False,
    ) -> None:
        super().__init__(
            soil_friction_angle,
            cohesion,
            moist_unit_wgt,
            foundation_size,
            water_level,
            local_shear_failure,
        )

        # bearing capacity factors
        self.bcf = TerzaghiBCF()

        # shape factors
        self.s_f = TerzaghiSF()

        # depth factors
        self.d_f = TerzaghiDF()

        # inclination factors
        self.i_f = TerzaghiIF()

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
        return self.s_f.s_c()

    @property
    def s_q(self) -> float:
        """Shape factor :math:`s_q`."""
        return self.s_f.s_q()

    @property
    def s_gamma(self) -> float:
        r"""Shape factor :math:`s_{\gamma}`."""
        return self.s_f.s_gamma()

    @property
    def d_c(self) -> float:
        """Depth factor :math:`d_c`."""
        return self.d_f.d_c()

    @property
    def d_q(self) -> float:
        """Depth factor :math:`d_q`."""
        return self.d_f.d_q()

    @property
    def d_gamma(self) -> float:
        r"""Depth factor :math:`d_{\gamma}`."""
        return self.d_f.d_gamma()

    @property
    def i_c(self) -> float:
        """Inclination factor :math:`i_c`."""
        return self.i_f.i_c()

    @property
    def i_q(self) -> float:
        """Inclination factor :math:`i_q`."""
        return self.i_f.i_q()

    @property
    def i_gamma(self) -> float:
        r"""Inclination factor :math:`i_{\gamma}`."""
        return self.i_f.i_gamma()

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


class HansenBCF(_BearingCapacityFactors):
    @classmethod
    @round_(ndigits=2)
    def n_c(cls, sfa: float) -> float:
        return 5.14 if isclose(sfa, 0.0) else cot(sfa) * (cls.n_q(sfa) - 1)

    @classmethod
    @round_(ndigits=2)
    def n_q(cls, sfa: float) -> float:
        return (tan(45 + sfa) ** 2) * (exp(PI * tan(sfa)))

    @classmethod
    @round_(ndigits=2)
    def n_gamma(cls, sfa) -> float:
        return 1.8 * (cls.n_q(sfa) - 1) * tan(sfa)
