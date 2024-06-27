from collections import UserDict
from dataclasses import dataclass
from numbers import Number

__all__ = ["DECIMAL_PLACES", "ERROR_TOL", "UNIT"]

#: The number of decimal places to round mathematical
#: values returned from functions (or methods) to.
DECIMAL_PLACES: int = 4

#: Allowable error tolerance for mathematical values
#: returned from functions (or methods).
ERROR_TOL: float = 0.01


class SoilProperties(UserDict):
    def __getattr__(self, attr) -> Number:
        return self.data[attr]


@dataclass(init=False)
class UNIT:
    """Physical units manager for values returned by various functions
    (or methods) that returns a float.

    Notes
    -----
    These units are compatible with the `pint <https://pint.readthedocs.io/en/stable/index.html>`_
    library unit system.
    """

    #: meter
    m = "meter"

    #: millimeter
    mm = "millimeter"

    #: kilogram
    kg = "kilogram"

    #: degree
    deg = "degrees"

    #: square meter
    m2 = "m**2"

    #: cubic meter
    m3 = "m**3"

    #: kilo Pascal
    kPa = "kPa"

    #: kilo Newton per cubic meter
    kN_m3 = "kN/m**3"
