import enum
from abc import ABC, abstractmethod
from typing import Literal, Optional

from geolysis import validators
from geolysis.foundation import FoundationSize, create_foundation
from geolysis.utils import inf


class SettlementError(ValueError):
    pass


class AllowableBearingCapacity(ABC):
    #: Maximum tolerable foundation settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(self, corrected_spt_n_value: float,
                 tol_settlement: float,
                 foundation_size: FoundationSize) -> None:
        self.corrected_spt_n_value = corrected_spt_n_value
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

    @property
    def corrected_spt_n_value(self) -> float:
        return self._corrected_spt_n_value

    @corrected_spt_n_value.setter
    @validators.ge(0.0)
    def corrected_spt_n_value(self, val: float) -> None:
        self._corrected_spt_n_value = val

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


from geolysis.bearing_capacity.abc.cohl.bowles_abc import (
    BowlesABC4MatFoundation, BowlesABC4PadFoundation)
from geolysis.bearing_capacity.abc.cohl.meyerhof_abc import (
    MeyerhofABC4MatFoundation, MeyerhofABC4PadFoundation)
from geolysis.bearing_capacity.abc.cohl.terzaghi_abc import (
    TerzaghiABC4MatFoundation, TerzaghiABC4PadFoundation)


class ABC_TYPE(enum.StrEnum):
    """Enumeration of available allowable bearing capacity types."""
    BOWLES = enum.auto()
    MEYERHOF = enum.auto()
    TERZAGHI = enum.auto()


def create_allowable_bearing_capacity(corrected_spt_n_value: float,
                                      tol_settlement: float,
                                      depth: float,
                                      width: float,
                                      length: Optional[float] = None,
                                      eccentricity=0.0,
                                      ground_water_level=inf,
                                      shape="SQUARE",
                                      foundation_type: Literal[
                                          "pad", "mat"] = "pad",
                                      abc_type: ABC_TYPE | str = "BOWLES",
                                      ) -> AllowableBearingCapacity:
    """ A factory function that encapsulate the creation of  allowable bearing
    capacities.

    :param corrected_spt_n_value: The corrected spt n value.
    :type corrected_spt_n_value: float

    :param tol_settlement: Tolerable settlement of foundation. (mm)
    :type tol_settlement: float

    :param depth: Depth of foundation. (m)
    :type depth: float

    :param width: Width of foundation footing. (m)
    :type width: float

    :param length: Length of foundation footing. (m)
    :type length: float, optional

    :param eccentricity: The deviation of the foundation load from the center 
                         of gravity of the foundation footing, defaults to 0.0.
                         This means that the foundation load aligns with the
                         center of gravity of the foundation footing. (m)
    :type eccentricity: float, optional

    :param ground_water_level: Depth of water below ground level. (m)
    :type ground_water_level: float

    :param shape: Shape of foundation footing, defaults to "SQUARE".
    :type shape: str, optional

    :param foundation_type: Type of foundation, defaults to "pad".
    :type foundation_type: Literal["pad", "mat"], optional

    :param abc_type: Type of allowable bearing capacity calculation to apply.
                     Available values are: "BOWLES", "MEYERHOF", "TERZAGHI".
                     defaults to "BOWLES".
    :type abc_type:  ABC_TYPE | str, optional
    """
    if isinstance(abc_type, str):
        abc_type = ABC_TYPE(abc_type.casefold())

    fnd_size = create_foundation(depth=depth, width=width, length=length,
                                 eccentricity=eccentricity,
                                 ground_water_level=ground_water_level,
                                 shape=shape)
    abc_classes = {
        ABC_TYPE.BOWLES: {
            "pad": BowlesABC4PadFoundation,
            "mat": BowlesABC4MatFoundation
        },
        ABC_TYPE.MEYERHOF: {
            "pad": MeyerhofABC4PadFoundation,
            "mat": MeyerhofABC4MatFoundation
        },
        ABC_TYPE.TERZAGHI: {
            "pad": TerzaghiABC4PadFoundation,
            "mat": TerzaghiABC4MatFoundation,
        }
    }

    if abc_type not in abc_classes:
        raise ValueError(f"abc_type {abc_type} is not supported")

    if foundation_type not in abc_classes[abc_type]:
        msg = "Unknown foundation type: {1}. Supported types: {2}"
        supported_types = list(abc_classes[abc_type].keys())
        raise ValueError(msg.format(abc_type, supported_types))

    abc_class = abc_classes[abc_type][foundation_type]
    abc = abc_class(corrected_spt_n_value=corrected_spt_n_value,
                    tol_settlement=tol_settlement, foundation_size=fnd_size)

    return abc
