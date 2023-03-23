import csv
import pathlib

import pytest

TEST_DATA = pathlib.Path(__file__).parent / "test_data.csv"


single_classification = []
dual_classification = []


@pytest.fixture(scope="session")
def soil_infos():
    f = open(TEST_DATA, "r")
    soil_info = csv.reader(f)
    next(soil_info)

    for soil_data in soil_info:
        if len(soil_data[-1].strip()) == 2:  # check classification type
            single_classification.append(soil_data)
        else:
            dual_classification.append(soil_data)

    yield

    f.close()
