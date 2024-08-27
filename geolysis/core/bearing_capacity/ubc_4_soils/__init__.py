from abc import ABC, abstractmethod

from geolysis.core.foundation import FoundationSize, Shape
from geolysis.core.utils import INF, arctan, isclose, round_, tan


def _get_footing_info(obj):
    B = obj.f_width
    L = obj.f_length
    f_type = obj.foundation_size.footing_type

    if not isclose(B, L) and f_type != Shape.STRIP:
        f_type = Shape.RECTANGLE

    return (B, L, f_type)


# depth to width ratio
def d2w(d: float, w: float) -> float:
    ratio = d / w

    if ratio > 1:
        ratio = arctan(ratio)

    return ratio


class UltimateBearingCapacity(ABC):
    # abstract ultimate bearing capacity class

    def __init__(
        self,
        soil_properties: dict,
        foundation_size: FoundationSize,
        water_level: float = INF,
        local_shear_failure: bool = False,
        e: float = 0.0,
    ) -> None:
        self._f_angle = soil_properties["soil_friction_angle"]
        self._cohesion = soil_properties["cohesion"]

        self.moist_unit_wgt = soil_properties["moist_unit_wgt"]

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

    @property
    def f_width(self) -> float:
        """Width of foundation footing."""
        effective_width = self.foundation_size.width - 2 * self.e
        return effective_width

    @property
    def f_length(self) -> float:
        """Length of foundation footing."""
        return self.foundation_size.length

    @round_
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
    @round_
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
    @round_
    def cohesion(self) -> float:
        """Cohesion of soil material.

        If ``local_shear_failure`` is false, ``cohesion`` is for general
        shear failure otherwise ``cohesion`` is for local shear failure.
        """
        return (2 / 3) * self._cohesion if self._lsf else self._cohesion

    @round_
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

    @round_
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
