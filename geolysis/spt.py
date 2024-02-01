from statistics import StatisticsError
from typing import Sequence

from geolysis.constants import ERROR_TOL, UNITS
from geolysis.utils import isclose, log10, mean, round_, sqrt


class OverburdenPressureError(ValueError):
    """
    Exception raised for overburden pressure related errors.
    """


@round_(ndigits=0)
def weighted_avg_spt_n_val(corrected_spt_vals: Sequence[float]) -> float:
    r"""
    Calculates the weighted average of the corrected SPT N-values in the foundation
    influence zone. (:math:`N_{design}`)

    Due to uncertainty in field procedure in standard penetration test and also
    to consider all the N-value in the influence zone of a foundation, a method
    was suggested to calculate the design N-value which should be used in
    calculating the allowable bearing capacity of shallow foundation rather than
    using a particular N-value. All the N-value from the influence zone is taken
    under consideration by giving the highest weightage to the closest N-value
    from the base.

    The determination of :math:`N_{design}` is given by:

    .. math::

        N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}{\sum_{i=1}^{n} \frac{1}{i^2}}

    - influence zone = :math:`D_f + 2B` or to a depth up to which soil
      types are approximately the same.
    - B = width of footing
    - :math:`n` = number of layers in the influence zone.
    - :math:`N_i` = corrected N-value at ith layer from the footing base.

    .. note::

        Alternatively, for ease in calculation, the lowest N-value from the influence zone
        can be taken as the :math:`N_{design}` as suggested by ``Terzaghi & Peck (1948)``.

    :param Sequence[float] corrected_spt_vals: Corrected SPT N-values within the
        foundation influence zone i.e. :math:`D_f` to :math:`D_f + 2B`

    :return: Weighted average of corrected SPT N-values
    :rtype: float

    :raises StatisticError: If ``corrected_spt_vals`` is empty, StatisticError is raised.
    """
    if not corrected_spt_vals:
        err_msg = "spt_n_design requires at least one corrected spt n-value"
        raise StatisticsError(err_msg)

    total_num = 0.0
    total_den = 0.0

    for i, corrected_spt in enumerate(corrected_spt_vals, start=1):
        idx_weight = 1 / i**2
        total_num += idx_weight * corrected_spt
        total_den += idx_weight

    return total_num / total_den


@round_(ndigits=0)
def avg_uncorrected_spt_n_val(uncorrected_spt_vals: Sequence[float]):
    """
    Calculates the average of the uncorrected SPT N-values in the foundation
    influence zone.

    :param Sequence[float] uncorrected_spt_vals: Uncorrected SPT N-values within the
        foundation influence zone i.e. :math:`D_f` |rarr| :math:`D_f + 2B`. Only water
        table correction suggested.

    :return: Average of corrected SPT N-values
    :rtype: float

    :raises StatisticError: If ``uncorrected_spt_vals`` is empty, StatisticError is raised.
    """
    if not uncorrected_spt_vals:
        msg = "spt_n_val requires at least one corrected spt n-value"
        raise StatisticsError(msg)

    return mean(uncorrected_spt_vals)


