import math

from geolab import ERROR_TOLERANCE, GeotechEng
from geolab.utils import log10, mul, sqrt


class spt_corrections:
    r"""SPT N-value Overburden Pressure and Dilatancy Correction.



    :param recorded_spt_nvalue: recorded SPT N-value (blows/300mm)
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
        recorded_spt_nvalue: int,
        *,
        hammer_efficiency: float = 0.6,
        borehole_diameter_correction: float = 1.0,
        sampler_correction: float = 1.0,
        rod_length_correction: float = 0.75,
        eop: float = 0.0,
        eng: GeotechEng = GeotechEng.SKEMPTON,
    ):
        self.recorded_spt_nvalue = recorded_spt_nvalue
        self.hammer_efficiency = hammer_efficiency
        self.borehole_diameter_correction = borehole_diameter_correction
        self.sampler_correction = sampler_correction
        self.rod_length_correction = rod_length_correction
        self.eop = eop
        self.eng = eng

    def __call__(self, recorded_spt_nvalue: float = 0) -> float:
        if recorded_spt_nvalue:
            self.recorded_spt_nvalue = recorded_spt_nvalue

        return self.overburden_pressure_spt_correction()

    def _skempton_opc(self) -> float:
        return (2 / (1 + 0.01044 * self.eop)) * self.spt_n60

    def _bazaraa_opc(self) -> float:
        corr_spt: float  # corrected spt n-value

        std_pressure = 71.8

        if math.isclose(self.eop, std_pressure, rel_tol=ERROR_TOLERANCE):
            corr_spt = self.spt_n60

        elif self.eop < std_pressure:
            corr_spt = 4 * self.spt_n60 / (1 + 0.0418 * self.eop)

        else:
            corr_spt = 4 * self.spt_n60 / (3.25 + 0.0104 * self.eop)

        return corr_spt

    def _gibbs_holtz_opc(self) -> float:
        corr_spt: float

        std_pressure = 280

        if self.eop > std_pressure:
            msg = f"{self.eop} should be less than or equal to {std_pressure}"
            raise ValueError(msg)

        corr_spt = self.spt_n60 * (350 / (self.eop + 70))
        spt_ratio = corr_spt / self.spt_n60

        if 0.45 < spt_ratio < 2.0:
            return corr_spt

        return corr_spt / 2 if spt_ratio > 2.0 else corr_spt

    def _peck_opc(self) -> float:
        std_pressure = 24

        if self.eop < std_pressure:
            msg = (
                f"{self.eop} should be greater than or equal to {std_pressure}"
            )
            raise ValueError(msg)

        return 0.77 * log10(1905 / self.eop) * self.spt_n60

    def _liao_whitman_opc(self) -> float:
        return sqrt(100 / self.eop) * self.spt_n60

    @property
    def spt_n60(self) -> float:
        correction = mul(
            self.hammer_efficiency,
            self.borehole_diameter_correction,
            self.sampler_correction,
            self.rod_length_correction,
        )

        return (correction * self.recorded_spt_nvalue) / 0.6

    def dilatancy_spt_correction(self) -> float:
        """Returns the dilatancy spt correction."""
        return (
            self.spt_n60
            if self.spt_n60 <= 15
            else 15 + 0.5 * (self.spt_n60 - 15)
        )

    def overburden_pressure_spt_correction(self) -> float:
        """Returns the overburden pressure spt correction."""
        opc: float

        if self.eng is GeotechEng.GIBBS:
            opc = self._gibbs_holtz_opc()

        elif self.eng is GeotechEng.BAZARAA:
            opc = self._bazaraa_opc()

        elif self.eng is GeotechEng.PECK:
            opc = self._peck_opc()

        elif self.eng is GeotechEng.LIAO:
            opc = self._liao_whitman_opc()

        elif self.eng is GeotechEng.SKEMPTON:
            opc = self._skempton_opc()

        else:
            msg = f"{self.eng} is not a valid type for overburden pressure spt correction"
            raise TypeError(msg)

        return opc
