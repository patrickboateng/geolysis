from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Annotated

from func_validator import (
    validate_params,
    MustBeNonNegative,
    MustBeLessThanOrEqual,
)

from geolysis.foundation import Foundation
from geolysis.utils import round_, add_repr


@dataclass
class AllowableBearingCapacityResult:
    allowable_bearing_capacity: float
    depth_factor: float
    water_correction_factor: float = 1.0


@add_repr
class AllowableBearingCapacity(ABC):
    #: Maximum tolerable foundation settlement (mm).
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
            self,
            corrected_spt_n_value: float,
            tol_settlement: float,
            foundation_size: Foundation,
    ) -> None:
        self.corrected_spt_n_value = corrected_spt_n_value
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

    @property
    def corrected_spt_n_value(self) -> float:
        """Statistical average of corrected SPT N-value."""
        return self._corrected_spt_n_value

    @corrected_spt_n_value.setter
    @validate_params
    def corrected_spt_n_value(
            self,
            corrected_spt_n_value: Annotated[float, MustBeNonNegative],
    ):
        self._corrected_spt_n_value = corrected_spt_n_value

    @property
    def tol_settlement(self) -> float:
        """Tolerable settlement of foundation (mm)."""
        return self._tol_settlement

    @tol_settlement.setter
    @validate_params
    def tol_settlement(
            self,
            tol_settlement: Annotated[float, MustBeLessThanOrEqual(25.4)],
    ):
        self._tol_settlement = tol_settlement

    def _sr(self) -> float:
        """Calculate the settlement ratio."""
        return self.tol_settlement / self.MAX_TOL_SETTLEMENT

    def _fd(self) -> float:
        """Calculate the depth factor."""
        depth = self.foundation_size.depth
        width = self.foundation_size.width
        return min(1.0 + 0.33 * depth / width, 1.33)

    def bearing_capacity_results(self) -> AllowableBearingCapacityResult:
        """Return bearing capacity results with intermediate calculations.

        !!! info "Added in v0.11.0"
        """
        return AllowableBearingCapacityResult(
            allowable_bearing_capacity=self.allowable_bearing_capacity(),
            depth_factor=self._fd(),
        )

    @round_(ndigits=1)
    def allowable_bearing_capacity(self) -> float:
        """Calculates the allowable bearing capacity.

        !!! info "Added in v0.12.0"
        """
        return self._bearing_capacity()

    def allowable_applied_load(self) -> float:
        """Calculate the allowable applied load on the foundation."""
        return self._bearing_capacity() * self.foundation_size.foundation_area()

    @abstractmethod
    def _bearing_capacity(self) -> float: ...
