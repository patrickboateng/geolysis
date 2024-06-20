from abc import ABC, abstractmethod
from typing import Protocol

from .constants import UNIT
from .foundation import FoundationSize
from .utils import (
    PI,
    arctan,
    cos,
    cot,
    deg2rad,
    exp,
    inf,
    isclose,
    round_,
    tan,
)

__all__ = ["TerzaghiUBC4StripFooting"]

#: Unit for bearing capacity
kPa = UNIT.kPa


class _BCF(Protocol):
    @property
    @abstractmethod
    def n_c(self) -> float: ...

    @property
    @abstractmethod
    def n_q(self) -> float: ...

    @property
    @abstractmethod
    def n_gamma(self) -> float: ...


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
    def n_gamma(cls, sfa) -> float:
        return (cls.n_q(sfa) - 1) * tan(1.4 * sfa)


class _AbstractTerzaghiUBC(ABC):
    _unit = kPa

    def __init__(
        self,
        soil_friction_angle: float,
        cohesion: float,
        moist_unit_wgt: float,
        foundation_size: FoundationSize,
        water_level: float = inf,
        local_shear_failure: bool = False,
    ) -> None:
        self._f_angle = soil_friction_angle
        self._cohesion = cohesion

        self.moist_unit_wgt = moist_unit_wgt
        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width
        self.f_length = foundation_size.length

        #: local shear failure
        self._lsf = local_shear_failure

        #: depth of water from the ground surface
        self.water_level = water_level

        #: bearing capacity factors
        self.bcf = TerzaghiBCF()

    @property
    def local_shear_failure(self) -> bool:
        return self._lsf

    @local_shear_failure.setter
    def local_shear_failure(self, __val: bool):
        self._lsf = __val

    @property
    @round_(ndigits=2)
    def sfa(self) -> float:
        return (
            arctan((2 / 3) * tan(self._f_angle))
            if self._lsf
            else self._f_angle
        )

    @sfa.setter
    def sfa(self, __val: float):
        self._f_angle = __val

    @property
    @round_(ndigits=2)
    def cohesion(self) -> float:
        return (2 / 3) * self._cohesion if self._lsf else self._cohesion

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def n_c(self) -> float:
        return self.bcf.n_c(self.sfa)

    @property
    def n_q(self) -> float:
        return self.bcf.n_q(self.sfa)

    @property
    def n_gamma(self) -> float:
        return self.bcf.n_gamma(self.sfa)

    def _cohesion_t(self) -> float:
        return self.cohesion * self.n_c

    def _surcharge_t(self) -> float:
        if self.water_level == inf:
            #: a -> water level above the base of the foundation
            a = 0
            water_correction = 1
        else:
            a = max(self.f_depth - self.water_level, 0)
            water_correction = min(1 - 0.5 * a / self.f_depth, 1)

        return self.moist_unit_wgt * self.f_depth * self.n_q * water_correction

    def _embedment_t(self) -> float:
        if self.water_level == inf:
            #: b -> water level below the base of the foundation
            b = 0
            water_correction = 1
        else:
            b = max(self.water_level - self.f_depth, 0)
            water_correction = min(0.5 + 0.5 * b / self.f_width, 1)

        return (
            self.moist_unit_wgt
            * self.f_width
            * self.n_gamma
            * water_correction
        )

    @abstractmethod
    def bearing_capacity(self) -> float: ...


class TerzaghiUBC4StripFooting(_AbstractTerzaghiUBC):
    @round_
    def bearing_capacity(self) -> float:
        return (
            self._cohesion_t()
            + self._surcharge_t()
            + 0.5 * self._embedment_t()
        )


class TerzaghiUBC4SquareFooting(_AbstractTerzaghiUBC):
    @round_
    def bearing_capacity(self) -> float:
        return (
            1.3 * self._cohesion_t()
            + self._surcharge_t()
            + 0.4 * self._embedment_t()
        )


class TerzaghiUBC4CircFooting(_AbstractTerzaghiUBC):
    @round_
    def bearing_capacity(self) -> float:
        return (
            1.3 * self._cohesion_t()
            + self._surcharge_t()
            + 0.3 * self._embedment_t()
        )


class TerzaghiUBC4RectFooting(_AbstractTerzaghiUBC):
    @round_
    def bearing_capacity(self) -> float:
        return (
            (1 + 0.3 * (self.f_width / self.f_length)) * self._cohesion_t()
            + self._surcharge_t()
            + (1 - 0.2 * (self.f_width / self.f_length))
            * 0.5
            * self._embedment_t()
        )
