from abc import abstractmethod

from geolysis.core.bearing_capacity.ubc_4_soils import UltimateBearingCapacity
from geolysis.core.foundation import FoundationSize
from geolysis.core.utils import (
    INF,
    PI,
    cos,
    cot,
    deg2rad,
    exp,
    isclose,
    round_,
    tan,
)


class TerzaghiBearingCapacityFactor:
    @classmethod
    @round_
    def n_c(cls, sfa: float) -> float:
        return 5.7 if isclose(sfa, 0.0) else cot(sfa) * (cls.n_q(sfa) - 1)

    @classmethod
    @round_
    def n_q(cls, sfa: float) -> float:
        return exp((3 * PI / 2 - deg2rad(sfa)) * tan(sfa)) / (
            2 * (cos(45 + sfa / 2)) ** 2
        )

    @classmethod
    @round_
    def n_gamma(cls, sfa: float) -> float:
        return (cls.n_q(sfa) - 1) * tan(1.4 * sfa)


class TerzaghiShapeFactor:
    @classmethod
    def s_c(cls) -> float:
        return 1.0

    @classmethod
    def s_q(cls) -> float:
        return 1.0

    @classmethod
    def s_gamma(cls) -> float:
        return 1.0


class TerzaghiDepthFactor:
    @classmethod
    def d_c(cls) -> float:
        return 1.0

    @classmethod
    def d_q(cls) -> float:
        return 1.0

    @classmethod
    def d_gamma(cls) -> float:
        return 1.0


class TerzaghiInclinationFactor:
    @classmethod
    def i_c(cls) -> float:
        return 1.0

    @classmethod
    def i_q(cls) -> float:
        return 1.0

    @classmethod
    def i_gamma(cls) -> float:
        return 1.0


class TerzaghiUltimateBearingCapacity(UltimateBearingCapacity):
    def __init__(
        self,
        soil_properties: dict,
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
            e,
        )

        # bearing capacity factors
        self.bcf = TerzaghiBearingCapacityFactor()

        # shape factors
        self.shape_factor = TerzaghiShapeFactor()

        # depth factors
        self.depth_factor = TerzaghiDepthFactor()

        # inclination factors
        self.incl_factor = TerzaghiInclinationFactor()

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


class TerzaghiUBC4StripFooting(TerzaghiUltimateBearingCapacity):
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


class TerzaghiUBC4SquareFooting(TerzaghiUltimateBearingCapacity):
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


class TerzaghiUBC4CircFooting(TerzaghiUltimateBearingCapacity):
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

    .. math:: q_u = 1.3cN_c + qN_q + 0.3 \gamma BN_{\gamma}

    Examples
    --------

    """

    @round_
    def bearing_capacity(self) -> float:
        _coh_t = 1.3 * self._coh_expr()
        _emb_t = 0.3 * self._emb_expr()
        return _coh_t + self._surcharge_expr() + _emb_t


class TerzaghiUBC4RectFooting(TerzaghiUltimateBearingCapacity):
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
