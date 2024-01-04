"""This module provides classes for SPT Data Analysis."""
from functools import partial
from typing import Sequence

from geolysis.constants import ERROR_TOLERANCE, GeotechEng
from geolysis.exceptions import (
    EngineerTypeError,
    OverburdenPressureError,
    StatisticsError,
)
from geolysis.utils import isclose, log10, mean, round_, sqrt


@round_(ndigits=0)
def spt_n_design(corrected_spt_n_vals: Sequence[float]) -> float:
    """Return the weighted average of the corrected SPT N-values in the
    foundation influence zone.

    :param Sequence[float] corrected_spt_n_vals: Corrected SPT N-values
        within the foundation influence zone i.e. :math:`D_f` to :math:`D_f + 2B`

    :return: weighted average of corrected SPT N-values
    :rtype: float

    :raises StatisticError: If `corrected_spt_n_vals` is empty, StatisticError
        is raised
    """
    if len(corrected_spt_n_vals) == 0:
        msg = "spt_n_design requires at least one corrected spt n-value"
        raise StatisticsError(msg)

    total_num = 0.0
    total_den = 0.0

    for i, corrected_spt in enumerate(corrected_spt_n_vals, start=1):
        idx_weight = 1 / i**2
        total_num += idx_weight * corrected_spt
        total_den += idx_weight

    return total_num / total_den


@round_(ndigits=0)
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


@round_(ndigits=2)
def spt_n_60(
    recorded_spt_n_val: float,
    *,
    hammer_efficiency=0.6,
    borehole_diameter_correction=1,
    sampler_correction=1,
    rod_length_correction=0.75,
) -> float:
    """Return SPT N-value standardized for field procedures.

    :param float hammer_efficiency: hammer efficiency, defaults to 0.6
    :param float borehole_diameter_correction: borehole diameter correction,
        defaults to 1.0
    :param float sampler_correction: sampler correction, defaults to 1.0
    :param float rod_length_correction: rod Length correction, defaults to 0.75
    """
    correction = (
        hammer_efficiency
        * borehole_diameter_correction
        * sampler_correction
        * rod_length_correction
    )

    return (correction * recorded_spt_n_val) / 0.6


def std_recorded_spt_n_vals(recorded_spt_n_vals: Sequence[float], **kwargs):
    return list(map(partial(spt_n_60, **kwargs), recorded_spt_n_vals))


class SPTCorrections:
    """Standard Penetration Test N-value correction for **Overburden Pressure**
    and **Dilatancy**.

    The available overburden pressure corrections are ``Gibbs & Holtz (1957)``,
    ``Peck et al (1974)``, ``Liao & Whitman (1986)``, ``Skempton (1986)``, and
    ``Bazaraa & Peck (1969)``.

    The dilatancy correction presented here is given by ``Terzaghi & Peck (1948)``.
    """

    def overburden_pressure_correction(
        self,
        std_spt_n_vals: Sequence[float],
        eop: float,
        eng=GeotechEng.SKEMPTON,
    ):
        opc_func = self._select_opc_func(eng=eng)
        return list(map(partial(opc_func, eop=eop), std_spt_n_vals))

    def dilatancy_correction(self, corrected_spt_n_vals: Sequence[float]):
        return list(map(self.terzaghi_peck_dc_1948, corrected_spt_n_vals))

    @staticmethod
    @round_(ndigits=2)
    def terzaghi_peck_dc_1948(corrected_spt_n_val: float) -> float:
        """Return the dilatancy spt correction."""

        if corrected_spt_n_val <= 15:
            return corrected_spt_n_val

        return 15 + 0.5 * (corrected_spt_n_val - 15)

    @staticmethod
    @round_(ndigits=2)
    def gibbs_holtz_opc_1957(spt_n_60: float, eop: float) -> float:
        """Return the overburden pressure correction given by ``Gibbs and
        Holtz (1957)``.
        """

        std_pressure = 280

        if eop <= 0 or eop > std_pressure:
            msg = (
                f"eop: {eop} should be less than or equal to {std_pressure}"
                "but not less than or equal to 0"
            )
            raise OverburdenPressureError(msg)

        corrected_spt = spt_n_60 * (350 / (eop + 70))
        spt_ratio = corrected_spt / spt_n_60

        if 0.45 < spt_ratio < 2.0:
            return corrected_spt

        corrected_spt = corrected_spt / 2 if spt_ratio > 2.0 else corrected_spt
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def peck_et_al_opc_1974(spt_n_60: float, eop: float) -> float:
        """Return the overburden pressure given by ``Peck et al (1974)``."""
        std_pressure = 24

        if eop <= 0 or eop < std_pressure:
            msg = (
                f"eop: {eop} should be greater than or equal to {std_pressure}"
            )
            raise OverburdenPressureError(msg)

        corrected_spt = 0.77 * log10(2000 / eop) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def liao_whitman_opc_1986(spt_n_60: float, eop: float) -> float:
        """Return the overburden pressure given by ``Liao Whitman (1986)``."""
        if eop <= 0:
            msg = f"eop: {eop} greater than 0"
            raise OverburdenPressureError(msg)

        corrected_spt = sqrt(100 / eop) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def skempton_opc_1986(spt_n_60: float, eop: float) -> float:
        """Return the overburden pressure correction given by ``Skempton
        (1986).``
        """
        corrected_spt = (2 / (1 + 0.01044 * eop)) * spt_n_60
        return min(corrected_spt, 2 * spt_n_60)

    @staticmethod
    @round_(ndigits=2)
    def bazaraa_peck_opc_1969(spt_n_60: float, eop: float) -> float:
        """Return the overburden pressure correction given by ``Bazaraa
        (1967)`` and also by ``Peck and Bazaraa (1969)``.
        """

        std_pressure = 71.8

        if isclose(eop, std_pressure, rel_tol=ERROR_TOLERANCE):
            return spt_n_60

        if eop < std_pressure:
            corrected_spt = 4 * spt_n_60 / (1 + 0.0418 * eop)

        else:
            corrected_spt = 4 * spt_n_60 / (3.25 + 0.0104 * eop)

        return min(corrected_spt, 2 * spt_n_60)

    def _select_opc_func(self, eng: GeotechEng):
        if eng is GeotechEng.GIBBS:
            opc_func = self.gibbs_holtz_opc_1957

        elif eng is GeotechEng.PECK:
            opc_func = self.peck_et_al_opc_1974

        elif eng is GeotechEng.LIAO:
            opc_func = self.liao_whitman_opc_1986

        elif eng is GeotechEng.SKEMPTON:
            opc_func = self.skempton_opc_1986

        elif eng is GeotechEng.BAZARAA:
            opc_func = self.bazaraa_peck_opc_1969

        else:
            msg = (
                f"{eng} is not a valid type for overburden pressure correction"
            )
            raise EngineerTypeError(msg)

        return opc_func
