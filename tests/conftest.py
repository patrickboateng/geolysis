import csv
import pathlib

import pytest

TEST_DATA = pathlib.Path(__file__).parent / "test_data.csv"


@pytest.fixture(scope="session")
def soils_():
    f = open(TEST_DATA, "r")
    soils = csv.reader(f)
    next(soils)

    soil_single_classification = []
    soil_dual_classification = []

    for soil_data in soils:
        if len(soil_data[-1].strip()) == 2:  # check classification type
            soil_single_classification.append(soil_data)
        else:
            soil_dual_classification.append(soil_data)

    yield soil_single_classification, soil_dual_classification

    f.close()
