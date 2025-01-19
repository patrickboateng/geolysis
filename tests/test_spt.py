import unittest

from geolysis.spt import (BazaraaPeckOPC, DilatancyCorrection, GibbsHoltzOPC,
                          LiaoWhitmanOPC, PeckOPC)


class TestGibbsHoltzOPC(unittest.TestCase):
    def test_errors(self):
        with self.assertRaises(ValueError):
            GibbsHoltzOPC(standardized_spt_value=15.4, eop=0.0)

        with self.assertRaises(ValueError):
            GibbsHoltzOPC(standardized_spt_value=11.0, eop=300.0)


class TestBazaraaPeckOPC(unittest.TestCase):
    def test_correction(self):
        cor = BazaraaPeckOPC(standardized_spt_value=11.4, eop=54.8)
        self.assertAlmostEqual(cor.corrected_spt_number(), 13.9)


class TestPeckOPC(unittest.TestCase):
    def test_errors(self):
        with self.assertRaises(ValueError):
            PeckOPC(standardized_spt_value=12.8, eop=15.8)


class TestLiaoWhitmanOPC(unittest.TestCase):
    def test_errors(self):
        with self.assertRaises(ValueError):
            LiaoWhitmanOPC(standardized_spt_value=16.7, eop=0.0)


class TestDilatancyCorrection(unittest.TestCase):
    def test_corrected_spt_number(self):
        cor = DilatancyCorrection(standardized_spt_value=12.6)
        self.assertAlmostEqual(cor.corrected_spt_number(), 12.6)
