from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Annotated, Optional

from func_validator import (
    validate_func_args,
    MustBeNonNegative,
    MustBePositive,
)

from geolysis.foundation import Foundation
from geolysis.utils import arctandeg, round_, tandeg


@dataclass(frozen=True, slots=True)
class UltimateBearingCapacityResult:
    ultimate_bearing_capacity: float
    allowable_bearing_capacity: float
    allowable_applied_load: float
    n_c: float
    n_q: float
    n_gamma: float
    s_c: float
    s_q: float
    s_gamma: float
    d_c: float
    d_q: float
    d_gamma: float
    i_c: float
    i_q: float
    i_gamma: float


class UltimateBearingCapacity(ABC):
    def __init__(
            self,
            friction_angle: float,
            cohesion: float,
            moist_unit_wgt: float,
            foundation_size: Foundation,
            saturated_unit_wgt: float = 20.5,
            apply_local_shear: bool = False,
            factor_of_safety: float = 3.0,
    ) -> None:
        r"""
        :param friction_angle: Internal angle of friction for general
                               shear failure (degrees).
        :param cohesion: Cohesion of soil ($kPa$).
        :param moist_unit_wgt: Moist unit weight of soil ($kN/m^3$).
        :param foundation_size: Size of the foundation.
        :param saturated_unit_wgt: Saturated unit weight of soil ($kN/m^3$).
        :param factor_of_safety: Factor of safety against bearing
                                 capacity failure. Added in v0.12.0.
        :param apply_local_shear: Indicate whether bearing capacity
                                  failure is general shear or local
                                  shear failure.
        """
        self.friction_angle = friction_angle
        self.cohesion = cohesion
        self.moist_unit_wgt = moist_unit_wgt
        self.foundation_size = foundation_size
        self.saturated_unit_wgt = saturated_unit_wgt
        self.factor_of_safety = factor_of_safety
        self.apply_local_shear = apply_local_shear

    @property
    def friction_angle(self) -> float:
        r"""Return friction angle for local shear in the case of local shear
        failure or general shear in the case of general shear failure.

        In the case of local shear failure:

        $$
        \phi' = \tan^{-1} \left(\frac{2}{3} \tan \phi\right)
        $$

        """
        if self.apply_local_shear:
            return arctandeg((2.0 / 3.0) * tandeg(self._friction_angle))
        return self._friction_angle

    @friction_angle.setter
    @validate_func_args
    def friction_angle(self, val: Annotated[float, MustBeNonNegative]):
        self._friction_angle = val

    @property
    def cohesion(self) -> float:
        r"""Return cohesion for local shear in the case of local shear failure
        or general shear in the case of general shear failure.

        In the case of local shear failure:

        $$C^{'} = \dfrac{2}{3} \cdot C$$
        """
        if self.apply_local_shear:
            return (2.0 / 3.0) * self._cohesion
        return self._cohesion

    @cohesion.setter
    @validate_func_args
    def cohesion(self, val: Annotated[float, MustBeNonNegative]):
        self._cohesion = val

    @property
    def moist_unit_wgt(self) -> float:
        """Moist unit weight of soil ($kN/m^3$)."""
        return self._moist_unit_wgt

    @moist_unit_wgt.setter
    @validate_func_args
    def moist_unit_wgt(self, val: Annotated[float, MustBePositive]):
        self._moist_unit_wgt = val

    @property
    def saturated_unit_wgt(self) -> float:
        """Saturated unit weight of soil ($kN/m^3$)."""
        return self._saturated_unit_wgt

    @saturated_unit_wgt.setter
    @validate_func_args
    def saturated_unit_wgt(self, val: Annotated[float, MustBePositive]):
        self._saturated_unit_wgt = val

    @property
    def load_angle(self):
        """Inclination of the applied load with the  vertical."""
        return self.foundation_size.load_angle

    @property
    def s_c(self) -> float:
        return 1.0

    @property
    def s_q(self) -> float:
        return 1.0

    @property
    def s_gamma(self) -> float:
        return 1.0

    @property
    def d_c(self) -> float:
        return 1.0

    @property
    def d_q(self) -> float:
        return 1.0

    @property
    def d_gamma(self) -> float:
        return 1.0

    @property
    def i_c(self) -> float:
        return 1.0

    @property
    def i_q(self) -> float:
        return 1.0

    @property
    def i_gamma(self) -> float:
        return 1.0

    def _cohesion_term(self, coef: float = 1.0) -> float:
        return coef * self.cohesion * self.n_c * self.s_c * self.d_c * self.i_c

    def _surcharge_term(self) -> float:
        depth = self.foundation_size.depth
        water_level = self.foundation_size.ground_water_level

        unit_wgt = self.moist_unit_wgt
        eop = unit_wgt * depth
        if water_level is not None:
            if water_level < depth:
                d_1 = water_level
                d_2 = depth - d_1
                unit_wgt = self.saturated_unit_wgt - 9.81
                eop = self.moist_unit_wgt * d_1 + unit_wgt * d_2
        return eop * self.n_q * self.s_q * self.d_q * self.i_q

    def _embedment_term(self, coef: float = 0.5) -> float:
        depth = self.foundation_size.depth
        width = self.foundation_size.effective_width
        water_level = self.foundation_size.ground_water_level

        unit_wgt = self.moist_unit_wgt

        if water_level is not None:
            wgt = self.saturated_unit_wgt - 9.81
            if water_level < depth:
                unit_wgt = wgt
            else:
                d = water_level - depth
                if d <= width:
                    unit_wgt = wgt + (d / width) * (self.moist_unit_wgt - wgt)

        return (
                coef
                * unit_wgt
                * width
                * self.n_gamma
                * self.s_gamma
                * self.d_gamma
                * self.i_gamma
        )

    def _bearing_capacity(self) -> float:
        return (
                self._cohesion_term(1.0)
                + self._surcharge_term()
                + self._embedment_term(0.5)
        )

    def bearing_capacity_results(self) -> UltimateBearingCapacityResult:
        """Return a dictionary of bearing capacity results with
        intermediate calculations.

        !!! info "Added in v0.11.0"

        """
        return UltimateBearingCapacityResult(
            ultimate_bearing_capacity=self.ultimate_bearing_capacity(),
            allowable_bearing_capacity=self.allowable_bearing_capacity(),
            allowable_applied_load=self.allowable_applied_load(),
            n_c=self.n_c,
            n_q=self.n_q,
            n_gamma=self.n_gamma,
            s_c=self.s_c,
            s_q=self.s_q,
            s_gamma=self.s_gamma,
            d_c=self.d_c,
            d_q=self.d_q,
            d_gamma=self.d_gamma,
            i_c=self.i_c,
            i_q=self.i_q,
            i_gamma=self.i_gamma,
        )

    @round_(ndigits=1)
    def ultimate_bearing_capacity(self) -> float:
        """Calculates the ultimate bearing capacity.

        !!! info "Added in v0.12.0"
        """
        return self._bearing_capacity()

    @round_(ndigits=1)
    def allowable_bearing_capacity(self) -> float:
        """Calculates the allowable bearing capacity.

        !!! info "Added in v0.12.0"
        """
        return self._bearing_capacity() / self.factor_of_safety

    @round_(ndigits=1)
    def allowable_applied_load(self) -> float:
        """Calculates the allowable applied load.

        !!! info "Added in v0.12.0"
        """
        area = self.foundation_size.foundation_area()
        return self.allowable_bearing_capacity() * area

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
