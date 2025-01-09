from abc import ABC, abstractmethod

from geolysis.bearing_capacity import SoilProperties
from geolysis.foundation import FoundationSize
from geolysis.utils import INF, arctan, tan

__all__ = ["k", "UltimateBearingCapacity", "TerzaghiUBC4StripFooting",
           "TerzaghiUBC4CircFooting", "TerzaghiUBC4RectFooting",
           "TerzaghiUBC4SquareFooting", "HansenUltimateBearingCapacity",
           "VesicUltimateBearingCapacity"]


def k(f_d: float, f_w: float) -> float:
    return arctan(d2w) if (d2w := f_d / f_w) > 1 else d2w


class UltimateBearingCapacity(ABC):
    def __init__(self, soil_properties: SoilProperties,
                 foundation_size: FoundationSize, water_level: float = INF,
                 apply_local_shear: bool = False) -> None:
        self._friction_angle = soil_properties["friction_angle"]
        self._cohesion = soil_properties["cohesion"]
        self.moist_unit_wgt = soil_properties["moist_unit_wgt"]
        self.water_level = water_level
        self.foundation_size = foundation_size
        self.apply_local_shear = apply_local_shear

    def _cohesion_term(self, coef: float = 1.0) -> float:
        return coef * self.cohesion * self.n_c * self.s_c * self.d_c * self.i_c

    def _surcharge_term(self) -> float:
        f_d = self.foundation_size.depth

        if self.water_level == INF:
            water_corr = 1.0  #: water correction
        else:
            #: a -> water level above the base of the foundation
            a = max(f_d - self.water_level, 0.0)
            water_corr = min(1 - 0.5 * a / f_d, 1)

        # effective overburden pressure (surcharge)
        eop = self.moist_unit_wgt * f_d
        return eop * self.n_q * self.s_q * self.d_q * self.i_q * water_corr

    def _embedment_term(self, coef: float = 0.5) -> float:
        f_d = self.foundation_size.depth
        f_w = self.foundation_size.effective_width

        if self.water_level == INF:
            # water correction
            water_corr = 1.0
        else:
            #: b -> water level below the base of the foundation
            b = max(self.water_level - f_d, 0)
            water_corr = min(0.5 + 0.5 * b / f_w, 1)

        return (coef * self.moist_unit_wgt * f_w * self.n_gamma * self.s_gamma
                * self.d_gamma * self.i_gamma * water_corr)

    @property
    def friction_angle(self) -> float:
        """
        Return friction angle for ``local shear`` in the case of
        ``local shear failure`` and friction angle for ``general shear`` in
        the case of ``general shear failure``.
        """
        return (arctan((2 / 3) * tan(self._friction_angle))
                if self.apply_local_shear else self._friction_angle)

    @property
    def cohesion(self) -> float:
        """
        Return cohesion for local shear in the case of local shear failure and
        cohesion for general shear in the case of general shear failure.
        """
        return ((2 / 3) * self._cohesion
                if self.apply_local_shear else self._cohesion)

    @abstractmethod
    def bearing_capacity(self):
        ...

    @property
    @abstractmethod
    def n_c(self) -> float:
        ...

    @property
    @abstractmethod
    def n_q(self) -> float:
        ...

    @property
    @abstractmethod
    def n_gamma(self) -> float:
        ...

    @property
    @abstractmethod
    def s_c(self) -> float:
        ...

    @property
    @abstractmethod
    def s_q(self) -> float:
        ...

    @property
    @abstractmethod
    def s_gamma(self) -> float:
        ...

    @property
    @abstractmethod
    def d_c(self) -> float:
        ...

    @property
    @abstractmethod
    def d_q(self) -> float:
        ...

    @property
    @abstractmethod
    def d_gamma(self) -> float:
        ...

    @property
    @abstractmethod
    def i_c(self) -> float:
        ...

    @property
    @abstractmethod
    def i_q(self) -> float:
        ...

    @property
    @abstractmethod
    def i_gamma(self) -> float:
        ...


from .terzaghi_ubc import (TerzaghiUBC4StripFooting, TerzaghiUBC4CircFooting,
                           TerzaghiUBC4SquareFooting, TerzaghiUBC4RectFooting)
from .hansen_ubc import HansenUltimateBearingCapacity
from .vesic_ubc import VesicUltimateBearingCapacity