class SPTCorrections:
    r"""
    SPT N-value correction for **Overburden Pressure** and **Dilatancy**.

    There are three (3) different SPT corrections namely:

    - Energy Correction / Correction for Field Procedures
    - Overburden Pressure Corrections
    - Dilatancy Correction

    Energy correction is used to standardized the SPT N-values for field procedures.

    In cohesionless soils, penetration resistance is affected by overburden pressure.
    Soils with the same density but different confining pressures have varying penetration
    numbers, with higher pressures leading to higher penetration numbers. As depth
    increases, confining pressure rises, causing underestimation of penetration numbers
    at shallow depths and overestimation at deeper depths. The need for corrections in
    Standard Penetration Test (SPT) values was acknowledged only in 1957 by Gibbs & Holtz,
    meaning data published before this, like Terzaghi's, are based on uncorrected values.

    The general formula for overburden pressure correction is:

    .. math::

        (N_1)_{60} = C_N \cdot N_{60} \le 2 \cdot N_{60}

    Where:

    - :math:`C_N` = Overburden Pressure Correction Factor

    Available overburden pressure corrections are given by the following authors:

    - Gibbs & Holtz (1957)
    - Peck et al (1974)
    - Liao & Whitman (1986)
    - Skempton (1986)
    - Bazaraa & Peck (1969)

    **Dilatancy Correction** is a correction for silty fine sands and fine sands below the
    water table that develop pore pressure which is not easily dissipated. The pore pressure
    increases the resistance of the soil hence the standard penetration number (N).
    Correction of silty fine sands recommended by ``Terzaghi and Peck (1948)`` if :math:`N_{60}`
    exceeds 15.
    """

    unit = UNITS.unitless

    @staticmethod
    @round_(ndigits=2)
    def energy_correction(
        recorded_spt_val: float,
        *,
        percentage_energy=0.6,
        hammer_efficiency=0.6,
        borehole_diameter_correction=1,
        sampler_correction=1,
        rod_length_correction=0.75,
    ) -> float:
        r"""
        Return SPT N-value standardized for field procedures.

        On the basis of field observations, it appears reasonable to standardize the field
        SPT N-value as a function of the input driving energy and its dissipation around
        the sampler around the surrounding soil. The variations in testing procedures may
        be at least partially compensated by converting the measured N-value to :math:`N_{60}`.

        .. rubric:: Mathematical Expression

        .. math::

            N_{60} = \dfrac{E_H \cdot C_B \cdot C_S \cdot C_R \cdot N}{0.6}

        Where:

        - :math:`N_{60}` = Corrected SPT N-value for field procedures
        - :math:`E_{H}`  = Hammer efficiency
        - :math:`C_{B}`  = Borehole diameter correction
        - :math:`C_{S}`  = Sampler correction
        - :math:`C_{R}`  = Rod length correction
        - N              = Recorded SPT N-value in field

        The values of :math:`E_H`, :math:`C_B`, :math:`C_S`, and :math:`C_R` can be found in
        the table below.

        .. table:: Correction table for field procedure of SPT N-value

            +--------------------+------------------------------+--------------------------------+
            | SPT Hammer Efficiencies                                                            |
            +====================+==============================+================================+
            | **Hammer Type**    | **Hammer Release Mechanism** | **Efficiency**, :math:`E_H`    |
            +--------------------+------------------------------+--------------------------------+
            | Automatic          | Trip                         | 0.70                           |
            +--------------------+------------------------------+--------------------------------+
            | Donut              | Hand dropped                 | 0.60                           |
            +--------------------+------------------------------+--------------------------------+
            | Donut              | Cathead+2 turns              | 0.50                           |
            +--------------------+------------------------------+--------------------------------+
            | Safety             | Cathead+2 turns              | 0.55 - 0.60                    |
            +--------------------+------------------------------+--------------------------------+
            | Drop/Pin           | Hand dropped                 | 0.45                           |
            +--------------------+------------------------------+--------------------------------+
            | Borehole, Sampler and Rod Correction                                               |
            +--------------------+------------------------------+--------------------------------+
            | **Factor**         | **Equipment Variables**      | **Correction Factor**          |
            +--------------------+------------------------------+--------------------------------+
            | Borehole Dia       | 65 - 115 mm (2.5-4.5 in)     | 1.00                           |
            | Factor,            |                              |                                |
            | :math:`C_B`        |                              |                                |
            +--------------------+------------------------------+--------------------------------+
            |                    | 150 mm (6 in)                | 1.05                           |
            +--------------------+------------------------------+--------------------------------+
            |                    | 200 mm (8 in)                | 1.15                           |
            +--------------------+------------------------------+--------------------------------+
            | Sampler            | Standard sampler             | 1.00                           |
            | Correction,        |                              |                                |
            | :math:`C_S`        |                              |                                |
            +--------------------+------------------------------+--------------------------------+
            |                    | Sampler without liner        | 1.20                           |
            |                    | (not recommended)            |                                |
            +--------------------+------------------------------+--------------------------------+
            | Rod Length         | 3 - 4 m (10-13 ft)           | 0.75                           |
            | Correction,        |                              |                                |
            | :math:`C_R`        |                              |                                |
            +--------------------+------------------------------+--------------------------------+
            |                    | 4 - 6 m (13-20 ft)           | 0.85                           |
            +--------------------+------------------------------+--------------------------------+
            |                    | 6 - 10 m (20-30 ft)          | 0.95                           |
            +--------------------+------------------------------+--------------------------------+
            |                    | >10 m (>30 ft)               | 1.00                           |
            +--------------------+------------------------------+--------------------------------+

        :param float percentage_energy: Percentage energy reaching the tip of the sampler.
        :param int recorded_spt_val: Recorded SPT N-value from field.
        :kwparam float hammer_efficiency: hammer efficiency, defaults to 0.6
        :kwparam float borehole_diameter_correction: borehole diameter correction,
            defaults to 1.0
        :kwparam float sampler_correction: sampler correction, defaults to 1.0
        :kwparam float rod_length_correction: rod Length correction, defaults to 0.75

        .. note::

            The ``energy correction`` is to be applied irrespective of the type of soil.
        """
        correction = (
            hammer_efficiency
            * borehole_diameter_correction
            * sampler_correction
            * rod_length_correction
        )

        return (correction * recorded_spt_val) / percentage_energy

    @staticmethod
    @round_(ndigits=2)
    def terzaghi_peck_dc_1948(corrected_spt_val: float) -> float:
        r"""
        Return the dilatancy spt correction.

        :param float corrected_spt_val: Corrected SPT N-value. This should be corrected
            using any of the overburden pressure corrections.

        .. rubric:: Mathematical Expression

        .. math::

            (N_1)_{60} &= 15 + \dfrac{1}{2}((N_1)_{60} - 15) \, , \, (N_1)_{60} \gt 15

            (N_1)_{60} &= (N_1)_{60} \, , \, (N_1)_{60} \le 15

        .. note::

            For coarse sand, this correction is not required. In applying this correction,
            overburden pressure correction is applied first and then dilatancy correction
            is applied.
        """

        if corrected_spt_val <= 15:
            return corrected_spt_val

        return 15 + 0.5 * (corrected_spt_val - 15)

    @staticmethod
    @round_(ndigits=2)
    def gibbs_holtz_opc_1957(spt_n_60: float, eop: float) -> float:
        r"""
        Return the overburden pressure correction given by ``Gibbs and Holtz
        (1957)``.

        :param float spt_n_60: SPT N-value standardized for field procedure. This can be
            done using :meth:`~geolysis.spt.SPTCorrections.energy_correction`.
        :param float eop: Effective overburden pressure (:math:`kN/m^2`).

        .. rubric:: Mathematical Expression

        .. math::

            C_N = \dfrac{350}{\sigma_o + 70} \, \sigma_o \le 280kN/m^2

        .. note::

            :math:`\frac{N_c}{N_{60}}` should lie between 0.45 and 2.0, if :math:`\frac{N_c}{N_{60}}`
            is greater than 2.0, :math:`N_c` should be divided by 2.0 to obtain the design value
            used in finding the bearing capacity of the soil.
        """

        std_pressure = 280

        if eop <= 0 or eop > std_pressure:
            err_msg = (
                f"eop: {eop} should be less than or equal to {std_pressure}"
                "but not less than or equal to 0"
            )
            raise OverburdenPressureError(err_msg)

        corrected_spt = spt_n_60 * (350 / (eop + 70))
        spt_ratio = corrected_spt / spt_n_60

        if 0.45 < spt_ratio < 2.0:
            return corrected_spt

        corrected_spt = corrected_spt / 2 if spt_ratio > 2.0 else corrected_spt
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def peck_et_al_opc_1974(spt_n_60: float, eop: float) -> float:
        r"""
        Return the overburden pressure given by ``Peck et al (1974)``.

        :param float spt_n_60: SPT N-value standardized for field procedure. This can be
            done using :meth:`~geolysis.spt.SPTCorrections.energy_correction`.
        :param float eop: Effective overburden pressure (:math:`kN/m^2`).

        .. rubric:: Mathematical Expression

        .. math::

            C_N = 0.77 \log \left( \dfrac{2000}{\sigma_o} \right)
        """
        std_pressure = 24

        if eop <= 0 or eop < std_pressure:
            err_msg = f"eop: {eop} >= {std_pressure}"
            raise OverburdenPressureError(err_msg)

        corrected_spt = 0.77 * log10(2000 / eop) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def liao_whitman_opc_1986(spt_n_60: float, eop: float) -> float:
        r"""
        Return the overburden pressure given by ``Liao Whitman (1986)``.

        :param float spt_n_60: SPT N-value standardized for field procedure. This can be
            done using :meth:`~geolysis.spt.SPTCorrections.energy_correction`.
        :param float eop: Effective overburden pressure (:math:`kN/m^2`).

        .. rubric:: Mathematical Expression

        .. math::

            C_N = \sqrt{\dfrac{100}{\sigma_o}}
        """
        if eop <= 0:
            err_msg = f"eop: {eop} > 0"
            raise OverburdenPressureError(err_msg)

        corrected_spt = sqrt(100 / eop) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def skempton_opc_1986(spt_n_60: float, eop: float) -> float:
        r"""
        Return the overburden pressure correction given by ``Skempton (1986).``

        :param float spt_n_60: SPT N-value standardized for field procedure. This can be
            done using :meth:`~geolysis.spt.SPTCorrections.energy_correction`.
        :param float eop: Effective overburden pressure (:math:`kN/m^2`).

        .. rubric:: Mathematical Expression

        .. math::

            C_N = \dfrac{2}{1 + 0.01044 \cdot \sigma_o}
        """
        corrected_spt = (2 / (1 + 0.01044 * eop)) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def bazaraa_peck_opc_1969(spt_n_60: float, eop: float) -> float:
        r"""
        Return the overburden pressure correction given by ``Bazaraa (1967)``
        and also by ``Peck and Bazaraa (1969)``.

        :param float spt_n_60: SPT N-value standardized for field procedure. This can be
            done using :meth:`~geolysis.spt.SPTCorrections.energy_correction`.
        :param float eop: Effective overburden pressure (:math:`kN/m^2`).

        .. rubric:: Mathematical Expression

        .. math::

            C_N &= \dfrac{4}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2

            C_N &= \dfrac{4}{3.25 + 0.0104 \cdot \sigma_o}, \, \sigma_o \gt 71.8kN/m^2

            C_N &= 1 \, , \, \sigma_o = 71.8kN/m^2
        """

        std_pressure = 71.8

        if isclose(eop, std_pressure, rel_tol=ERROR_TOL):
            return spt_n_60

        if eop < std_pressure:
            corrected_spt = 4 * spt_n_60 / (1 + 0.0418 * eop)

        else:
            corrected_spt = 4 * spt_n_60 / (3.25 + 0.0104 * eop)

        return min(corrected_spt, 2 * spt_n_60)
