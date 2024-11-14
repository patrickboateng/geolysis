import unittest

from src.foundation import CircularFooting, SquareFooting


class TestCircularFooting(unittest.TestCase):
    def testAttributes(self):
        circ_footing = CircularFooting(diameter=1.2)
        circ_footing.width = 1.4
        self.assertAlmostEqual(circ_footing.length, 1.4)
        self.assertAlmostEqual(circ_footing.diameter, 1.4)

        circ_footing.length = 1.5
        self.assertAlmostEqual(circ_footing.width, 1.5)
        self.assertAlmostEqual(circ_footing.diameter, 1.5)


class TestSquareFooting(unittest.TestCase):
    def testAttributes(self):
        sqr_footing = SquareFooting(1.2)
        sqr_footing.length = 1.4
        self.assertAlmostEqual(sqr_footing.width, 1.4)
