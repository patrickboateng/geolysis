from collections import UserDict
from dataclasses import dataclass
from typing import Any

__all__ = ["DECIMAL_PLACES", "ERROR_TOL", "UnitRegistry"]

#: The number of decimal places to round mathematical
#: values returned from functions to.
DECIMAL_PLACES: int = 4

#: Allowable error tolerance for mathematical values
#: returned from functions.
ERROR_TOL: float = 0.01


class GDict(UserDict):
    """A custom dictionary datastructure."""

    def __getattr__(self, __name: str) -> Any:
        return self.data[__name]


@dataclass(init=False, frozen=True, slots=True)
class UnitRegistry:
    """Physical units manager for values returned by various functions and
    attributes within a class.

    Attributes
    ----------
    metre, m
    kPa
        kilo Pascal or kilo Newton per square metres
    kN_m3
        kilo Newton per cubic metres
    degrees, deg
    unitless

    Notes
    -----
    These units are compatible with the `pint <https://pint.readthedocs.io/en/stable/index.html>`_
    library unit system.
    """

    metre = m = "metre"
    kPa = "kPa"
    kN_m3 = "kN/m**3"
    degrees = deg = "degrees"
    unitless = ""
