import enum
from typing import Final, Optional, Protocol

import attrs
from attrs import field, validators

from geolysis.core.utils import INF, ref_field

# __all__ = ["create_foundation"]


class Shape(enum.StrEnum):
    """"""

    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


class FootingSize(Protocol):
    shape_: Shape
    width: float
    length: float


@attrs.define
class StripFooting(FootingSize):
    width: int | float = field(validator=validators.gt(0.0))
    length: int | float = field(default=INF, validator=validators.gt(0.0))
    shape_: Final[Shape] = field(default=Shape.STRIP, init=False)


@attrs.define
class CircularFooting(FootingSize):
    """A class representation of circular footing.

    :param float diameter: Diameter of foundation footing. (m)

    .. seealso::

        :class:`SquareFooting`, :class:`RectangularFooting`

    .. note::

        The ``width`` and ``length`` properties refer to the diameter
        of the circular footing. This is to make it compatible with the
        protocol square and rectangular footing follow.


    >>> from geolysis.core.foundation import CircularFooting
    >>> circ_footing = CircularFooting(diameter=1.2)
    >>> circ_footing.diameter
    1.2
    >>> circ_footing.width
    1.2
    >>> circ_footing.length
    1.2
    """

    diameter: int | float = field(validator=validators.gt(0.0))
    shape_: Final[Shape] = field(default=Shape.CIRCLE, init=False)

    width = ref_field(ref_attr="diameter", doc="Diameter of footing.")  # type: ignore
    length = ref_field(ref_attr="diameter", doc="Diameter of footing.")  # type: ignore


@attrs.define
class SquareFooting(FootingSize):
    """A class representation of square footing.

    :param float width: Width of foundation footing. (m)

    .. seealso::

        :class:`CircularFooting`, :class:`RectangularFooting`

    .. code::

        >>> from geolysis.core.foundation import SquareFooting
        >>> sq_footing = SquareFooting(width=1.2)
        >>> sq_footing.width
        1.2
        >>> sq_footing.length
        1.2
    """

    width: int | float = field(validator=validators.gt(0.0))
    shape_: Final[Shape] = field(default=Shape.SQUARE, init=False)

    length = ref_field(ref_attr="width", doc="Width of footing. (m)")  # type: ignore


@attrs.define
class RectangularFooting(FootingSize):
    """A class representation of rectangular footing.

    :param float width: Width of foundation footing. (m)
    :param float length: Length of foundation footing. (m)

    .. seealso::

        :class:`CircularFooting`, :class:`SquareFooting`

    .. code::

        >>> from geolysis.core.foundation import RectangularFooting
        >>> rect_footing = RectangularFooting(width=1.2, length=1.4)
        >>> rect_footing.width
        1.2
        >>> rect_footing.length
        1.4
    """

    width: int | float = field(validator=validators.gt(0.0))
    length: int | float = field(validator=validators.gt(0.0))
    shape_: Final[Shape] = field(default=Shape.RECTANGLE, init=False)


@attrs.define
class FoundationSize:
    """A simple class representing a foundation structure.

    :param float depth: Depth of foundation. (m)
    :param FootingSize footing_size: Represents the size of the foundation
        footing.

    >>> from geolysis.core.foundation import (
    ...     FoundationSize,
    ...     CircularFooting,
    ...     Shape,
    ...     create_foundation,
    ... )
    >>> foundation_size = create_foundation(
    ...     depth=1.5, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> foundation_size.depth
    1.5
    >>> foundation_size.length
    1.2
    >>> foundation_size.width
    1.2
    """

    depth: int | float = field(validator=validators.gt(0.0))
    footing_size: FootingSize = field()
    eccentricity: int | float = field(
        default=0.0, validator=validators.ge(0.0)
    )

    width = ref_field(ref_attr="width", ref_obj="footing_size")
    length = ref_field(ref_attr="length", ref_obj="footing_size")
    footing_shape = ref_field(ref_attr="shape_", ref_obj="footing_size")

    @property
    def effective_width(self) -> float:
        return self.width - 2 * self.eccentricity


def create_foundation(
    depth: float,
    width: float,
    length: Optional[float] = None,
    eccentricity: float = 0.0,
    footing_shape: Shape | str = Shape.SQUARE,
) -> FoundationSize:
    """A factory function that encapsulate the creation of a foundation
    footing.

    :param float width: Width of foundation footing (m)
    :param float length: Length of foundation footing, defaults to None. (m)
    :param Shape | str footing_shape: Shape of foundation footing, defaults to
        :class:`Shape.SQUARE` or "square"

    :raises ValueError: Raised when length is not provided for a rectangular
        footing.
    :raises TypeError: Raised if an invalid footing shape is provided.

    :return: Size of foundation.
    :rtype: FoundationSize
    """
    if isinstance(footing_shape, str):
        footing_shape = footing_shape.casefold()

    if footing_shape == Shape.STRIP:
        footing_size = StripFooting(width=width)
    elif footing_shape == Shape.SQUARE:
        footing_size = SquareFooting(width=width)
    elif footing_shape == Shape.CIRCLE:
        footing_size = CircularFooting(diameter=width)
    elif footing_shape == Shape.RECTANGLE:
        if not length:
            raise ValueError("Length of footing must be provided.")
        footing_size = RectangularFooting(width=width, length=length)
    else:
        raise TypeError("Invalid footing shape.")

    return FoundationSize(
        depth=depth,
        eccentricity=eccentricity,
        footing_size=footing_size,
    )
