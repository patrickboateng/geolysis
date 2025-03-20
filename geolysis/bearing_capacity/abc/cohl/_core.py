from abc import ABC, abstractmethod

from geolysis.foundation import FoundationSize
from geolysis.utils import validators


class SettlementError(ValueError):
    """Raised when tolerable settlement is greater than the maximum 
    allowable settlement.
    """


class AllowableBearingCapacity(ABC):
    #: Maximum tolerable foundation settlement (mm).
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(self, corrected_spt_n_value: float,
                 tol_settlement: float,
                 foundation_size: FoundationSize) -> None:
        self.corrected_spt_n_value = corrected_spt_n_value
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

    @property
    def corrected_spt_n_value(self) -> float:
        """Statistical average of corrected SPT N-value."""
        return self._corrected_spt_n_value

    @corrected_spt_n_value.setter
    @validators.ge(0.0)
    def corrected_spt_n_value(self, val: float) -> None:
        self._corrected_spt_n_value = val

    @property
    def tol_settlement(self) -> float:
        """Tolerable settlement foundation (mm)."""
        return self._tol_settlement

    @tol_settlement.setter
    @validators.le(25.4, exc_type=SettlementError)
    def tol_settlement(self, tol_settlement: float) -> None:
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
