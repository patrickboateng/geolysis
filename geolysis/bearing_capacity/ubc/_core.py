from abc import ABC, abstractmethod
from typing import Annotated

from func_validator import (
    validate_func_args,
    MustBeNonNegative,
    MustBePositive,
)

from geolysis.foundation import Foundation
from geolysis.utils import arctan, round_, tan


class UltimateBearingCapacity(ABC):
    def __init__(
            self,
            friction_angle: float,
            cohesion: float,
            moist_unit_wgt: float,
            foundation_size: Foundation,
            apply_local_shear: bool = False,
    ) -> None:
        r"""
        :param friction_angle: Internal angle of friction for general
                               shear failure (degrees).
        :param cohesion: Cohesion of soil ($kPa$).
        :param moist_unit_wgt: Moist unit weight of soil ($kN/m^3$).
        :param foundation_size: Size of the foundation.
        :param apply_local_shear: Indicate whether bearing capacity
                                  failure is general shear or local
                                  shear failure.
        """
        self.friction_angle = friction_angle
        self.cohesion = cohesion
        self.moist_unit_wgt = moist_unit_wgt
        self.foundation_size = foundation_size
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
            return arctan((2.0 / 3.0) * tan(self._friction_angle))
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

        $$
        C^{'} = \dfrac{2}{3} \cdot C
        $$
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

        if water_level is None:
            water_corr = 1.0  # water correction
        else:
            # water level above the base of the foundation
            a = max(depth - water_level, 0.0)
            water_corr = min(1 - 0.5 * a / depth, 1)

        # effective overburden pressure (surcharge)
        eop = self.moist_unit_wgt * depth
        return eop * self.n_q * self.s_q * self.d_q * self.i_q * water_corr

    def _embedment_term(self, coef: float = 0.5) -> float:
        depth = self.foundation_size.depth
        width = self.foundation_size.effective_width
        water_level = self.foundation_size.ground_water_level

        if water_level is None:
            # water correction
            water_corr = 1.0
        else:
            #: b -> water level below the base of the foundation
            b = max(water_level - depth, 0)
            water_corr = min(0.5 + 0.5 * b / width, 1)

        return (
                coef
                * self.moist_unit_wgt
                * width
                * self.n_gamma
                * self.s_gamma
                * self.d_gamma
                * self.i_gamma
                * water_corr
        )

    @round_(ndigits=2)
    def bearing_capacity(self) -> float:
        """Calculates the ultimate bearing capacity."""
        return (
                self._cohesion_term(1.0)
                + self._surcharge_term()
                + self._embedment_term(0.5)
        )

    def bearing_capacity_results(self) -> dict:
        """Return a dictionary of bearing capacity results with
        intermediate calculations.

        !!! info "Added in v0.11.0"

        """
        return {
            "bearing_capacity": self.bearing_capacity(),
            "n_c": self.n_c,
            "n_q": self.n_q,
            "n_gamma": self.n_gamma,
            "s_c": self.s_c,
            "s_q": self.s_q,
            "s_gamma": self.s_gamma,
            "d_c": self.d_c,
            "d_q": self.d_q,
            "d_gamma": self.d_gamma,
            "i_c": self.i_c,
            "i_q": self.i_q,
            "i_gamma": self.i_gamma,
        }

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
