from statistics import StatisticsError
from typing import Literal, Optional, Sequence

from geolysis.constants import ERROR_TOL
from geolysis.utils import isclose, log10, mean, round_, sqrt

__all__ = ["SPT", "SPTCorrection"]


class OPCError(ValueError):
    pass


class SPT:
    r"""Standard Penetration Test.

    Parameters
    ----------
    corrected_spt_n_vals : Sequence[float]
        SPT N-values within the foundation influence zone. i.e. :math:`D_f`
        to :math:`D_f + 2B`. ``corrected_spt_n_vals`` can either be **corrected**
        or **uncorrected**.

    Attributes
    ----------
    corrected_spt_n_vals : Sequence[float]

    Raises
    ------
    StatisticError
        If ``corrected_spt_n_vals`` is empty, StatisticError is raised.

    Notes
    -----
    Weighted average :math:`(N_{design})` is given by the formula:

    .. math::

        N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}{\sum_{i=1}^{n} \frac{1}{i^2}}

    Average is given by the formula:

    .. math::  N_{avg} = \dfrac{\sum_{i=1}^{n}N_i}{n}

    Examples
    --------
    >>> from geolysis.spt import SPT
    >>> spt_n_vals = [7.0, 15.0, 18.0]
    >>> spt_avg = SPT(corrected_spt_n_vals=spt_n_vals)
    >>> spt_avg.weighted_average()
    9.37
    >>> spt_avg.average()
    13.33
    >>> spt_avg.min()
    7.0

    >>> SPT(corrected_spt_n_vals=[])
    Traceback (most recent call last):
        ...
    StatisticsError: spt_n_design requires at least one spt n-value
    """

    def __init__(self, corrected_spt_n_vals: Sequence[float]) -> None:
        self.corrected_spt_n_vals = corrected_spt_n_vals

        if not self.corrected_spt_n_vals:
            err_msg = "corrected_spt_n_vals requires at least one SPT N-value"
            raise StatisticsError(err_msg)

    @round_(ndigits=2)
    def weighted_average(self) -> float:
        """Calculates the weighted average of the corrected SPT N-values in the
        foundation influence zone. (:math:`N_{design}`)

        Due to uncertainty in field procedure in standard penetration test and also
        to consider all the N-value in the influence zone of a foundation, a method
        was suggested to calculate the design N-value which should be used in
        calculating the allowable bearing capacity of shallow foundation rather than
        using a particular N-value. All the N-value from the influence zone is taken
        under consideration by giving the highest weightage to the closest N-value
        from the base.
        """

        total = 0.0
        total_wgts = 0.0

        for i, corrected_spt in enumerate(self.corrected_spt_n_vals, start=1):
            wgt = 1 / i**2
            total += wgt * corrected_spt
            total_wgts += wgt

        return total / total_wgts

    @round_(ndigits=2)
    def average(self) -> float:
        """Calculates the average of the uncorrected SPT N-values in the foundation
        influence zone.
        """
        return mean(self.corrected_spt_n_vals)

    @round_(ndigits=2)
    def min(self) -> float:
        """For ease in calculation, the lowest N-value from the influence zone can be
        taken as the :math:`N_{design}` as suggested by ``Terzaghi & Peck (1948)``.
        """
        return min(self.corrected_spt_n_vals)


