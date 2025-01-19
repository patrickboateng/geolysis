from abc import ABC, abstractmethod

from geolysis.foundation import FoundationSize
from geolysis import validators

class SettlementError(ValueError):
    pass


class AllowableBearingCapacity(ABC):
    #: Maximum tolerable foundation settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(self, corrected_spt_number: float, 
                 tol_settlement: float,
                 foundation_size: FoundationSize) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

    @property
    def corrected_spt_number(self) -> float:
        return self._corrected_spt_number

    @corrected_spt_number.setter
    @validators.ge(0.0)
    def corrected_spt_number(self, corrected_spt_number: float) -> None:
        self._corrected_spt_number = corrected_spt_number

    @property
    def tol_settlement(self) -> float:
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


from geolysis.bearing_capacity.abc.cohl.bowles_abc import (BowlesABC4PadFoundation, 
    BowlesABC4MatFoundation)
from geolysis.bearing_capacity.abc.cohl.meyerhof_abc import (MeyerhofABC4PadFoundation,
    MeyerhofABC4MatFoundation)
from geolysis.bearing_capacity.abc.cohl.terzaghi_abc import (TerzaghiABC4PadFoundation,
    TerzaghiABC4MatFoundation)
