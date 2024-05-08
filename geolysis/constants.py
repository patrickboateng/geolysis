from dataclasses import dataclass

__all__ = ["DECIMAL_PLACES", "ERROR_TOL", "UnitRegistry"]

#: The number of decimal places to round mathematical
#: values returned from functions (or methods) to.
DECIMAL_PLACES: int = 4

#: Allowable error tolerance for mathematical values
#: returned from functions (or methods).
ERROR_TOL: float = 0.01


@dataclass(init=False, frozen=True, slots=True)
class UnitRegistry:
    """Physical units manager for values returned by various functions (or methods)
    that returns a float.

    Attributes
    ----------
    millimetre, millimeter, mm
    metre, meter, m
    kPa, kN_m2
        kilo Pascal or kilo Newton per square metres
    kN_m3
        kilo Newton per cubic metres
    square_meters, square_metres, m2
    cubic_meters, cubic_metres, m3
    degrees, deg
    unitless

    Notes
    -----
    These units are compatible with the `pint <https://pint.readthedocs.io/en/stable/index.html>`_
    library unit system.

    Examples
    --------
    >>> from geolysis.estimators import SoilUnitWeight
    >>> from geolysis.constants import UnitRegistry as UReg

    >>> suw_est = SoilUnitWeight(std_spt_number=25)
    >>> suw_est.moist_wgt
    18.5

    >>> from pint import Quantity as Q_  # doctest: +SKIP
    >>> quant = Q_(suw_est.moist_wgt, UReg.kN_m3)  # doctest: +SKIP
    >>> quant  # doctest: +SKIP
    <Quantity(18.5, 'kilonewton / meter ** 3')>
    """

    millimetre = millimeter = mm = "millimetre"
    metre = meter = m = "metre"
    kPa = kN_m2 = "kPa"
    kN_m3 = "kN/m**3"
    square_meters = square_metres = m2 = "m**2"
    cubic_meters = cubic_metres = m3 = "m**3"
    degrees = deg = "degrees"
    unitless = ""
