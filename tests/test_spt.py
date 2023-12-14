import pytest

from geolysis import ERROR_TOLERANCE, GeotechEng
from geolysis.bearing_capacity.spt import SPTCorrections, n_design
from geolysis.exceptions import EngineerTypeError


def test_n_design():
    assert n_design([7.0, 15.0, 18.0]) == pytest.approx(9.37, ERROR_TOLERANCE)
    assert n_design([7.0, 15.0, 18.0], t=True) == pytest.approx(
        7.0, ERROR_TOLERANCE
    )
    assert n_design([]) == 0.0


class TestSPTCorrections:
    @classmethod
    def setup_class(cls):
        cls.spt_correction = SPTCorrections(
            hammer_efficiency=0.6,
            borehole_diameter_correction=1,
            sampler_correction=1,
            rod_length_correction=0.85,
        )

    @pytest.mark.parametrize(
        ("recorded_spt_nval", "n60"),
        ((15, 12.75), (8, 6.8), (7, 5.95), (26, 22.1)),
    )
    def test_spt_n60(self, recorded_spt_nval, n60):
        assert self.spt_correction.spt_n60(recorded_spt_nval) == pytest.approx(
            n60, ERROR_TOLERANCE
        )

    def test_dilatancy_correction(self):
        assert self.spt_correction.dilatancy_correction(
            recorded_spt_nval=15
        ) == pytest.approx(12.75, ERROR_TOLERANCE)

        assert self.spt_correction.dilatancy_correction(
            recorded_spt_nval=30
        ) == pytest.approx(20.25, ERROR_TOLERANCE)

    def test_overburden_pressure(self):
        # Gibbs and Holtz (1957)
        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.GIBBS
        ) == pytest.approx(12.84, ERROR_TOLERANCE)

        with pytest.raises(ValueError):
            self.spt_correction.overburden_pressure_correction(
                recorded_spt_nval=15, eop=300, eng=GeotechEng.GIBBS
            )

        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=200, eng=GeotechEng.GIBBS
        ) == pytest.approx(16.53, ERROR_TOLERANCE)

        # Peck et al (1974)
        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.PECK
        ) == pytest.approx(12.61, ERROR_TOLERANCE)

        with pytest.raises(ValueError):
            self.spt_correction.overburden_pressure_correction(
                recorded_spt_nval=15, eop=20, eng=GeotechEng.PECK
            )

        # Liao and Whitman (1986)
        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.LIAO
        ) == pytest.approx(12.51, ERROR_TOLERANCE)

        # Skempton (1986)
        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.SKEMPTON
        ) == pytest.approx(12.24, ERROR_TOLERANCE)

        # Bazaraa and Peck (1969)
        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=71.8, eng=GeotechEng.BAZARAA
        ) == pytest.approx(12.75, ERROR_TOLERANCE)

        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=60.8, eng=GeotechEng.BAZARAA
        ) == pytest.approx(14.4, ERROR_TOLERANCE)

        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.BAZARAA
        ) == pytest.approx(11.78, ERROR_TOLERANCE)

        with pytest.raises(EngineerTypeError):
            self.spt_correction.overburden_pressure_correction(
                recorded_spt_nval=15, eop=103.8, eng=GeotechEng.KULLHAWY
            )
