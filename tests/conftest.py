import csv
import pathlib

import pytest

TEST_DATA = pathlib.Path(__file__).parent / "test_data.csv"


def soil_infos():
    with open(TEST_DATA, "r") as f:
        soil_info = csv.reader(f)
        next(soil_info)

        for soil_data in soil_info:
            classification = soil_data.pop()
            if len(classification) > 2:
                continue

            soil_data = [
                float(i) for i in soil_data
            ]  # converting soil parameters to float
            yield (soil_data, classification)
