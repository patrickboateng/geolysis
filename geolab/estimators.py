"""This module provides functions for estimating soil engineering parameters."""

from typing import Optional

import numpy as np


def elastic_modulus_of_soil(spt_n60: float) -> float:
    r"""Elastic modulus of soil ($kN/m^2$).

    $$E_s = 320\left(N_{60} + 15 \right)$$

    Args:
        spt_n60: The SPT N-value corrected for 60% hammer efficiency.

    Returns:
        Elastic modulus

    References:

    """
    elastic_modulus = 320 * (spt_n60 + 15)

    return np.round(elastic_modulus, 2)


def friction_angle(
    spt_n60,
    effective_overburden_pressure: Optional[float] = None,
    atmospheric_pressure: Optional[float] = None,
) -> float:
    r"""Internal angle of friction.

    For cohesionless soils the coefficient of internal friction ($\phi$) was
    determined from the minimum value from `Peck, Hanson and Thornburn (1974)`
    and `Kullhawy and Mayne (1990)`. The correlations are shown below.

    $$\phi = 27.1 + 0.3 \times N_{60} - 0.00054 \times (N_{60})^2$$

    $$\phi = \tan^{-1}\left[\dfrac{N_{60}}{12.2 + 20.3(\frac{\sigma_o}{P_a})} \right]^0.34$$

    Examples:
        >>> friction_angle(20)
        32.88
        >>> friction_angle(30)
        35.61


    Args:
        spt_n60: The SPT N-value corrected for 60% hammer efficiency. (blows/300 mm)
        effective_overburden_pressure (float): Effective overburden pressure. Defaults to None.
                                               ($kN/m^2$)
        atmospheric_pressure (float): Atmospheric pressure. ($kN/m^2$)

    Returns:
        The internal angle of friction in degrees.
    """
    if (effective_overburden_pressure is not None) and (
        atmospheric_pressure is not None
    ):
        den = 12.2 + 20.3 * (effective_overburden_pressure / atmospheric_pressure)
        phi = np.arctan(spt_n60 / den) ** 0.34
        return np.round(phi, 2)

    phi = 27.1 + (0.3 * spt_n60) - (0.00054 * (spt_n60**2))

    return np.round(phi, 2)  # rounded to 2 d.p for consistency with eng. practices


if __name__ == "__main__":
    import doctest

    doctest.testmod()
