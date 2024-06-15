from abc import ABC, abstractmethod
from typing import Protocol

from .constants import UNIT
from .foundation import FoundationSize
from .utils import PI, arctan, cos, cot, deg2rad, exp, isclose, round_, tan

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

    def __init__(self, soil_friction_angle: float) -> None:
        self._f_angle = soil_friction_angle

    @property
    @round_(ndigits=2)
    def n_c(self) -> float:
        return (
            5.7
            if isclose(self._f_angle, 0.0)
            else cot(self._f_angle) * (self.n_q - 1)
        )

    @property
    @round_(ndigits=2)
    def n_q(self) -> float:
        num_expr = exp(
            (3 * PI / 2 - deg2rad(self._f_angle)) * tan(self._f_angle)
        )
        den_expr = 2 * (cos(45 + self._f_angle / 2)) ** 2
        return num_expr / den_expr

    @property
    @round_(ndigits=2)
    def n_gamma(self) -> float:
        return (self.n_q - 1) * tan(1.4 * self._f_angle)


_local_f_angle = lambda f_angle: round(arctan((2 / 3) * tan(f_angle)), 2)
_local_cohesion = lambda cohesion: round((2 / 3) * cohesion, 2)


class _AbstractTerzaghiUBC(ABC):

    _unit = kPa

    def __init__(
        self,
        soil_friction_angle: float,
        cohesion: float,
        unit_wgt: float,
        foundation_size: FoundationSize,
        local_shear_failure: bool = False,
    ) -> None:

        self._f_angle = (
            _local_f_angle(soil_friction_angle)
            if local_shear_failure
            else soil_friction_angle
        )
        self.cohesion = (
            _local_cohesion(cohesion) if local_shear_failure else cohesion
        )
        self.unit_wgt = unit_wgt
        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width
        self.f_length = foundation_size.length

        self._bcf = TerzaghiBCF(self._f_angle)

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def n_c(self) -> float:
        return self._bcf.n_c

    @property
    def n_q(self) -> float:
        return self._bcf.n_q

    @property
    def n_gamma(self) -> float:
        return self._bcf.n_gamma

    @abstractmethod
    def bearing_capacity(self) -> float: ...


class TerzaghiUBC4StripFooting(_AbstractTerzaghiUBC):

    @round_
    def bearing_capacity(self) -> float:
        expr_1 = self.cohesion * self.n_c
        expr_2 = self.unit_wgt * self.f_depth * self.n_q
        expr_3 = self.unit_wgt * self.f_width * self.n_gamma
        return expr_1 + expr_2 + 0.5 * expr_3


class TerzaghiUBC4SquareFooting(_AbstractTerzaghiUBC):

    @round_
    def bearing_capacity(self) -> float:
        expr_1 = self.cohesion * self.n_c
        expr_2 = self.unit_wgt * self.f_depth * self.n_q
        expr_3 = self.unit_wgt * self.f_width * self.n_gamma
        return 1.3 * expr_1 + expr_2 + 0.4 * expr_3


class TerzaghiUBC4CircFooting(_AbstractTerzaghiUBC):

    @round_
    def bearing_capacity(self) -> float:
        expr_1 = self.cohesion * self.n_c
        expr_2 = self.unit_wgt * self.f_depth * self.n_q
        expr_3 = self.unit_wgt * self.f_width * self.n_gamma
        return 1.3 * expr_1 + expr_2 + 0.3 * expr_3


class TerzaghiUBC4RectFooting(_AbstractTerzaghiUBC):

    @round_
    def bearing_capacity(self) -> float:
        expr_1 = self.cohesion * self.n_c
        expr_2 = self.unit_wgt * self.f_depth * self.n_q
        expr_3 = self.unit_wgt * self.f_width * self.n_gamma
        return (
            (1 + 0.3 * (self.f_width / self.f_length)) * expr_1
            + expr_2
            + (1 - 0.2 * (self.f_width / self.f_length)) / 2 * expr_3
        )
