import unittest

from geolysis.estimators import (
    EstimatorError,
    KullhawyMayneSoilFrictionAngle,
    StroudUndrainedShearStrength,
)


class TestKMSFA(unittest.TestCase):

    def testEstimatorError(self):
        with self.assertRaises(EstimatorError):
            KullhawyMayneSoilFrictionAngle(
                std_spt_number=15.0, eop=103.8, atm_pressure=0.0
            )


class TestSUSS(unittest.TestCase):

    def testEstimatorError(self):
        with self.assertRaises(EstimatorError):
            StroudUndrainedShearStrength(std_spt_number=10.0, k=7.0)
