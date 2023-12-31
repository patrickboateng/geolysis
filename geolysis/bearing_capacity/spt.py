"""This module provides classes for SPT Data Analysis."""
from collections import OrderedDict
from typing import Sequence

from geolysis.constants import ERROR_TOLERANCE, GeotechEng
from geolysis.exceptions import EngineerTypeError, StatisticsError
from geolysis.utils import inf, isclose, log10, mean, prod, round_, sqrt


@round_(ndigits=0)
def spt_n_design(
    corrected_spt_n_vals: Sequence[float],
    t: bool = False,
) -> float:
    """Return the weighted average of the corrected SPT N-values in the
    foundation influence zone.

    :param Sequence[float] corrected_spt_n_vals:
        Corrected SPT N-values within the foundation influence zone i.e.
        :math:`D_f` |rarr| :math:`D_f + 2B`
    :param bool t:
        A flag used to specify that the minimum value in `corrected_spt_nvalues`
        should be taken as the :math:`N_{design}`

    :return: weighted average of corrected SPT N-values
    :rtype: float

    :raises StatisticError:
        if `corrected_spt_n_vals` is empty, StatisticError is raised
    """
    if len(corrected_spt_n_vals) == 0:
        msg = "spt_n_design requires at least one corrected spt n-value"
        raise StatisticsError(msg)

    if t:
        return min(corrected_spt_n_vals)

    total_num = 0.0
    total_den = 0.0

    for i, corrected_spt in enumerate(corrected_spt_n_vals, start=1):
        idx_weight = 1 / i**2
        total_num += idx_weight * corrected_spt
        total_den += idx_weight

    return total_num / total_den


@round_(ndigits=2)
def spt_n_val(uncorrected_spt_n_vals: Sequence[float]):
    """Return the average of the corrected SPT N-values in the foundation
    influence zone.

    :param Sequence[float] uncorrected_spt_n_vals:
        Uncorrected SPT N-values within the foundation influence zone i.e.
        :math:`D_f` |rarr| :math:`D_f + 2B`. Only water table correction
        suggested

    :return: Average of corrected SPT N-values
    :rtype: float
    """
    if len(uncorrected_spt_n_vals) == 0:
        msg = "spt_n_val requires at least one corrected spt n-value"
        raise StatisticsError(msg)

    return mean(uncorrected_spt_n_vals)


