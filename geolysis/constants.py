from dataclasses import dataclass

ERROR_TOL = 0.01


@dataclass(frozen=True, slots=True)
class UNITS:
    """SI units manager for values returned by various functions.

    .. note::

        These values are compatible with the `pint <https://pint.readthedocs.io/en/stable/index.html>`_
        library.
    """

    kilo_pascal = "kPa"
    kilo_newton_per_cubic_metre = "kN/m**3"
    degrees = "degrees"
    unitless = ""
