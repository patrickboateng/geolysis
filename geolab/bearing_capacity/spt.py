from typing import Iterable

from geolab import ERROR_TOLERANCE, GeotechEng
from geolab.utils import isclose, log10, mean, prod, sqrt


class spt_corrections:
    r"""SPT N-value Overburden Pressure and Dilatancy Correction.

    :param recorded_spt_nvalue: recorded SPT N-voalue (blows/300mm)
    :type recorded_spt_nvalue: int
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
                Available values are geolab.GIBBS, geolab.BAZARAA, geolab.PECK, geolab.LIAO,
                and geolab.SKEMPTON
    :type eng: GeotechEng
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

    def n_design(self, recorded_spt_nvalues: Iterable[int]) -> float:
        """"""
        spt_corrected_n60s = map(self.spt_n60, recorded_spt_nvalues)
        spt_corrected_vals = map(self.skempton_opc_1986, spt_corrected_n60s)

        return mean(spt_corrected_vals)

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
        """Return spt N-value corrected for 60% hammer efficiency."""
        correction = prod(
            self.hammer_efficiency,
            self.borehole_diameter_correction,
            self.sampler_correction,
            self.rod_length_correction,
        )

        return (correction * recorded_spt_nvalue) / 0.6

    def dilatancy(self, recorded_spt_nvalue: int) -> float:
        """Returns the dilatancy spt correction."""

        dsc: float  # dilatancy spt correction

        spt_n60 = self.spt_n60(recorded_spt_nvalue)

        if spt_n60 <= 15:
            dsc = spt_n60
        else:
            dsc = 15 + 0.5 * (spt_n60 - 15)

        return dsc

    def overburden_pressure(self, recorded_spt_nvalue: int) -> float:
        """Returns the overburden pressure spt correction."""
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
