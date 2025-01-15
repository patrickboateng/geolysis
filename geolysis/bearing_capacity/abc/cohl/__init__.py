from abc import ABC, abstractmethod

from geolysis.foundation import FoundationSize

class SettlementError(ValueError):
    pass


class AllowableBearingCapacity(ABC):
    #: Maximum tolerable foundation settlement (mm).
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(self, corrected_spt_number: float, 
                 tol_settlement: float,
                 foundation_size: FoundationSize) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

    @property
    def tol_settlement(self) -> float:
        return self._tol_settlement

    @tol_settlement.setter
    def tol_settlement(self, tol_settlement: float) -> None:
        self._chk_settlement(tol_settlement, self.MAX_TOL_SETTLEMENT)
        self._tol_settlement = tol_settlement

    def _sr(self) -> float:
        return self.tol_settlement / self.MAX_TOL_SETTLEMENT

    def _fd(self) -> float:
        f_d = self.foundation_size.depth
        f_w = self.foundation_size.width

        return min(1 + 0.33 * f_d / f_w, 1.33)

    @staticmethod
    def _chk_settlement(tol_settlement: float, max_tol_settlement: float):
        if tol_settlement > max_tol_settlement:
            err_msg = "tol_settlement should not be greater than 25.4mm"
            raise SettlementError(err_msg)

    @abstractmethod
    def bearing_capacity(self): ...


from geolysis.bearing_capacity.abc.cohl.bowles_abc import (BowlesABC4PadFoundation, 
    BowlesABC4MatFoundation)
from geolysis.bearing_capacity.abc.cohl.meyerhof_abc import (MeyerhofABC4PadFoundation,
    MeyerhofABC4MatFoundation)
from geolysis.bearing_capacity.abc.cohl.terzaghi_abc import (TerzaghiABC4PadFoundation,
    TerzaghiABC4MatFoundation)
