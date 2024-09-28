import enum
from typing import Final, Optional, TypeAlias

import attrs

from geolysis.core.utils import INF, Number

__all__ = ["create_foundation"]


class FootingCreationError(TypeError):
    pass


class Shape(enum.StrEnum):
    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


validators: Final = [
    attrs.validators.instance_of((int, float)),
    attrs.validators.gt(0.0),
]


@attrs.define
class StripFooting:
    width: Number = attrs.field(validator=validators)
    length: Number = attrs.field(default=INF, validator=validators)

    shape_: Final[Shape] = attrs.field(
        default=Shape.STRIP, init=False, on_setattr=attrs.setters.frozen
    )


@attrs.define
class CircularFooting:
    """A class representation of circular footing.

    :param float diameter: Diameter of foundation footing. (m)

    .. seealso::

        :class:`SquareFooting`, :class:`RectangularFooting`

    Notes
    -----
    The ``width`` and ``length`` properties refer to the diameter
    of the circular footing. This is to make it compatible with the
    protocol square and rectangular footing follow.

    Examples
    --------
    >>> from geolysis.core.foundation import CircularFooting
    >>> circ_footing = CircularFooting(diameter=1.2)
    >>> circ_footing.diameter
    1.2
    >>> circ_footing.width
    1.2
    >>> circ_footing.length
    1.2
    """

    diameter: Number = attrs.field(validator=validators)
    shape_: Final[Shape] = attrs.field(
        default=Shape.CIRCLE, init=False, on_setattr=attrs.setters.frozen
    )

    @property
    def width(self) -> Number:
        """Diameter of foundation footing."""
        return self.diameter

    @width.setter
    def width(self, val: Number):
        self.diameter = val

    @property
    def length(self) -> Number:
        """Diameter of foundation footing."""
        return self.diameter

    @length.setter
    def length(self, val: Number):
        self.diameter = val


@attrs.define
class SquareFooting:
    """A class representation of square footing.

    :param float width: Width of foundation footing. (m)

    .. seealso::

        :class:`CircularFooting`, :class:`RectangularFooting`

    Examples
    --------
    >>> from geolysis.core.foundation import SquareFooting
    >>> sq_footing = SquareFooting(width=1.2)
    >>> sq_footing.width
    1.2
    >>> sq_footing.length
    1.2
    """

    width: Number = attrs.field(validator=validators)
    shape_: Final[Shape] = attrs.field(
        default=Shape.SQUARE, init=False, on_setattr=attrs.setters.frozen
    )

    @property
    def length(self) -> Number:
        """Length of foundation footing."""
        return self.width

    @length.setter
    def length(self, val: Number):
        self.width = val


@attrs.define
class RectangularFooting:
    """A class representation of rectangular footing.

    :param float width: Width of foundation footing. (m)
    :param float length: Length of foundation footing. (m)

    .. seealso::

        :class:`CircularFooting`, :class:`SquareFooting`

    Examples
    --------
    >>> from geolysis.core.foundation import RectangularFooting
    >>> rect_footing = RectangularFooting(width=1.2, length=1.4)
    >>> rect_footing.width
    1.2
    >>> rect_footing.length
    1.4
    """

    width: Number = attrs.field(validator=validators)
    length: Number = attrs.field(validator=validators)
    shape_: Final[Shape] = attrs.field(
        default=Shape.RECTANGLE,
        init=False,
        on_setattr=attrs.setters.frozen,
    )


_FootingSize: TypeAlias = (
    StripFooting | SquareFooting | CircularFooting | RectangularFooting
)


@attrs.define
class FoundationSize:
    """A simple class representing a foundation structure.

    :param float depth: Depth of foundation. (m)
    :param FootingSize footing_size: Represents the size of the foundation
        footing.

    .. seealso::

        :class:`FootingSize`

    Examples
    --------
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

    depth: Number = attrs.field(validator=validators)
    footing_size: _FootingSize = attrs.field()
    eccentricity: Number = attrs.field(
        default=0.0,
        validator=attrs.validators.ge(0.0),
    )

    @property
    def width(self) -> float:
        """Width of foundation footing."""
        return self.footing_size.width

    @width.setter
    def width(self, val: float):
        self.footing_size.width = val

    @property
    def effective_width(self) -> float:
        return self.width - 2 * self.eccentricity

    @property
    def length(self) -> float:
        """Length of foundation footing."""
        return self.footing_size.length

    @length.setter
    def length(self, val: float):
        self.footing_size.length = val

    @property
    def footing_shape(self) -> Shape:
        return self.footing_size.shape_


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

    :raises FootingCreationError: Exception raised when footing is not created
        successfully.

    :return: Size of foundation footing.
    :rtype: FootingSize

    Examples
    --------

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
        if length:
            footing_size = RectangularFooting(width=width, length=length)
        else:
            err_msg = "The length of the footing must be provided"
            raise FootingCreationError(err_msg)
    else:
        err_msg = "Supported footing shapes are SQUARE, RECTANGLE, and CIRCLE"
        raise FootingCreationError(err_msg)

    return FoundationSize(
        depth=depth,
        eccentricity=eccentricity,
        footing_size=footing_size,
    )
