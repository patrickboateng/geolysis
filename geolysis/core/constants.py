from dataclasses import dataclass
from typing import Any

__all__ = ["DECIMAL_PLACES", "ERROR_TOL", "UNIT"]

#: The number of decimal places to round mathematical
#: values returned from functions (or methods) to.
DECIMAL_PLACES: int = 4

#: Allowable error tolerance for mathematical values
#: returned from functions (or methods).
ERROR_TOL: float = 0.01


@dataclass(init=False)
class UNIT:
    """Physical units manager for values returned by various functions
    (or methods) that returns a float.

    Attributes
    ----------
    m : str
        meter
    mm : str
        millimeter
    kg : str
        kilogram
    deg : str
        degree
    m2 : str
        square meter
    m3 : str
        cubic meter
    kPa : str
        kilo Pascal
    kN_m3 : str
        kilo Newton per cubic meter

    Notes
    -----
    These units are compatible with the `pint <https://pint.readthedocs.io/en/stable/index.html>`_
    library unit system.
    """

    m = "meter"
    mm = "millimeter"
    kg = "kilogram"
    deg = "degrees"
    m2 = "m**2"
    m3 = "m**3"
    kPa = "kPa"
    kN_m3 = "kN/m**3"
