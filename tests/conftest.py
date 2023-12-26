import pytest

from geolysis.bearing_capacity import FoundationSize, SquareFooting


@pytest.fixture(scope="function")
def foundation_size():
    fs = SquareFooting(1.2)
    return FoundationSize(depth=1.5, footing_size=fs)
