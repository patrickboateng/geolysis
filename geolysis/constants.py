from dataclasses import dataclass

#: Error tolerance
ERROR_TOL = 0.01


@dataclass(frozen=True, slots=True)
class UNITS:
    """SI units manager for values returned by various functions.

    .. note::

        These units are compatible with the `pint <https://pint.readthedocs.io/en/stable/index.html>`_
        library unit system.
    """

    kPa = "kPa"
    kN_m3 = "kN/m**3"
    degrees = "degrees"
    unitless = ""
