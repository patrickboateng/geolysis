import unittest

from geolysis.core.bearing_capacity.abc_4_cohl_soils import (
    BowlesABC,
    MeyerhofABC,
    SettlementError,
    TerzaghiABC,
)
from geolysis.core.foundation import Shape, create_foundation


class TestBowlesABC(unittest.TestCase):

    def setUp(self) -> None:
        self.foundation_size = create_foundation(
            depth=1.5, thickness=0.3, width=1.4, footing_shape=Shape.SQUARE
        )
        return super().setUp()

    def testABC(self):

        bowles_abc = BowlesABC(
            corrected_spt_number=17.0,
            tol_settlement=20.0,
            foundation_size=self.foundation_size,
        )
        abc = bowles_abc.abc_4_pad_foundation()
        self.assertAlmostEqual(abc, 316.2891)

    def testSettlementError(self):
        with self.assertRaises(SettlementError):
            BowlesABC(
                corrected_spt_number=11.0,
                tol_settlement=30.0,
                foundation_size=self.foundation_size,
            )


class TestMeyerhofABC(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation_size = create_foundation(
            depth=1.5, thickness=0.3, width=1.4, footing_shape=Shape.SQUARE
        )

    def testABC(self):

        meyerhof_abc = MeyerhofABC(
            corrected_spt_number=17.0,
            tol_settlement=20.0,
            foundation_size=self.foundation_size,
        )
        abc = meyerhof_abc.abc_4_pad_foundation()
        self.assertAlmostEqual(abc, 211.2114)

    def testSettlementError(self):
        with self.assertRaises(SettlementError):
            MeyerhofABC(
                corrected_spt_number=11.0,
                tol_settlement=30.0,
                foundation_size=self.foundation_size,
            )


class TestTerzaghiABC(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation_size = create_foundation(
            depth=1.5, thickness=0.3, width=1.4, footing_shape=Shape.SQUARE
        )

    def testABC(self):

        terzaghi_abc = TerzaghiABC(
            corrected_spt_number=17,
            tol_settlement=20.0,
            water_depth=1.7,
            foundation_size=self.foundation_size,
        )
        abc = terzaghi_abc.abc_4_pad_foundation()
        self.assertAlmostEqual(abc, 91.2086)

    def testSettlementError(self):
        with self.assertRaises(SettlementError):
            TerzaghiABC(
                corrected_spt_number=11.0,
                tol_settlement=30.0,
                water_depth=1.8,
                foundation_size=self.foundation_size,
            )
