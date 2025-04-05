import unittest

from geolysis.foundation import (CircularFooting, FoundationSize,
                                 RectangularFooting, Shape, SquareFooting,
                                 StripFooting, create_foundation)


class TestCircularFooting(unittest.TestCase):
    def test_attributes(self):
        circ_footing = CircularFooting(diameter=1.2)
        circ_footing.width = 1.4
        self.assertAlmostEqual(circ_footing.length, 1.4)
        self.assertAlmostEqual(circ_footing.diameter, 1.4)

        circ_footing.length = 1.5
        self.assertAlmostEqual(circ_footing.width, 1.5)
        self.assertAlmostEqual(circ_footing.diameter, 1.5)


class TestSquareFooting(unittest.TestCase):
    def test_attributes(self):
        sqr_footing = SquareFooting(1.2)
        sqr_footing.length = 1.4
        self.assertAlmostEqual(sqr_footing.width, 1.4)


class TestFoundation(unittest.TestCase):

    def test_strip_footing(self):
        footing = StripFooting(width=2.0)
        self.assertEqual(footing.width, 2.0)
        self.assertEqual(footing.length, float('inf'))
        self.assertEqual(footing.shape, Shape.STRIP)

    def test_circular_footing(self):
        footing = CircularFooting(diameter=3.0)
        self.assertEqual(footing.diameter, 3.0)
        self.assertEqual(footing.width, 3.0)
        self.assertEqual(footing.length, 3.0)
        self.assertEqual(footing.shape, Shape.CIRCLE)

    def test_square_footing(self):
        footing = SquareFooting(width=2.5)
        self.assertEqual(footing.width, 2.5)
        self.assertEqual(footing.length, 2.5)
        self.assertEqual(footing.shape, Shape.SQUARE)

    def test_rectangular_footing(self):
        footing = RectangularFooting(width=2.0, length=3.0)
        self.assertEqual(footing.width, 2.0)
        self.assertEqual(footing.length, 3.0)
        self.assertEqual(footing.shape, Shape.RECTANGLE)

    def test_foundation_size(self):
        footing = StripFooting(width=2.0)
        foundation = FoundationSize(depth=1.5,
                                    footing_size=footing,
                                    eccentricity=0.1)
        self.assertEqual(foundation.depth, 1.5)
        self.assertEqual(foundation.width, 2.0)
        self.assertEqual(foundation.length, float('inf'))
        self.assertEqual(foundation.eccentricity, 0.1)
        self.assertEqual(foundation.effective_width, 1.8)
        self.assertEqual(foundation.footing_shape, Shape.STRIP)

        foundation.width = 1.4
        foundation.length = 1.5
        foundation.ground_water_level = 1.8

        self.assertEqual(foundation.width, 1.4)
        self.assertEqual(foundation.length, 1.5)
        self.assertEqual(foundation.ground_water_level, 1.8)

    def test_create_foundation_strip(self):
        foundation = create_foundation(depth=1.5, width=2.0, shape=Shape.STRIP)
        self.assertEqual(foundation.depth, 1.5)
        self.assertEqual(foundation.width, 2.0)
        self.assertEqual(foundation.length, float('inf'))
        self.assertEqual(foundation.footing_shape, Shape.STRIP)

    def test_create_foundation_square(self):
        foundation = create_foundation(depth=1.5,
                                       width=2.5,
                                       shape=Shape.SQUARE)
        self.assertEqual(foundation.depth, 1.5)
        self.assertEqual(foundation.width, 2.5)
        self.assertEqual(foundation.length, 2.5)
        self.assertEqual(foundation.footing_shape, Shape.SQUARE)

    def test_create_foundation_circle(self):
        foundation = create_foundation(depth=1.5,
                                       width=3.0,
                                       shape=Shape.CIRCLE)
        self.assertEqual(foundation.depth, 1.5)
        self.assertEqual(foundation.width, 3.0)
        self.assertEqual(foundation.length, 3.0)
        self.assertEqual(foundation.footing_shape, Shape.CIRCLE)

    def test_create_foundation_rectangle(self):
        foundation = create_foundation(depth=1.5,
                                       width=2.0,
                                       length=3.0,
                                       shape=Shape.RECTANGLE)
        self.assertEqual(foundation.depth, 1.5)
        self.assertEqual(foundation.width, 2.0)
        self.assertEqual(foundation.length, 3.0)
        self.assertEqual(foundation.footing_shape, Shape.RECTANGLE)

    def test_create_foundation_invalid_shape(self):
        with self.assertRaises(ValueError):
            create_foundation(depth=1.5, width=2.0, shape="invalid_shape")

    def test_create_foundation_missing_length(self):
        with self.assertRaises(ValueError):
            create_foundation(depth=1.5, width=2.0, shape=Shape.RECTANGLE)
