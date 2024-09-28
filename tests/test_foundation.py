import unittest

from geolysis.core.foundation import (
    CircularFooting,
    FoundationSize,
    SquareFooting,
)


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


class TestFoundationSize(unittest.TestCase):
    def testAttributes(self):
        fs = FoundationSize(depth=1.5, footing_size=SquareFooting(width=1.2))

        fs.width = 1.4
        self.assertAlmostEqual(fs.width, 1.4)

        fs.length = 1.5
        self.assertAlmostEqual(fs.length, 1.5)

        footing_type = CircularFooting(diameter=1.5)
        fs.footing_size = footing_type
        self.assertEqual(fs.footing_size, CircularFooting(diameter=1.5))
