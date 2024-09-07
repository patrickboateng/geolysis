import pytest

from geolysis.core import UnitSystem, reset_option, set_option


@pytest.fixture(scope="session")
def configure():
    set_option("unit_system", UnitSystem.SI)
    yield
    reset_option("unit_system")
