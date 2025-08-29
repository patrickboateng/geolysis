from abc import ABC, abstractmethod
from typing import Annotated

from func_validator import (
    validate_func_args,
    MustBeNonNegative,
    MustBeLessThanOrEqual,
)

from geolysis.foundation import Foundation


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
    @validate_func_args
    def corrected_spt_n_value(self, val: Annotated[float, MustBeNonNegative]):
        self._corrected_spt_n_value = val

    @property
    def tol_settlement(self) -> float:
        """Tolerable settlement of foundation (mm)."""
        return self._tol_settlement

    @tol_settlement.setter
    @validate_func_args
    def tol_settlement(
        self, tol_settlement: Annotated[float, MustBeLessThanOrEqual(25.4)]
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

    @abstractmethod
    def bearing_capacity(self): ...
