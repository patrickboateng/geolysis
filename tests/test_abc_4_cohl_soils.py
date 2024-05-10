import unittest

from geolysis.bearing_capacity.abc_4_cohl_soils import (
    BowlesABC,
    MeyerhofABC,
    TerzaghiABC,
)
from geolysis.foundation import Shape, create_foundation


class TestBowlesABC(unittest.TestCase):

    def testABC(self):
        foundation_size = create_foundation(
            depth=1.5, thickness=0.3, width=1.4, footing_shape=Shape.SQUARE
        )
        bowles_abc = BowlesABC(
            corrected_spt_number=17.0,
            tol_settlement=20.0,
            foundation_size=foundation_size,
        )
        abc = bowles_abc.abc_4_pad_foundation()
        self.assertAlmostEqual(abc, 316.2891)


class TestMeyerhofABC(unittest.TestCase):
    def testABC(self):
        foundation_size = create_foundation(
            depth=1.5, thickness=0.3, width=1.4, footing_shape=Shape.SQUARE
        )
        meyerhof_abc = MeyerhofABC(
            corrected_spt_number=17.0,
            tol_settlement=20.0,
            foundation_size=foundation_size,
        )
        abc = meyerhof_abc.abc_4_pad_foundation()
        self.assertAlmostEqual(abc, 211.2114)


class TestTerzaghiABC(unittest.TestCase):
    def testABC(self):
        foundation_size = create_foundation(
            depth=1.5, thickness=0.3, width=1.4, footing_shape=Shape.SQUARE
        )
        terzaghi_abc = TerzaghiABC(
            corrected_spt_number=17,
            tol_settlement=20.0,
            water_depth=1.7,
            foundation_size=foundation_size,
        )
        abc = terzaghi_abc.abc_4_pad_foundation()
        self.assertAlmostEqual(abc, 91.2086)
