import math

from geolab import DECIMAL_PLACES, ERROR_TOLERANCE, GeotechEng
from geolab.utils import mul, log10, sqrt


def spt_n60(
    recorded_spt_nvalue: int,
    hammer_efficiency: float = 0.6,
    borehole_diameter_correction: float = 1.0,
    sampler_correction: float = 1.0,
    rod_length_correction: float = 0.75,
) -> float:
    r"""SPT N-value corrected for field procedures according to ``Skempton (1986)``.

    .. note::

        This correction is to be applied irrespective of the type of soil.

    .. math::

        N_{60} = \dfrac{E_m \times C_B \times C_s \times C_R \times N_r}{0.6}

    :param recorded_spt_nvalue: recorded SPT N-value (blows/300mm)
    :type recorded_spt_nvalue: int
    :param hammer_efficiency: hammer efficiency, defaults to 0.575
    :type hammer_efficiency: float, optional
    :param borehole_diameter_correction: borehole diameter correction, defaults to 1.0
    :type borehole_diameter_correction: float, optional
    :param sampler_correction: sampler correction, defaults to 1.0
    :type sampler_correction: float, optional
    :param rod_length_correction: rod Length correction, defaults to 0.75
    :type rod_length_correction: float
    :return: spt N-value corrected for 60% hammer efficiency
    :rtype: float
    """
    correction = mul(
        hammer_efficiency,
        borehole_diameter_correction,
        sampler_correction,
        rod_length_correction,
    )

    corrected_spt_nvalue = (correction * recorded_spt_nvalue) / 0.6
    return round(corrected_spt_nvalue, DECIMAL_PLACES)


def _skempton_opc(spt_n60: float, eop: float) -> float:
    correction = 2 / (1 + 0.01044 * eop)
    corrected_spt = correction * spt_n60

    return round(corrected_spt, DECIMAL_PLACES)


def _bazaraa_opc(spt_n60: float, eop: float) -> float:
    std_pressure = 71.8

    if math.isclose(eop, std_pressure, rtol=ERROR_TOLERANCE):
        return spt_n60

    if eop < std_pressure:
        spt_correction = 4 * spt_n60 / (1 + 0.0418 * eop)
        return round(spt_correction, DECIMAL_PLACES)

    spt_correction = 4 * spt_n60 / (3.25 + 0.0104 * eop)
    return round(spt_correction, DECIMAL_PLACES)


def _gibbs_holtz_opc(spt_n60: float, eop: float) -> float:
    std_pressure = 280

    if eop > std_pressure:
        msg = f"{eop} should be less than or equal to {std_pressure}"
        raise ValueError(msg)

    corrected_spt = spt_n60 * (350 / (eop + 70))
    spt_ratio = corrected_spt / spt_n60

    if 0.45 < spt_ratio < 2.0:
        return round(corrected_spt, DECIMAL_PLACES)

    if spt_ratio > 2.0:
        return round(corrected_spt / 2, DECIMAL_PLACES)

    return round(corrected_spt, DECIMAL_PLACES)


def _peck_opc(spt_n60: float, eop: float) -> float:
    std_pressure = 24

    if eop < std_pressure:
        msg = f"{eop} should be greater than or equal to {std_pressure}"
        raise ValueError(msg)

    _cn = 0.77 * log10(1905 / eop)

    return round(_cn * spt_n60, DECIMAL_PLACES)


def _liao_whitman_opc(spt_n60: float, eop: float) -> float:
    return round(sqrt(100 / eop) * spt_n60, DECIMAL_PLACES)


def overburden_pressure_spt_correction(
    spt_n60: float,
    eop: float,
    eng: GeotechEng = GeotechEng.GIBBS,
) -> float:
    r"""
    SPT N-value Overburden Pressure Correction.
    ===========================================

    Gibbs and Holtz (1957)
    ----------------------

    It was only as late as in ``1957`` that ``Gibbs and Holtz`` suggested that corrections
    should be made for field ``SPT`` values for depth. As the correction factor came to be
    considered only after ``1957``, all empirical data published before ``1957`` like those
    by ``Terzaghi`` is for uncorrected values of ``SPT``.

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

    Bazaraa and Peck (1969)
    -----------------------

    This is a correction given by ``Bazaraa (1967)`` and also by ``Peck and Bazaraa (1969)``
    and it is one of the commonly used corrections.
    According to them:

    .. math::

        N = \dfrac{4N_R}{1 + 0.0418\sigma_o} if \sigma_o \lt 71.8kN/m^2

        N = \dfrac{4N_R}{3.25 + 0.0104\sigma_o} if \sigma_o \gt 71.8kN/m^2

        N = N_R if \sigma_o = 71.8kN/m^2

    Peck, Hansen and Thornburn (1974)
    ---------------------------------

    .. math::

        (N_1)_{60} = C_N \times N_{60} \le 2N_{60}

        C_N = overburden \, pressure \, coefficient \, factor

        C_N = 0.77\log(\frac{1905}{\sigma})

    Liao and Whitman (1986)
    -----------------------

    .. math::

        C_N = \sqrt{\frac{100}{\sigma}}

    Skempton
    --------

    .. math::

        C_N = \dfrac{2}{1 + 0.01044\sigma_o}

    :param spt_n60: spt N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :param eop: effective overburden pressure :math:`kN/m^2`
    :type eop: float
    :param eng: specifies the type of overburden pressure correction formula to use.
                Available values are geolab.GIBBS, geolab.BAZARAA, geolab.PECK, geolab.LIAO,
                and geolab.SKEMPTON
    :type eng: GeotechEng
    :return: corrected SPT N-value
    :rtype: float

    References
    ----------

    .. bibliography::
    """
    if eng is GeotechEng.GIBBS:
        return _gibbs_holtz_opc(spt_n60, eop)

    if eng is GeotechEng.BAZARAA:
        return _bazaraa_opc(spt_n60, eop)

    if eng is GeotechEng.PECK:
        return _peck_opc(spt_n60, eop)

    if eng is GeotechEng.LIAO:
        return _liao_whitman_opc(spt_n60, eop)

    if eng is GeotechEng.SKEMPTON:
        return _skempton_opc(spt_n60, eop)

    msg = f"{eng} is not a valid type for overburden pressure spt correction"
    raise TypeError(msg)


def dilatancy_spt_correction(spt_n60: float) -> float:
    r"""SPT N-value Dilatancy Correction.

    **Dilatancy Correction** is a correction for silty fine sands and fine sands
    below the water table that develop pore pressure which is not easily
    dissipated. The pore pressure increases the resistance of the soil hence the
    penetration number (N). (:cite:author:`2003:arora`)

    Correction of silty fine sands recommended by ``Terzaghi and Peck (1967)`` if
    :math:`N_{60}` exceeds 15.

    .. math::

        N_c = 15 + \frac{1}{2}\left(N_{60} - 15\right) if N_{60} \gt 15

        N_c = N_{60} if N_{60} \le 15

    :param spt_n60: spt N-value corrected for 60% hammer efficiency
    :type spt_n60: float
    :return: corrected SPT N-value

    References
    ----------

    .. bibliography::
    """
    if spt_n60 <= 15:
        return spt_n60

    return round(15 + 0.5 * (spt_n60 - 15), DECIMAL_PLACES)
