"""This module provides classes for SPT Data Analysis."""
from typing import Sequence

from geolysis import ERROR_TOLERANCE, GeotechEng
from geolysis.utils import isclose, log10, prod, round_, sqrt


@round_(precision=2)
def n_design(corrected_spt_nvalues: Sequence[float], t: bool = False) -> float:
    r"""Returns the weighted average of the corrected SPT N-values
    in the foundation influence zone.

    influence zone = :math:`D_f + 2B` or to a depth up to which soil
    types are approximately the same.

    B = width of foundation

    .. math::

        N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}{\sum_{i=1}^{n} \frac{1}{i^2}}

    - :math:`n` |rarr| number of layers in the influence zone.
    - :math:`N_i` |rarr| corrected N-value at ith layer from the
      footing base.

    .. note::

        Alternatively, for ease in calculation, the lowest N-value from
        the influence zone can be taken as the :math:`N_{design}` as
        suggested by ``Terzaghi & Peck (1948)``.

    :param Sequence[float] corrected_spt_nvalues:
        Corrected SPT N-values in the foundation influence zone
    :param bool t:
        A flag used to specify that the minimum value in `corrected_spt_nvalues`
        should be taken as the :py:func:`n_design`

    :return: weighted average of corrected SPT N-values
    :rtype: float
    """
    if len(corrected_spt_nvalues) == 0:
        return 0.0

    if t:
        return min(corrected_spt_nvalues)

    total_num = 0.0
    total_den = 0.0

    for i, corrected_spt in enumerate(corrected_spt_nvalues, start=1):
        idx_weight = 1 / i**2
        total_num += idx_weight * corrected_spt
        total_den += idx_weight

    return total_num / total_den


