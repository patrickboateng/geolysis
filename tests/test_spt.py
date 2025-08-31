import pytest
from func_validator import ValidationError

from geolysis.spt import (
    DilatancyCorrection,
    EnergyCorrection,
    HammerType,
    SamplerType,
    SPT,
    create_overburden_pressure_correction,
)


def test_create_spt_correction_errors():
    with pytest.raises(ValidationError):
        create_overburden_pressure_correction(
            std_spt_n_value=34, eop=100, opc_type="TERZAGHI"
        )


class TestSPTNDesign:

    def test_spt_n_design(self):
        spt_design = SPT([7.0, 15.0, 18], method="min")

        assert spt_design.n_design() == pytest.approx(7.0)
        spt_design.method = "avg"
        assert spt_design.n_design() == pytest.approx(13.3)
        spt_design.method = "wgt"
        assert spt_design.n_design() == pytest.approx(9.4)

    def test_errors(self):
        # Provided an empty value for corrected_spt_n_values
        with pytest.raises(ValidationError):
            SPT(corrected_spt_n_values=[])

        # Provided an invalid method
        with pytest.raises(ValidationError):
            SPT(corrected_spt_n_values=[7.0, 15.0, 18], method="max")

        # corrected_spt_n_values is greater than 100
        with pytest.raises(ValidationError):
            SPT(corrected_spt_n_values=[22, 44, 120])

        # corrected_spt_n_values is 0.0
        with pytest.raises(ValidationError):
            SPT(corrected_spt_n_values=[0.0, 15.0, 18])

        # corrected_spt_n_values is less than 0.0
        with pytest.raises(ValidationError):
            SPT(corrected_spt_n_values=[-10, 15.0, 18])


class TestEnergyCorrection:

    @pytest.mark.parametrize(
        [
            "rec_spt_n_val",
            "energy_percentage",
            "borehole_diameter",
            "rod_len",
            "hammer_type",
            "sampler_type",
            "expected",
        ],
        [
            (30, 0.6, 65.0, 3, HammerType.DONUT_1, SamplerType.STANDARD, 22.5),
            (30, 0.6, 120.0, 5, HammerType.AUTOMATIC, SamplerType.NON_STANDARD, 37.5),
            (30, 0.6, 170.0, 7, HammerType.DONUT_2, SamplerType.STANDARD, 27.3),
            (30, 0.6, 65.0, 12, HammerType.SAFETY, SamplerType.STANDARD, 27.5),
        ],
    )
    def test_energy_correction(
        self,
        rec_spt_n_val,
        energy_percentage,
        borehole_diameter,
        rod_len,
        hammer_type,
        sampler_type,
        expected,
    ):
        energy_corr = EnergyCorrection(
            recorded_spt_n_value=rec_spt_n_val,
            energy_percentage=energy_percentage,
            borehole_diameter=borehole_diameter,
            rod_length=rod_len,
            hammer_type=hammer_type,
            sampler_type=sampler_type,
        )

        assert energy_corr.standardized_spt_n_value() == pytest.approx(expected)

    def test_errors(self):
        # Provided an invalid value for hammer_type
        with pytest.raises(ValidationError):
            EnergyCorrection(recorded_spt_n_value=22, hammer_type="manual")

        # Provided an invalid value for sampler_type
        with pytest.raises(ValidationError):
            EnergyCorrection(recorded_spt_n_value=22, sampler_type="std")


class TestGibbsHoltzOPC:

    @pytest.mark.parametrize(
        ["std_spt_n_value", "eop", "expected"], [(22.5, 100.0, 23.2)]
    )
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = create_overburden_pressure_correction(
            std_spt_n_value=std_spt_n_value, eop=eop, opc_type="gibbs"
        )
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestBazaraaPeckOPC:

    @pytest.mark.parametrize(
        ["std_spt_n_value", "eop", "expected"],
        [(11.4, 54.8, 13.9), (22.5, 100.0, 21.0), (22.5, 71.8, 22.5)],
    )
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = create_overburden_pressure_correction(
            std_spt_n_value=std_spt_n_value, eop=eop, opc_type="bazaraa"
        )
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestPeckOPC:

    @pytest.mark.parametrize(
        ["std_spt_n_value", "eop", "expected"], [(22.5, 100.0, 22.5)]
    )
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = create_overburden_pressure_correction(
            std_spt_n_value=std_spt_n_value, eop=eop, opc_type="peck"
        )
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestLiaoWhitmanOPC:

    @pytest.mark.parametrize(
        ["std_spt_n_value", "eop", "expected"], [(22.5, 100.0, 22.5)]
    )
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = create_overburden_pressure_correction(
            std_spt_n_value=std_spt_n_value, eop=eop, opc_type="liao"
        )
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestSkemptonOPC:
    @pytest.mark.parametrize(
        ["std_spt_n_value", "eop", "expected"], [(22.5, 100.0, 22.0)]
    )
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = create_overburden_pressure_correction(
            std_spt_n_value=std_spt_n_value, eop=eop, opc_type="skempton"
        )
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestDilatancyCorrection:

    @pytest.mark.parametrize(
        ["std_spt_n_value", "expected"], [(22.5, 18.8), (12.6, 12.6)]
    )
    def test_correction(self, std_spt_n_value, expected):
        corr = DilatancyCorrection(corr_spt_n_value=std_spt_n_value)
        assert corr.corrected_spt_n_value() == pytest.approx(expected)
