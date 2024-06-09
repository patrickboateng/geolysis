import pytest

from geolysis.core.constants import ERROR_TOL
from geolysis.core.ubc import TerzaghiBCF


class TestTerzaghiBCF:

    @pytest.mark.parametrize(
        ("arg, r_value"), ((0, 5.70), (10, 9.61), (20, 17.69))
    )
    def test_n_c(self, arg, r_value):
        t_bcf = TerzaghiBCF(arg)

        assert t_bcf.n_c == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("arg, r_value"), ((0, 1.00), (10, 2.69), (20, 7.44))
    )
    def test_n_q(self, arg, r_value):
        t_bcf = TerzaghiBCF(arg)
        assert t_bcf.n_q == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("arg, r_value"), ((0, 0.00), (10, 0.42), (20, 3.42))
    )
    def test_n_gamma(self, arg, r_value):
        t_bcf = TerzaghiBCF(arg)
        assert t_bcf.n_gamma == pytest.approx(r_value, ERROR_TOL)