class SPTCorrections:
    r"""Standard Penetration Test N-value correction for **Overburden
    Pressure** and **Dilatancy**.

    The available overburden pressure corrections are :meth:`skempton_opc_1986`,
    :meth:`bazaraa_peck_opc_1969`, :meth:`gibbs_holtz_opc_1957`,
    :meth:`peck_et_al_opc_1974`, and :meth:`liao_whitman_opc_1986`.

    :param float hammer_efficiency:
        hammer efficiency, defaults to 0.6
    :param float borehole_diameter_correction:
        borehole diameter correction, defaults to 1.0
    :param float sampler_correction:
        sampler correction, defaults to 1.0
    :param float rod_length_correction:
        rod Length correction, defaults to 0.75
    :param float eop:
        effective overburden pressure :math:`kN/m^2`
    """

    def __init__(
        self,
        *,
        hammer_efficiency: float = 0.6,
        borehole_diameter_correction: float = 1.0,
        sampler_correction: float = 1.0,
        rod_length_correction: float = 0.75,
        # eop: float = 0.0,
    ):
        self.hammer_efficiency = hammer_efficiency
        self.borehole_diameter_correction = borehole_diameter_correction
        self.sampler_correction = sampler_correction
        self.rod_length_correction = rod_length_correction
        # self.eop = eop

    @round_(precision=2)
    def spt_n60(self, recorded_spt_nval: int) -> float:
        r"""Return SPT N-value for field procedures.

        :param int recorded_spt_nval:
            Measured SPT N-value in the field
        """
        correction = prod(
            self.hammer_efficiency,
            self.borehole_diameter_correction,
            self.sampler_correction,
            self.rod_length_correction,
        )

        return (correction * recorded_spt_nval) / 0.6

    def gibbs_holtz_opc_1957(
        self,
        recorded_spt_nval: int,
        eop: float,
    ) -> float:
        r"""Return the overburden pressure correction given by
        ``Gibbs and Holtz``.

        :param int recorded_spt_nval:
            Measured SPT N-value in the field
        """

        std_pressure = 280

        if eop > std_pressure:
            msg = f"{eop} should be less than or equal to {std_pressure}"
            raise ValueError(msg)

        spt_n60 = self.spt_n60(recorded_spt_nval)

        corrected_spt = spt_n60 * (350 / (eop + 70))
        spt_ratio = corrected_spt / spt_n60

        if 0.45 < spt_ratio < 2.0:
            return corrected_spt

        corrected_spt = corrected_spt / 2 if spt_ratio > 2.0 else corrected_spt

        return min(corrected_spt, 2 * spt_n60)

    def peck_et_al_opc_1974(self, recorded_spt_nval: int, eop: float) -> float:
        r"""Return the overburden pressure given by ``Peck (1974)``.

        :param int recorded_spt_nval:
            Measured SPT N-value in the field
        """
        std_pressure = 24

        if eop < std_pressure:
            msg = f"{eop} should be greater than or equal to {std_pressure}"

            raise ValueError(msg)

        spt_n60 = self.spt_n60(recorded_spt_nval)
        corrected_spt = 0.77 * log10(2000 / eop) * spt_n60

        return min(corrected_spt, 2 * spt_n60)

    def liao_whitman_opc_1986(
        self,
        recorded_spt_nval: int,
        eop: float,
    ) -> float:
        r"""Return the overburden pressure given by ``Liao Whitman (1986)``.

        :param int recorded_spt_nval:
            Measured SPT N-value in the field
        """
        spt_n60 = self.spt_n60(recorded_spt_nval)
        corrected_spt = sqrt(100 / eop) * spt_n60

        return min(corrected_spt, 2 * spt_n60)

    def skempton_opc_1986(self, recorded_spt_nval: int, eop: float) -> float:
        r"""Return the overburden pressure correction given by
        ``Skempton (1986).``

        :param int recorded_spt_nval:
            Measured SPT N-value in the field
        """
        spt_n60 = self.spt_n60(recorded_spt_nval)
        corr_spt = (2 / (1 + 0.01044 * eop)) * spt_n60

        return min(corr_spt, 2 * spt_n60)

    def bazaraa_peck_opc_1969(
        self,
        recorded_spt_nval: int,
        eop: float,
    ) -> float:
        r"""Return the overburden pressure correction given by
        ``Bazaraa (1967)`` and also by ``Peck and Bazaraa (1969)``.

        :param int recorded_spt_nval:
            Measured SPT N-value in the field
        """

        spt_n60 = self.spt_n60(recorded_spt_nval)
        std_pressure = 71.8

        if isclose(eop, std_pressure, rel_tol=ERROR_TOLERANCE):
            return spt_n60

        if eop < std_pressure:
            corrected_spt = 4 * spt_n60 / (1 + 0.0418 * eop)

        else:
            corrected_spt = 4 * spt_n60 / (3.25 + 0.0104 * eop)

        return min(corrected_spt, 2 * spt_n60)

    @round_(precision=2)
    def dilatancy_correction(self, recorded_spt_nval: int) -> float:
        r"""Return the dilatancy spt correction.

        :param int recorded_spt_nval:
            Measured SPT N-value in the field
        """

        spt_n60 = self.spt_n60(recorded_spt_nval)

        if spt_n60 <= 15:
            return spt_n60

        return 15 + 0.5 * (spt_n60 - 15)

    @round_(precision=2)
    def overburden_pressure_correction(
        self,
        recorded_spt_nval: int,
        eop: float,
        eng: GeotechEng = GeotechEng.GIBBS,
    ) -> float:
        """Return the overburden pressure spt correction.

        :param int recorded_spt_nval:
            Measured SPT N-value in the field

        :param GeotechEng eng:
            specifies the type of overburden pressure correction formula to use.
            Available values are ``GeotechEng.GIBBS``, ``GeotechEng.BAZARAA``,
            ``GeotechEng.PECK``, ``GeotechEng.LIAO``, and ``GeotechEng.SKEMPTON``
        """
        if eng is GeotechEng.GIBBS:
            corrected_spt = self.gibbs_holtz_opc_1957(recorded_spt_nval, eop)

        elif eng is GeotechEng.BAZARAA:
            corrected_spt = self.bazaraa_peck_opc_1969(recorded_spt_nval, eop)

        elif eng is GeotechEng.PECK:
            corrected_spt = self.peck_et_al_opc_1974(recorded_spt_nval, eop)

        elif eng is GeotechEng.LIAO:
            corrected_spt = self.liao_whitman_opc_1986(recorded_spt_nval, eop)

        elif eng is GeotechEng.SKEMPTON:
            corrected_spt = self.skempton_opc_1986(recorded_spt_nval, eop)

        else:
            msg = f"{eng} is not a valid type for overburden pressure spt correction"
            raise TypeError(msg)

        return corrected_spt
