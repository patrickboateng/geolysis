import enum
from abc import ABC, abstractmethod
from typing import Protocol

from .constants import UNIT
from .foundation import FoundationSize
from .utils import PI, cos, cot, deg2rad, exp, isclose, round_, tan

kPa = UNIT.kPa


class GeotechEng(enum.Enum):
    pass


class _AbstractTerzaghiUBC(ABC):

    _unit = kPa

    def __init__(
        self,
        cohesion: float,
        unit_wgt: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.cohesion = cohesion
        self.unit_wgt = unit_wgt
        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

    @abstractmethod
    def bearing_capacity(self) -> float: ...

    @property
    def unit(self) -> str:
        return self._unit


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
        self.friction_angle = soil_friction_angle

    @property
    @round_(ndigits=2)
    def n_c(self) -> float:
        return (
            5.7
            if isclose(self.friction_angle, 0.0)
            else cot(self.friction_angle) * (self.n_q - 1)
        )

    @property
    @round_(ndigits=2)
    def n_q(self) -> float:
        num_expr = exp(
            (3 * PI / 2 - deg2rad(self.friction_angle))
            * tan(self.friction_angle)
        )
        den_expr = 2 * (cos(45 + self.friction_angle / 2)) ** 2
        return num_expr / den_expr

    @property
    @round_(ndigits=2)
    def n_gamma(self) -> float:
        return (self.n_q - 1) * tan(1.4 * self.friction_angle)


class TerzaghiUBC4StripFooting(_AbstractTerzaghiUBC):

    def __init__(
        self,
        internal_angle_of_friction: float,
        cohesion: float,
        unit_wgt: float,
        foundation_size: FoundationSize,
    ) -> None:
        #: bearing capacity factors
        self._bcf = TerzaghiBCF(internal_angle_of_friction)

        super().__init__(cohesion, unit_wgt, foundation_size)

    @round_
    def bearing_capacity(self) -> float:
        expr_1 = self.cohesion * self.n_c
        expr_2 = self.unit_wgt * self.f_depth * self.n_q
        expr_3 = self.unit_wgt * self.f_width * self.n_gamma
        return expr_1 + expr_2 + 0.5 * expr_3

    @property
    def n_c(self) -> float:
        return self._bcf.n_c

    @property
    def n_q(self) -> float:
        return self._bcf.n_q

    @property
    def n_gamma(self) -> float:
        return self._bcf.n_gamma


class TerzaghiUBC4SquareFooting:
    def __init__(self) -> None:
        pass
