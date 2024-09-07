import unittest

from geolysis.core.spt import (
    BazaraaPeckOPC,
    DilatancyCorrection,
    GibbsHoltzOPC,
    LiaoWhitmanOPC,
    OPCError,
    PeckOPC,
)


class TestGibbsHoltzOPC(unittest.TestCase):
    def testErrors(self):
        with self.assertRaises(OPCError):
            GibbsHoltzOPC(std_spt_number=15.4, eop=0)

        with self.assertRaises(OPCError):
            GibbsHoltzOPC(std_spt_number=11.0, eop=300)


class TestBazaraaPeckOPC(unittest.TestCase):
    def testCorrection(self):
        cor = BazaraaPeckOPC(std_spt_number=11.4, eop=71.8)
        self.assertEqual(cor.correction, 1.0)

        cor.eop = 54.8
        self.assertAlmostEqual(cor.correction, 1.2156)
        self.assertAlmostEqual(cor.corrected_spt_number, 13.8578)


class TestPeckOPC(unittest.TestCase):
    def testErrors(self):
        with self.assertRaises(OPCError):
            PeckOPC(std_spt_number=12.8, eop=15.8)


class TestLiaoWhitmanOPC(unittest.TestCase):
    def testErrors(self):
        with self.assertRaises(OPCError):
            LiaoWhitmanOPC(std_spt_number=16.7, eop=0.0)


class TestDilatancyCorrection(unittest.TestCase):
    def testCorrectedSPTNumber(self):
        cor = DilatancyCorrection(spt_number=12.6)
        self.assertAlmostEqual(cor.corrected_spt_number, 12.6)
