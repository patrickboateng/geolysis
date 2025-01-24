from typing import TypeAlias

from geolysis.bearing_capacity.abc.cohl import \
    create_allowable_bearing_capacity
from geolysis.foundation import FoundationSize, Shape
from geolysis.utils import isclose

FndParams: TypeAlias = tuple[float, float, Shape]


def get_footing_params(foundation_size: FoundationSize) -> FndParams:
    """Returns the ``width``, ``length``, and ``shape`` of the
    foundation footing.

    .. note:: "width" is the effective width of the foundation footing.
    """
    width = foundation_size.effective_width
    length = foundation_size.length
    shape = foundation_size.footing_shape

    if not isclose(width, length) and shape != Shape.STRIP:
        shape = Shape.RECTANGLE

    return width, length, shape
