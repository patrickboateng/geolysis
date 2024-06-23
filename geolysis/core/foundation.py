import enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Protocol

__all__ = [
    "create_footing",
    "create_foundation",
    "Shape",
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
    "FootingSize",
    "FoundationSize",
]


class FootingCreationError(TypeError):
    pass


class Shape(enum.Enum):
    STRIP = "strip"
    CIRCLE = "circle"
    SQUARE = "square"
    RECTANGLE = "rectangle"

    def __eq__(self, other) -> bool:
        if isinstance(other, Shape):
            return super().__eq__(other)
        elif isinstance(other, str):
            return self.value == other
        else:
            return NotImplemented


class _FootingShape(Protocol):
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

    @property
    def length(self) -> float:
        """Width of foundation footing."""
        return self.width

    @length.setter
    def length(self, __val: float):
        self.width = __val


@dataclass
class CircularFooting:
    """A class representation of circular footing.

    Parameters
    ----------
    diameter : float, m
        Diameter of foundation footing.

    Attributes
    ----------
    width : float, m
    length : float, m

    See Also
    --------
    SquareFooting, RectangularFooting

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

    Parameters
    ----------
    width : float, m
        Width of foundation footing.

    Attributes
    ----------
    length : float, m

    See Also
    --------
    CircularFooting, RectangularFooting

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

    Parameters
    ----------
    width : float, m
        Width of foundation footing.
    length : float, m
        Length of foundation footing.

    See Also
    --------
    CircularFooting, SquareFooting

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


@dataclass
class FootingSize:
    """Size of foundation footing.

    Parameters
    ----------
    thickness : float, m
        Thickness of foundation footing.
    footing_shape : _FootingShape
        Shape of foundation footing.

    Attributes
    ----------
    width : float, m
    length : float, m

    See Also
    --------
    FoundationSize

    Examples
    --------
    >>> from geolysis.core.foundation import FootingSize, SquareFooting
    >>> footing_shape = SquareFooting(width=1.2)
    >>> footing_size = FootingSize(thickness=0.45, footing_shape=footing_shape)
    >>> footing_size.thickness
    0.45
    >>> footing_size.width
    1.2
    >>> footing_size.length
    1.2
    """

    thickness: float
    footing_shape: _FootingShape

    @property
    def width(self) -> float:
        """Width of foundation footing."""
        return self.footing_shape.width

    @width.setter
    def width(self, __val: float):
        self.footing_shape.width = __val

    @property
    def length(self) -> float:
        """Length of foundation footing."""
        return self.footing_shape.length

    @length.setter
    def length(self, __val: float):
        self.footing_shape.length = __val


@dataclass
class FoundationSize:
    """A simple class representing a foundation structure.

    Parameters
    ----------
    depth : float, m
        Depth of foundation.
    footing_size : FootingSize
        Represents the size of the foundation footing.

    Attributes
    ----------
    thickness : float, m
    width : float, m
    length : float, m
    footing_shape : _FootingShape

    See Also
    --------
    FootingSize

    Examples
    --------
    >>> from geolysis.core.foundation import (
    ...     FoundationSize,
    ...     CircularFooting,
    ...     Shape,
    ...     create_footing,
    ... )
    >>> footing_size = create_footing(
    ...     thickness=0.45, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> foundation_size = FoundationSize(depth=1.5, footing_size=footing_size)
    >>> foundation_size.depth
    1.5
    >>> foundation_size.thickness
    0.45
    >>> foundation_size.length
    1.2
    >>> foundation_size.width
    1.2
    """

    depth: float
    footing_size: FootingSize

    @property
    def thickness(self) -> float:
        """Thickness of foundation footing."""
        return self.footing_size.thickness

    @thickness.setter
    def thickness(self, __val: float):
        self.footing_size.thickness = __val

    @property
    def width(self) -> float:
        """Width of foundation footing."""
        return self.footing_size.width

    @width.setter
    def width(self, __val: float):
        self.footing_size.width = __val

    @property
    def length(self) -> float:
        """Length of foundation footing."""
        return self.footing_size.length

    @length.setter
    def length(self, __val: float):
        self.footing_size.length = __val

    @property
    def footing_shape(self) -> _FootingShape:
        """Represents the shape of the foundation footing."""
        return self.footing_size.footing_shape

    @footing_shape.setter
    def footing_shape(self, __val: _FootingShape):
        self.footing_size.footing_shape = __val


def create_footing(
    thickness: float,
    width: float,
    length: Optional[float] = None,
    footing_shape: Shape | str = Shape.SQUARE,
) -> FootingSize:
    """A factory function that encapsulate the creation of a foundation
    footing.

    Parameters
    ----------
    thickness : float, m
        Thickness of foundation footing.
    width : float, m
        Width of foundation footing.
    length : float, optional, m
        Length of foundation footing.
    footing_shape : Shape | str, default=Shape.SQUARE
        Shape of foundation footing.

    Returns
    -------
    FootingSize
        Size of foundation footing.

    Raises
    ------
    FootingCreationError
        Exception raised when footing is not created successfully.

    # TODO: Update examples to test for strip footing creation.

    Examples
    --------
    >>> from geolysis.core.foundation import create_footing, Shape
    >>> square_footing = create_footing(
    ...     thickness=0.3, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> square_footing
    FootingSize(thickness=0.3, footing_shape=SquareFooting(width=1.2))
    >>> square_footing.footing_shape
    SquareFooting(width=1.2)

    >>> circ_footing = create_footing(thickness=0.4, width=1.4, footing_shape="CIRCLE")
    >>> circ_footing
    FootingSize(thickness=0.4, footing_shape=CircularFooting(diameter=1.4))
    >>> circ_footing.footing_shape
    CircularFooting(diameter=1.4)

    >>> rect_footing = create_footing(
    ...     thickness=0.5, width=1.3, length=1.4, footing_shape=Shape.RECTANGLE
    ... )
    >>> rect_footing
    FootingSize(thickness=0.5, footing_shape=RectangularFooting(width=1.3, length=1.4))
    >>> rect_footing.footing_shape
    RectangularFooting(width=1.3, length=1.4)
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

    return FootingSize(thickness=thickness, footing_shape=_footing_shape)


def create_foundation(
    depth: float,
    thickness: float,
    width: float,
    length: Optional[float] = None,
    footing_shape: Shape | str = Shape.SQUARE,
) -> FoundationSize:
    """A factory function that encapsulate the creation of a foundation.

    Parameters
    ----------
    depth : float, m
        Depth of foundation.
    thickness : float, m
        Thickness of foundation footing.
    width : float, m
        Width of foundation footing.
    length : float, optional, m
        Length of foundation footing.
    footing_shape : Shape | str, default=Shape.SQUARE
        Shape of foundation footing.

    Returns
    -------
    FootingSize
        Size of foundation footing.

    Raises
    ------
    FootingCreationError
        Exception raised when footing is not created successfully.

    Examples
    --------
    >>> from geolysis.core.foundation import Shape, create_foundation
    >>> foundation_size = create_foundation(
    ...     depth=1.5, thickness=0.3, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> foundation_size.depth
    1.5
    >>> foundation_size.thickness
    0.3
    >>> foundation_size.width
    1.2
    >>> foundation_size.length
    1.2
    """

    footing_size = create_footing(thickness, width, length, footing_shape)
    return FoundationSize(depth, footing_size)
