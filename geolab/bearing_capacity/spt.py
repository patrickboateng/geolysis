"""
This module provides classes for SPT Data Analysis.
"""
from typing import Iterable

from geolab import ERROR_TOLERANCE, GeotechEng
from geolab.utils import isclose, log10, prod, round_, sqrt


class SPTCorrections:
    r"""
    Standard Penetration Test N-value correction for **Overburden Pressure**
    and **Dilatancy**.

    The available overburden pressure corrections are :py:meth:`skempton_opc_1986`,
    :py:meth:`bazaraa_peck_opc_1969`, :py:meth:`gibbs_holtz_opc_1957`,
    :py:meth:`peck_et_al_opc_1974`, and :py:meth:`liao_whitman_opc_1986`.

    :param hammer_efficiency: hammer efficiency, defaults to 0.6
    :type hammer_efficiency: float, optional
    :param borehole_diameter_correction: borehole diameter correction, defaults to 1.0
    :type borehole_diameter_correction: float, optional
    :param sampler_correction: sampler correction, defaults to 1.0
    :type sampler_correction: float, optional
    :param rod_length_correction: rod Length correction, defaults to 0.75
    :type rod_length_correction: float
    :param eop: effective overburden pressure :math:`kN/m^2`
    :type eop: float
    :param eng: specifies the type of overburden pressure correction formula to use.
                Available values are ``GeotechEng.GIBBS``, ``GeotechEng.BAZARAA``,
                ``GeotechEng.PECK``, ``GeotechEng.LIAO``, and ``GeotechEng.SKEMPTON``
    :type eng: GeotechEng

    :raises exceptions.EngineerTypeError: if eng specified is not valid
    """

    def __init__(
        self,
        *,
        hammer_efficiency: float = 0.6,
        borehole_diameter_correction: float = 1.0,
        sampler_correction: float = 1.0,
        rod_length_correction: float = 0.75,
        eop: float = 0.0,
        eng: GeotechEng = GeotechEng.SKEMPTON,
    ):
        self.hammer_efficiency = hammer_efficiency
        self.borehole_diameter_correction = borehole_diameter_correction
        self.sampler_correction = sampler_correction
        self.rod_length_correction = rod_length_correction
        self.eop = eop
        self.eng = eng

    @round_(precision=2)
    def n_design(self, corrected_spt_nvalues: Iterable[float]) -> float:
        r"""
        Returns the weighted average of the corrected SPT N-values in the
        foundation influence zone.

        influence zone = :math:`D_f + 2B` or to a depth up to which soil types
        are approximately the same.

        B = width of foundation

        .. math::

            N_{design} = \dfrac{\sum_{i=1}^{n} \frac{N_i}{i^2}}{\sum_{i=1}^{n} \frac{1}{i^2}}

        - :math:`n \rightarrow` number of layers in the influence zone.
        - :math:`N_i \rightarrow` corrected N-value at ith layer from the footing base.

        .. note::

            Alternatively, for ease in calculation, the lowest N-value from the influence
            zone can be taken as the :math:`N_{design}` as suggested by ``Terzaghi & Peck (1948)``.

        :param corrected_spt_nvalues: Corrected SPT N-values
        :type corrected_spt_nvalues: Iterable[float]
        """

        if not len(corrected_spt_nvalues):  # type: ignore
            return 0.0

        total = 0.0
        total_weights = 0.0

        for idx, corrected_spt_nvalue in enumerate(
            corrected_spt_nvalues, start=1
        ):
            idx_weight = 1 / idx**2
            total += idx_weight * corrected_spt_nvalue
            total_weights += idx_weight

        _n_design = total / total_weights

        return _n_design

    def skempton_opc_1986(self, spt_n60: float) -> float:
        corr_spt = (2 / (1 + 0.01044 * self.eop)) * spt_n60
        return self._opc(corr_spt, spt_n60)

    def bazaraa_peck_opc_1969(self, spt_n60: float) -> float:
        corr_spt: float  # corrected spt n-value

        std_pressure = 71.8

        if isclose(self.eop, std_pressure, rel_tol=ERROR_TOLERANCE):
            corr_spt = spt_n60

        elif self.eop < std_pressure:
            corr_spt = 4 * spt_n60 / (1 + 0.0418 * self.eop)

        else:
            corr_spt = 4 * spt_n60 / (3.25 + 0.0104 * self.eop)

        return self._opc(corr_spt, spt_n60)

    def gibbs_holtz_opc_1957(self, spt_n60: float) -> float:
        corr_spt: float

        std_pressure = 280

        if self.eop > std_pressure:
            msg = f"{self.eop} should be less than or equal to {std_pressure}"
            raise ValueError(msg)

        corr_spt = spt_n60 * (350 / (self.eop + 70))
        spt_ratio = corr_spt / spt_n60

        if 0.45 < spt_ratio < 2.0:
            return corr_spt

        corr_spt = corr_spt / 2 if spt_ratio > 2.0 else corr_spt

        return self._opc(corr_spt, spt_n60)

    def peck_et_al_opc_1974(self, spt_n60: float) -> float:
        std_pressure = 24

        if self.eop < std_pressure:
            msg = (
                f"{self.eop} should be greater than or equal to {std_pressure}"
            )
            raise ValueError(msg)

        corr_spt = 0.77 * log10(1905 / self.eop) * spt_n60

        return self._opc(corr_spt, spt_n60)

    def liao_whitman_opc_1986(self, spt_n60) -> float:
        corr_spt = sqrt(100 / self.eop) * spt_n60
        return self._opc(corr_spt, spt_n60)

    def spt_n60(self, recorded_spt_nvalue: int) -> float:
        """
        Return SPT N-value corrected for 60% hammer efficiency.
        """
        correction = prod(
            self.hammer_efficiency,
            self.borehole_diameter_correction,
            self.sampler_correction,
            self.rod_length_correction,
        )

        return (correction * recorded_spt_nvalue) / 0.6

    def dilatancy(self, recorded_spt_nvalue: int) -> float:
        """
        Returns the dilatancy spt correction.
        """

        dsc: float  # dilatancy spt correction

        spt_n60 = self.spt_n60(recorded_spt_nvalue)

        if spt_n60 <= 15:
            dsc = spt_n60
        else:
            dsc = 15 + 0.5 * (spt_n60 - 15)

        return dsc

    def overburden_pressure(self, recorded_spt_nvalue: int) -> float:
        """
        Returns the overburden pressure spt correction.
        """
        opc: float
        spt_n60 = self.spt_n60(recorded_spt_nvalue)

        if self.eng is GeotechEng.GIBBS:
            opc = self.gibbs_holtz_opc_1957(spt_n60)

        elif self.eng is GeotechEng.BAZARAA:
            opc = self.bazaraa_peck_opc_1969(spt_n60)

        elif self.eng is GeotechEng.WOLFF:
            opc = self.peck_et_al_opc_1974(spt_n60)

        elif self.eng is GeotechEng.LIAO:
            opc = self.liao_whitman_opc_1986(spt_n60)

        elif self.eng is GeotechEng.SKEMPTON:
            opc = self.skempton_opc_1986(spt_n60)

        else:
            msg = f"{self.eng} is not a valid type for overburden pressure spt correction"
            raise TypeError(msg)

        return opc

    @staticmethod
    def _opc(corr_spt: float, spt_n60: float) -> float:
        return corr_spt if corr_spt <= (expr := 2 * spt_n60) else expr
