import unittest

from geolysis.core.foundation import (
    CircularFooting,
    FoundationSize,
    Shape,
    SquareFooting,
    create_foundation,
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
        fs = create_foundation(
            depth=1.5, width=1.2, footing_shape=Shape.SQUARE
        )
        fs = FoundationSize(depth=1.5, footing_shape=fs)

        fs.width = 1.4
        self.assertAlmostEqual(fs.width, 1.4)

        fs.length = 1.5
        self.assertAlmostEqual(fs.length, 1.5)

        footing_shape = CircularFooting(diameter=1.5)
        fs.footing_shape = footing_shape
        self.assertEqual(fs.footing_shape, CircularFooting(diameter=1.5))
