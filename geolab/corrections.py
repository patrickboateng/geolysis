from typing import Union

import numpy as np

from geolab import DECIMAL_PLACES, ERROR_TOLERANCE
from geolab.utils import product


def spt_n60(
    recorded_spt_nvalue: int,
    hammer_efficiency: float = 0.575,
    borehole_diameter_cor: float = 1.0,
    sampler_cor: float = 1.0,
    rod_length_cor: float = 0.75,
) -> float:
    r"""SPT N-value corrected for field procedures.

    .. math::

        N_{60} = \dfrac{E_m \times C_B \times C_s \times C_R \times N_r}{0.6}

    :param recorded_spt_nvalue: Recorded SPT N-value (blows/300mm)
    :type recorded_spt_nvalue: int
    :param hammer_efficiency: Hammer Efficiency, defaults to 0.575
    :type hammer_efficiency: float, optional
    :param borehole_diameter_cor: Borehole Diameter Correction, defaults to 1
    :type borehole_diameter_cor: float, optional
    :param sampler_cor: Sampler Correction, defaults to 1
    :type sampler_cor: float, optional
    :param rod_length_cor: Rod Length Correction, defaults to 0.75
    :type rod_length_cor: float
    :return: SPT N-value corrected for 60% hammer efficiency
    :rtype: float
    """
    correction = product(
        hammer_efficiency,
        borehole_diameter_cor,
        sampler_cor,
        rod_length_cor,
    )

    corrected_spt_nvalue = correction * recorded_spt_nvalue
    return round(corrected_spt_nvalue / 0.6, DECIMAL_PLACES)


def dilatancy_spt_correction(recorded_spt_nvalue: int) -> Union[float, int]:
    r"""SPT N-value Dilatancy Correction.

    **Dilatancy Correction** is a correction for silty fine sands and fine sands
    below the water table that develop pore pressure which is not easily
    dissipated. The pore pressure increases the resistance of the soil hence the
    penetration number (N). (:cite:author:`2003:arora`)

    Correction of silty fine sands recommended by ``Terzaghi and Peck (1967)`` if
    :math:`N_R` exceeds 15.

    .. math::

        N_c = 15 + \frac{1}{2}\left(N_R - 15\right) if N_R \gt 15

        N_c = N_R if N_R \le 15

    :param recorded_spt_nvalue: Recorded SPT N-value (blows/300mm)
    :type recorded_spt_nvalue: int
    :return: Corrected SPT N-value

    References
    ----------

    .. bibliography::
    """
    if recorded_spt_nvalue <= 15:
        return recorded_spt_nvalue

    corrected_spt_nvalue = 15 + 0.5 * (recorded_spt_nvalue - 15)
    return np.round(corrected_spt_nvalue, DECIMAL_PLACES)


def overburden_pressure_spt_correction(recorded_spt_nvalue: int, eop: float) -> float:
    r"""SPT N-value Overburden Pressure Correction.

    In granular soils, the overburden pressure affects the penetration resistance.
    If two soils having same relative density but different confining pressures are tested,
    the one with a higher confining pressure gives a higher penetration number. As the
    confining pressure in cohesionless soils increases with the depth, the penetration number
    for soils at shallow depths is underestimated and that at greater depths is overestimated.
    For uniformity, the N-values obtained from field tests under different effective overburden
    pressures are corrected to a standard effective overburden pressure.
    ``Gibbs and Holtz (1957)`` recommend the use of the following equation for dry or moist clean
    sand. (:cite:author:`2003:arora`, p. 428)

    .. math::

        N = \dfrac{350}{\sigma_o + 70} \times N_R if \sigma_o \le 280kN/m^2

    .. note::

        :math:`\frac{N_c}{N_R}` should lie between 0.45 and 2.0, if :math:`\frac{N_c}{N_R}` is
        greater than 2.0, :math:`N_c` should be divided by 2.0 to obtain the design value used in
        finding the bearing capacity of the soil. (:cite:author:`2003:arora`, p. 428)

    :param recorded_spt_nvalue: Recorded SPT N-value
    :type recorded_spt_nvalue: int
    :param eop: Effective overburden pressure :math:`kN/m^2`
    :type eop: float
    :return: Corrected SPT N-value
    :rtype: float

    References
    ----------

    .. bibliography::
    """
    if eop > 280:
        raise ValueError(f"{eop} should be less than or equal to 280")

    corrected_spt = recorded_spt_nvalue * (350 / (eop + 70))
    spt_ratio = corrected_spt / recorded_spt_nvalue

    if 0.45 < spt_ratio < 2.0:
        return np.round(corrected_spt, DECIMAL_PLACES)

    if spt_ratio > 2.0:
        return np.round(corrected_spt / 2, DECIMAL_PLACES)

    return np.round(corrected_spt, DECIMAL_PLACES)


def skempton_spt_correction(recorded_spt_nvalue: int, eop: float) -> float:
    r"""SPT N-value correction.

    .. math::

        N = \dfrac{2}{1 + 0.01044\sigma_o} \times N_R

    :param recorded_spt_nvalue: Recorded SPT N-value
    :type recorded_spt_nvalue: int
    :param eop: Effective overburden pressure :math:`kN/m^2`
    :type eop: float
    :return: Corrected SPT N-value
    :rtype: float
    """
    correction = 2 / (1 + 0.01044 * eop)
    corrected_spt = correction * recorded_spt_nvalue

    return np.round(corrected_spt, DECIMAL_PLACES)


def bazaraa_spt_correction(recorded_spt_nvalue: int, eop: float) -> float:
    r"""SPT N-value correction.

    This is a correction given by ``Bazaraa (1967)`` and also by ``Peck and Bazaraa (1969)``
    and it is one of the commonly used corrections.
    According to them:

    .. math::

        N = \dfrac{4N_R}{1 + 0.0418\sigma_o} if \sigma_o \lt 71.8kN/m^2

        N = \dfrac{4N_R}{3.25 + 0.0104\sigma_o} if \sigma_o \gt 71.8kN/m^2

        N = N_R if \sigma_o = 71.8kN/m^2

    :param recorded_spt_nvalue: Recorded SPT N-value.
    :type recorded_spt_nvalue: int
    :param eop: Effective overburden pressure :math:`kN/m^2`
    :type eop: float
    :return: Corrected SPT N-value
    :rtype: float
    """
    overburden_pressure = 71.8

    if np.isclose(eop, overburden_pressure, rtol=ERROR_TOLERANCE):
        return recorded_spt_nvalue

    if eop < overburden_pressure:
        spt_correction = 4 * recorded_spt_nvalue / (1 + 0.0418 * eop)
        return np.round(spt_correction, DECIMAL_PLACES)

    spt_correction = 4 * recorded_spt_nvalue / (3.25 + 0.0104 * eop)

    return np.round(spt_correction, DECIMAL_PLACES)