class SPTCorrections:
    """Standard Penetration Test N-value correction for **Overburden Pressure**
    and **Dilatancy**.

    The available overburden pressure corrections are ``Gibbs and Holtz (1957)``,
    ``Peck et al (1974)``, ``Liao and Whitman (1986)``, ``Skempton (1986)``, and
    ``Bazaraa and Peck (1969)``.

    :param float hammer_efficiency:
        hammer efficiency, defaults to 0.6
    :param float borehole_diameter_correction:
        borehole diameter correction, defaults to 1.0
    :param float sampler_correction:
        sampler correction, defaults to 1.0
    :param float rod_length_correction:
        rod Length correction, defaults to 0.75
    :param float eop:
        effective overburden pressure (:math:`kN/m^2`)
    """

    rod_length_correction_vals = OrderedDict(
        {(1, 4): 0.75, (4, 6): 0.85, (6, 10): 0.95, (10, inf): 1.0}
    )  # The dict keys are the rod lengths

    def __init__(
        self,
        eop: float,
        *,
        hammer_efficiency=0.6,
        borehole_diameter_correction=1.0,
        sampler_correction=1.0,
        rod_length_correction=0.75,
    ):
        self.eop = eop
        self.hammer_efficiency = hammer_efficiency
        self.borehole_diameter_correction = borehole_diameter_correction
        self.sampler_correction = sampler_correction
        self.rod_length_correction = rod_length_correction

    def __call__(
        self,
        recorded_spt_n_vals: dict[float, int],
        *,
        eng=GeotechEng.SKEMPTON,
    ):
        """Return corrected SPT N-values.

        :param int recorded_spt_n_val:
            Measured SPT N-value in the field
        :param float eop:
            Effective overburden pressure (:math:`kN/m^2`)
        :kwparam GeotechEng eng:
            specifies the type of overburden pressure correction formula to use.
            Available values are :class:`GeotechEng.GIBBS`, :class:`GeotechEng.PECK``,
            :class:`GeotechEng.LIAO`, :class:`GeotechEng.SKEMPTON`, and
            :class:`GeotechEng.BAZARAA

        .. note::

            Corrections were made considering overburden pressure only.
            Dilatancy correction should be applied seperately.
        """
        std_spt_n_vals = []

        for rod_len, spt_n_val in recorded_spt_n_vals.items():
            for rod_lens in self.rod_length_correction_vals.keys():
                if rod_lens[0] <= rod_len < rod_lens[1]:
                    self.rod_length_correction = (
                        self.rod_length_correction_vals[rod_lens]
                    )
                    std_spt_n_vals.append(self.spt_n_60(spt_n_val))

                    break

        opc_func = self._select_opc_func(eng=eng)
        corrected_spt_n_vals = list(map(opc_func, std_spt_n_vals))

        return corrected_spt_n_vals

    @round_
    def spt_n_60(self, recorded_spt_n_val: int) -> float:
        """Return SPT N-value standardized for field procedures.

        :param int recorded_spt_n_val:
            Measured SPT N-value in the field
        """
        correction = prod(
            self.hammer_efficiency,
            self.borehole_diameter_correction,
            self.sampler_correction,
            self.rod_length_correction,
        )

        return (correction * recorded_spt_n_val) / 0.6

    @round_
    def gibbs_holtz_opc_1957(self, spt_n_60: float) -> float:
        """Return the overburden pressure correction given by ``Gibbs and
        Holtz (1957)``.
        """

        std_pressure = 280

        if self.eop > std_pressure:
            msg = f"{self.eop} should be less than or equal to {std_pressure}"
            raise ValueError(msg)

        corrected_spt = spt_n_60 * (350 / (self.eop + 70))
        spt_ratio = corrected_spt / spt_n_60

        if 0.45 < spt_ratio < 2.0:
            return corrected_spt

        corrected_spt = corrected_spt / 2 if spt_ratio > 2.0 else corrected_spt
        return min(corrected_spt, 2 * spt_n_60)

    @round_
    def peck_et_al_opc_1974(self, spt_n_60: float) -> float:
        """Return the overburden pressure given by ``Peck (1974)``."""
        std_pressure = 24

        if self.eop < std_pressure:
            msg = (
                f"{self.eop} should be greater than or equal to {std_pressure}"
            )
            raise ValueError(msg)

        corrected_spt = 0.77 * log10(2000 / self.eop) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @round_
    def liao_whitman_opc_1986(self, spt_n_60: float) -> float:
        """Return the overburden pressure given by ``Liao Whitman (1986)``."""
        corrected_spt = sqrt(100 / self.eop) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @round_
    def skempton_opc_1986(self, spt_n_60: float) -> float:
        """Return the overburden pressure correction given by ``Skempton
        (1986).``
        """
        corrected_spt = (2 / (1 + 0.01044 * self.eop)) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @round_
    def bazaraa_peck_opc_1969(self, spt_n_60: float) -> float:
        """Return the overburden pressure correction given by ``Bazaraa
        (1967)`` and also by ``Peck and Bazaraa (1969)``.
        """

        std_pressure = 71.8

        if isclose(self.eop, std_pressure, rel_tol=ERROR_TOLERANCE):
            return spt_n_60

        if self.eop < std_pressure:
            corrected_spt = 4 * spt_n_60 / (1 + 0.0418 * self.eop)

        else:
            corrected_spt = 4 * spt_n_60 / (3.25 + 0.0104 * self.eop)

        return min(corrected_spt, 2 * spt_n_60)

    @round_
    def dilatancy_correction(self, corrected_spt_n_val: float) -> float:
        """Return the dilatancy spt correction."""

        if corrected_spt_n_val <= 15:
            return corrected_spt_n_val

        return 15 + 0.5 * (corrected_spt_n_val - 15)

    def _select_opc_func(self, eng):
        if eng is GeotechEng.GIBBS:
            opc_func = self.gibbs_holtz_opc_1957

        elif eng is GeotechEng.BAZARAA:
            opc_func = self.bazaraa_peck_opc_1969

        elif eng is GeotechEng.PECK:
            opc_func = self.peck_et_al_opc_1974

        elif eng is GeotechEng.LIAO:
            opc_func = self.liao_whitman_opc_1986

        elif eng is GeotechEng.SKEMPTON:
            opc_func = self.skempton_opc_1986

        else:
            msg = f"{eng} is not a valid type for overburden pressure spt correction"
            raise EngineerTypeError(msg)

        return opc_func
