from typing import Union

import numpy as np

from geolab import DECIMAL_PLACES, ERROR_TOLERANCE


def spt_n60(
    recorded_spt_nvalue: int,
    hammer_efficiency: float = 0.575,
    borehole_diameter_cor: float = 1,
    sampler_cor: float = 1,
    rod_length_cor: float = 0.75,
) -> float:
    r"""SPT N-value corrected for field procedures.

    $$N_{60} = \dfrac{E_m \times C_B \times C_s \times C_R \times N_r}{0.6}$$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        hammer_efficiency: Hammer Efficiency. Defaults to 0.575.
        borehole_diameter_cor: Borehole Diameter Correction. Defaults to 1.
        sampler_cor: Sampler Correction. Defaults to 1.
        rod_length_cor: Rod Length Correction. Defaults to 0.75.

    Returns:
        SPT N-value corrected for 60% hammer efficiency.
    """
    first_expr = (
        hammer_efficiency
        * borehole_diameter_cor
        * sampler_cor
        * rod_length_cor
        * recorded_spt_nvalue
    )

    return round(first_expr / 0.6, DECIMAL_PLACES)


def dilatancy_spt_correction(recorded_spt_nvalue: int) -> Union[float, int]:
    r"""SPT N-value Dilatancy Correction.

    **Dilatancy Correction** is a correction for silty fine sands and fine sands
    below the water table that develop pore pressure which is not easily
    dissipated. The pore pressure increases the resistance of the soil hence the
    penetration number (N).

    Correction of silty fine sands recommended by `Terzaghi and Peck (1967)` if
    $N_R$ exceeds 15.

    $N_c = 15 + \frac{1}{2}\left(N_R - 15\right)$ if $N_R \gt 15$

    $N_c = N_R$ if $N_R \le 15$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.

    Returns:
        Corrected SPT N-value.

    References:
        Arora, K 2003, _Soil Mechanics and Foundation Engineering_, 6 Edition,
        Standard Publishers Distributors, Delhi.
    """
    if recorded_spt_nvalue <= 15:
        corrected_spt_nvalue = recorded_spt_nvalue
        return corrected_spt_nvalue

    corrected_spt_nvalue = 15 + 0.5 * (recorded_spt_nvalue - 15)

    return np.round(corrected_spt_nvalue, DECIMAL_PLACES)


def overburden_pressure_spt_correction(
    recorded_spt_nvalue: int, effective_overburden_pressure: float
) -> float:
    r"""SPT N-value Overburden Pressure Correction.

    In granular soils, the overburden pressure affects the penetration resistance.
    If two soils having same relative density but different confining pressures are tested,
    the one with a higher confining pressure gives a higher penetration number. As the
    confining pressure in cohesionless soils increases with the depth, the penetration number
    for soils at shallow depths is underestimated and that at greater depths is overestimated.
    For uniformity, the N-values obtained from field tests under different effective overburden pressures
    are corrected to a standard effective overburden pressure.
    `Gibbs and Holtz (1957)` recommend the use of the following equation for dry or moist clean sand.
    (Arora 2003, p. 428)

    $N = \dfrac{350}{\sigma_o + 70} \times N_R$ if $\sigma_o \le 280kN/m^2$

    !!! Note
        $\frac{N_c}{N_R}$ should lie between 0.45 and 2.0, if $\frac{N_c}{N_R}$ is greater than 2.0,
        $N_c$ should be divided by 2.0 to obtain the design value used in finding the bearing
        capacity of the soil. (Arora 2003, p. 428)

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        effective_overburden_pressure: Effective overburden pressure. ($kN/m^2$)

    Returns:
        Corrected SPT N-value.

    References:
        Arora, K 2003, _Soil Mechanics and Foundation Engineering_, 6 edn,
        Standard Publishers Distributors, Delhi.
    """

    if effective_overburden_pressure > 280:
        raise ValueError(
            f"{effective_overburden_pressure} should be less than or equal to 280"
        )

    corrected_spt = recorded_spt_nvalue * (350 / (effective_overburden_pressure + 70))
    spt_ratio = corrected_spt / recorded_spt_nvalue

    if 0.45 < spt_ratio < 2.0:
        return np.round(corrected_spt, DECIMAL_PLACES)

    if spt_ratio > 2.0:
        return np.round(corrected_spt / 2, DECIMAL_PLACES)

    return np.round(corrected_spt, DECIMAL_PLACES)


def skempton_spt_correction(
    recorded_spt_nvalue: int, effective_overburden_pressure: float
) -> float:
    r"""SPT N-value correction.

    $$N = \dfrac{2}{1 + 0.01044\sigma_o} \times N_R$$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        effective_overburden_pressure: Effective overburden pressure. ($kN/m^2$)

    Returns:
        Corrected SPT N-value.
    """
    first_expr = 2 / (1 + 0.01044 * effective_overburden_pressure)
    corrected_spt = first_expr * recorded_spt_nvalue

    return np.round(corrected_spt, DECIMAL_PLACES)


def bazaraa_spt_correction(
    recorded_spt_nvalue: int, effective_overburden_pressure: float
) -> float:
    r"""SPT N-value correction.

    This is a correction given by `Bazaraa (1967)` and also by
    `Peck and Bazaraa (1969)` and it is one of the commonly used corrections.
    According to them:

    $N = \dfrac{4N_R}{1 + 0.0418\sigma_o}$ if $\sigma_o \lt 71.8kN/m^2$

    $N = \dfrac{4N_R}{3.25 + 0.0104\sigma_o}$ if $\sigma_o \gt 71.8kN/m^2$

    $N = N_R$ if $\sigma_o = 71.8kN/m^2$

    Args:
        recorded_spt_nvalue: Recorded SPT N-value.
        effective_overburden_pressure: Effective overburden pressure ($kN/m^2$).

    Returns:
        Corrected SPT N-value.
    """
    overburden_pressure = 71.8

    if np.isclose(
        effective_overburden_pressure, overburden_pressure, rtol=ERROR_TOLERANCE
    ):
        return recorded_spt_nvalue

    if effective_overburden_pressure < overburden_pressure:
        spt_correction = (
            4 * recorded_spt_nvalue / (1 + 0.0418 * effective_overburden_pressure)
        )
        return np.round(spt_correction, DECIMAL_PLACES)

    spt_correction = (
        4 * recorded_spt_nvalue / (3.25 + 0.0104 * effective_overburden_pressure)
    )

    return np.round(spt_correction, DECIMAL_PLACES)