class SPTCorrection:
    r"""SPT N-value correction for **Overburden Pressure** and **Dilatancy**.

    There are three (3) different SPT corrections namely:

    - :meth:`Energy Correction <energy_correction>`
    - Overburden Pressure Corrections (OPC)
        - :meth:`Gibbs & Holtz (1957) <gibbs_holtz_opc_1957>`
        - :meth:`Bazaraa & Peck (1969) <bazaraa_peck_opc_1969>`
        - :meth:`Peck et al (1974) <peck_et_al_opc_1974>`
        - :meth:`Liao Whitman (1986) <liao_whitman_opc_1986>`
        - :meth:`Skempton (1986) <skempton_opc_1986>`
    - :meth:`Dilatancy Correction <terzaghi_peck_dc_1948>`

    The ``energy correction`` is to be applied irrespective of the type of soil.

    Parameters
    ----------
    recorded_spt_n_val : float
        Recorded SPT N-value from field.
    eop : float, default=100.0, unit = :math:`kN/m^2`
        Effective overburden pressure.
    energy_percentage : float, default=0.6
        Energy percentage reaching the tip of the sampler.
    hammer_efficiency : float, default=0.6
        Hammer efficiency, defaults to 0.6
    borehole_diameter_correction : float, default=1.0
        Borehole diameter correction
    sampler_correction : float, default=1.0
        Sampler correction
    rod_length_correction : float, default=0.75
        Rod Length correction
    opc_func : Literal["gibbs", "bazaraa", "peck", "liao", "skempton"], default=None
        Overburden pressure correction to use when correcting for dilatancy.

    Attributes
    ----------
    recorded_spt_n_val : float
    eop: float, unit = :math:`kN/m^2`
    energy_percentage : float
    hammer_efficiency : float
    borehole_diameter_correction : float
    sampler_correction : float
    rod_length_correction : float
    opc_func : str

    Notes
    -----
    The general formula for overburden pressure correction is:

    .. math:: (N_1)_{60} = C_N \cdot N_{60} \le 2 \cdot N_{60}

    Energy correction is given by the formula:

    .. math:: N_{60} = \dfrac{E_H \cdot C_B \cdot C_S \cdot C_R \cdot N}{0.6}

    ``Gibbs & Holtz`` overburden pressure correction is given by the formula:

    .. math:: C_N = \dfrac{350}{\sigma_o + 70} \, \sigma_o \le 280kN/m^2

    :math:`\frac{N_c}{N_{60}}` should lie between 0.45 and 2.0, if :math:`\frac{N_c}{N_{60}}`
    is greater than 2.0, :math:`N_c` should be divided by 2.0 to obtain the design value
    used in finding the bearing capacity of the soil.

    ``Bazaraa & Peck`` overburden pressure correction is given by the formula:

    .. math::

        C_N &= \dfrac{4}{1 + 0.0418 \cdot \sigma_o}, \, \sigma_o \lt 71.8kN/m^2

        C_N &= \dfrac{4}{3.25 + 0.0104 \cdot \sigma_o}, \, \sigma_o \gt 71.8kN/m^2

        C_N &= 1 \, , \, \sigma_o = 71.8kN/m^2

    ``Peck et al`` overburden pressure correction is given by the formula:

    .. math:: C_N = 0.77 \log \left( \dfrac{2000}{\sigma_o} \right)

    ``Liao & Whitman`` overburden pressure correction is given by the formula:

    .. math:: C_N = \sqrt{\dfrac{100}{\sigma_o}}

    ``Skempton`` overburden pressure correction is given by the formula:

    .. math:: C_N = \dfrac{2}{1 + 0.01044 \cdot \sigma_o}

    For coarse sand, this correction is not required. In applying this correction,
    overburden pressure correction is applied first and then dilatancy correction
    is applied.

    Dilatancy correction is given by the formula:

    .. math::

        (N_1)_{60} &= 15 + \dfrac{1}{2}((N_1)_{60} - 15) \, , \, (N_1)_{60} \gt 15

        (N_1)_{60} &= (N_1)_{60} \, , \, (N_1)_{60} \le 15

    Examples
    --------
    >>> from geolysis.spt import SPTCorrection
    >>> spt_correction = SPTCorrection(recorded_spt_n_val=30, eop=100, opc_func="gibbs")

    Energy Correction

    >>> spt_correction.energy_correction()
    22.5

    Overburden Pressure Corrections

    >>> spt_correction.gibbs_holtz_opc_1957()
    23.16
    >>> spt_correction.bazaraa_peck_opc_1969()
    20.98
    >>> spt_correction.peck_et_al_opc_1974()
    22.54
    >>> spt_correction.liao_whitman_opc_1986()
    22.5
    >>> spt_correction.skempton_opc_1986()
    22.02

    Dilatancy Correction

    >>> spt_correction.terzaghi_peck_dc_1948()
    19.08
    """

    def __init__(
        self,
        recorded_spt_n_val: float,
        eop: float = 100.0,
        *,
        energy_percentage=0.6,
        hammer_efficiency=0.6,
        borehole_diameter_correction=1.0,
        sampler_correction=1.0,
        rod_length_correction=0.75,
        opc_func: Optional[
            Literal["gibbs", "bazaraa", "peck", "liao", "skempton"]
        ] = None,
    ) -> None:
        self.recorded_spt_n_val = recorded_spt_n_val
        self.eop = eop
        self.energy_percentage = energy_percentage
        self.hammer_efficiency = hammer_efficiency
        self.borehole_diameter_correction = borehole_diameter_correction
        self.sampler_correction = sampler_correction
        self.rod_length_correction = rod_length_correction
        self.opc_func = opc_func

    @round_(ndigits=2)
    def energy_correction(self) -> float:
        """SPT N-value standardized for field procedures.

        On the basis of field observations, it appears reasonable to standardize the field
        SPT N-value as a function of the input driving energy and its dissipation around
        the sampler around the surrounding soil. The variations in testing procedures may
        be at least partially compensated by converting the measured N-value to :math:`N_{60}`.
        """
        correction = (
            self.hammer_efficiency
            * self.borehole_diameter_correction
            * self.sampler_correction
            * self.rod_length_correction
        )

        return (correction * self.recorded_spt_n_val) / self.energy_percentage

    @round_(ndigits=2)
    def terzaghi_peck_dc_1948(self) -> float:
        """Return the dilatancy spt correction given by ``Terzaghi & Peck (1948)``."""

        match self.opc_func:
            case None:
                corrected_spt = self.energy_correction()
            case "gibbs":
                corrected_spt = self.gibbs_holtz_opc_1957()
            case "bazaraa":
                corrected_spt = self.bazaraa_peck_opc_1969()
            case "peck":
                corrected_spt = self.peck_et_al_opc_1974()
            case "liao":
                corrected_spt = self.liao_whitman_opc_1986()
            case "skempton":
                corrected_spt = self.skempton_opc_1986()
            case _:
                err_msg = f"{self.opc_func} is not a valid overburden pressure correction"
                raise ValueError(err_msg)

        if corrected_spt <= 15:
            return corrected_spt

        return 15 + 0.5 * (corrected_spt - 15)

    @round_(ndigits=2)
    def gibbs_holtz_opc_1957(self) -> float:
        """Return the overburden pressure correction given by ``Gibbs & Holtz (1957)``."""
        STD_PRESSURE = 280

        if self.eop <= 0 or self.eop > STD_PRESSURE:
            err_msg = (
                "eop should be less than or equal to 280"
                " but not less than or equal to 0"
            )
            raise OPCError(err_msg)

        spt_n_60 = self.energy_correction()
        corrected_spt = spt_n_60 * (350.0 / (self.eop + 70))
        spt_ratio = corrected_spt / spt_n_60

        if 0.45 < spt_ratio < 2.0:
            return corrected_spt

        corrected_spt = corrected_spt / 2 if spt_ratio > 2.0 else corrected_spt
        return min(corrected_spt, 2 * spt_n_60)

    @round_(ndigits=2)
    def bazaraa_peck_opc_1969(self) -> float:
        """Return the overburden pressure correction given by ``Bazaraa (1967)``
        and also by ``Peck and Bazaraa (1969)``.
        """
        STD_PRESSURE = 71.8
        spt_n_60 = self.energy_correction()

        if isclose(self.eop, STD_PRESSURE, rel_tol=ERROR_TOL):
            return spt_n_60

        if self.eop < STD_PRESSURE:
            corrected_spt = 4 * spt_n_60 / (1 + 0.0418 * self.eop)
        else:
            corrected_spt = 4 * spt_n_60 / (3.25 + 0.0104 * self.eop)

        return min(corrected_spt, 2 * spt_n_60)

    @round_(ndigits=2)
    def peck_et_al_opc_1974(self) -> float:
        """Return the overburden pressure given by ``Peck et al (1974)``."""
        STD_PRESSURE = 24

        if self.eop < STD_PRESSURE:
            err_msg = "eop cannot be less than 24"
            raise OPCError(err_msg)

        spt_n_60 = self.energy_correction()
        corrected_spt = 0.77 * log10(2000 / self.eop) * spt_n_60

        return min(corrected_spt, 2 * spt_n_60)

    @round_(ndigits=2)
    def liao_whitman_opc_1986(self) -> float:
        """Return the overburden pressure given by ``Liao Whitman (1986)``."""
        if self.eop <= 0:
            err_msg = "eop cannot be less than or equal to 0"
            raise OPCError(err_msg)

        spt_n_60 = self.energy_correction()
        corrected_spt = sqrt(100 / self.eop) * spt_n_60

        return min(corrected_spt, 2 * spt_n_60)

    @round_(ndigits=2)
    def skempton_opc_1986(self) -> float:
        """Return the overburden pressure correction given by ``Skempton (1986).``"""
        spt_n_60 = self.energy_correction()
        corrected_spt = (2 / (1 + 0.01044 * self.eop)) * spt_n_60

        return min(corrected_spt, 2 * spt_n_60)
