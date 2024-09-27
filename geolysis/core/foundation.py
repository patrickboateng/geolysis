import enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Protocol

from geolysis.core.utils import INF

__all__ = ["create_foundation"]


class FootingCreationError(TypeError):
    pass


class Shape(enum.StrEnum):
    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


class _FootingShape(Protocol):
    type_: Shape

    @property
    @abstractmethod
    def width(self) -> float: ...

    @width.setter
    def width(self, __val: float): ...

    @property
    @abstractmethod
    def length(self) -> float: ...

    @length.setter
    def length(self, __val: float): ...


@dataclass
class StripFooting:
    width: float
    length: float = INF
    type_ = Shape.STRIP


@dataclass
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

    diameter: float
    type_ = Shape.CIRCLE

    @property
    def width(self) -> float:
        """Diameter of foundation footing."""
        return self.diameter

    @width.setter
    def width(self, __val: float):
        self.diameter = __val

    @property
    def length(self) -> float:
        """Diameter of foundation footing."""
        return self.diameter

    @length.setter
    def length(self, __val: float):
        self.diameter = __val


@dataclass
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

    width: float
    type_ = Shape.SQUARE

    @property
    def length(self) -> float:
        """Length of foundation footing."""
        return self.width

    @length.setter
    def length(self, __val: float):
        self.width = __val


@dataclass
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

    width: float
    length: float
    type_ = Shape.RECTANGLE


@dataclass
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

    depth: float
    footing_shape: _FootingShape
    eccentricity: float = 0.0

    @property
    def width(self) -> float:
        """Width of foundation footing."""
        return self.footing_shape.width

    @width.setter
    def width(self, __val: float):
        self.footing_shape.width = __val

    @property
    def effective_width(self) -> float:
        return self.width - 2 * self.eccentricity

    @property
    def length(self) -> float:
        """Length of foundation footing."""
        return self.footing_shape.length

    @length.setter
    def length(self, __val: float):
        self.footing_shape.length = __val

    @property
    def footing_type(self) -> Shape:
        return self.footing_shape.type_


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

    match footing_shape:
        case Shape.STRIP:
            _footing_shape = StripFooting(width=width)
        case Shape.SQUARE:
            _footing_shape = SquareFooting(width=width)
        case Shape.CIRCLE:
            _footing_shape = CircularFooting(diameter=width)
        case Shape.RECTANGLE:
            if length:
                _footing_shape = RectangularFooting(width=width, length=length)
            else:
                err_msg = "The length of the footing must be provided"
                raise FootingCreationError(err_msg)
        case _:
            err_msg = (
                "Supported footing shapes are SQUARE, RECTANGLE, and CIRCLE"
            )
            raise FootingCreationError(err_msg)

    return FoundationSize(
        depth=depth,
        eccentricity=eccentricity,
        footing_shape=_footing_shape,
    )
