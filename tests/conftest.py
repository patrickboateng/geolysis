import pytest

from typing import Tuple

@pytest.fixture
def strings() -> Tuple[str, str, str]:
    return (
        "Whatever string",
        "Shout Bamalama!",
        "Sing a song about statistical models.", 
    )

