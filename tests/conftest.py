import pytest

from geolysis.bearing_capacity import FoundationSize


@pytest.fixture
def fs():
    return FoundationSize(
        foundation_depth=1.5,
        footing_length=1.2,
        footing_width=1.2,
    )
