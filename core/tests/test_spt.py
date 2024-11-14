import unittest

from geolysis.spt import (
    BazaraaPeckOPC,
    DilatancyCorrection,
    GibbsHoltzOPC,
    LiaoWhitmanOPC,
    PeckOPC,
)


class TestGibbsHoltzOPC(unittest.TestCase):
    def testErrors(self):
        with self.assertRaises(ValueError):
            GibbsHoltzOPC(std_spt_number=15.4, eop=0.0)

        with self.assertRaises(ValueError):
            GibbsHoltzOPC(std_spt_number=11.0, eop=300.0)


class TestBazaraaPeckOPC(unittest.TestCase):
    def testCorrection(self):
        cor = BazaraaPeckOPC(std_spt_number=11.4, eop=54.8)
        self.assertAlmostEqual(cor.corrected_spt_number(), 13.9)


class TestPeckOPC(unittest.TestCase):
    def testErrors(self):
        with self.assertRaises(ValueError):
            PeckOPC(std_spt_number=12.8, eop=15.8)


class TestLiaoWhitmanOPC(unittest.TestCase):
    def testErrors(self):
        with self.assertRaises(ValueError):
            LiaoWhitmanOPC(std_spt_number=16.7, eop=0.0)


class TestDilatancyCorrection(unittest.TestCase):
    def testCorrectedSPTNumber(self):
        cor = DilatancyCorrection(std_spt_number=12.6)
        self.assertAlmostEqual(cor.corrected_spt_number(), 12.6)
