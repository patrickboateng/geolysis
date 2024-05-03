import enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Protocol

from geolysis.utils import PI, round_

__all__ = [
    "create_footing",
    "create_foundation",
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
    "FootingSize",
    "FoundationSize",
]


class FootingCreationError(TypeError):
    pass


class Shape(enum.IntEnum):
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


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

    @property
    @abstractmethod
    def area(self) -> float: ...

    @property
    @abstractmethod
    def perimeter(self) -> float: ...


@dataclass
class CircularFooting:
    """A class representation of circular footing.

    Parameters
    ----------
    diameter : float, unit=metre
        Diameter of foundation footing.

    Attributes
    ----------
    diameter : float, unit=metre
    width : float, unit=metre
    length : float, unit=metre
    area : float, unit = :math:`m^2`
    perimeter : float, unit=metre

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
    >>> from geolysis.foundation import CircularFooting
    >>> circ_footing = CircularFooting(diameter=1.2)
    >>> circ_footing.diameter
    1.2
    >>> circ_footing.width
    1.2
    >>> circ_footing.length
    1.2
    >>> circ_footing.area
    1.131
    >>> circ_footing.perimeter
    3.7699
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

    @property
    @round_
    def area(self) -> float:
        """Area of circular footing. |rarr| :math:`m^2`"""
        return PI * (self.diameter**2) / 4

    @property
    @round_
    def perimeter(self) -> float:
        """Perimeter of circular footing. |rarr| m"""
        return PI * self.diameter


@dataclass
class SquareFooting:
    """A class representation of square footing.

    Parameters
    ----------
    width : float, unit=metre
        Width of foundation footing.

    Attributes
    ----------
    width : float, unit=metre
    length : float, unit=metre
    area : float, unit = :math:`m^2`
    perimeter : float, unit=metre

    See Also
    --------
    CircularFooting, RectangularFooting

    Examples
    --------
    >>> from geolysis.foundation import SquareFooting
    >>> sq_footing = SquareFooting(width=1.2)
    >>> sq_footing.width
    1.2
    >>> sq_footing.length
    1.2
    >>> sq_footing.area
    1.44
    >>> sq_footing.perimeter
    4.8
    """

    width: float

    @property
    def length(self) -> float:
        """Length of foundation footing."""
        return self.width

    @length.setter
    def length(self, __val: float):
        self.width = __val

    @property
    @round_
    def area(self) -> float:
        """Area of square footing. |rarr| :math:`m^2`"""
        return self.width**2

    @property
    @round_
    def perimeter(self) -> float:
        """Perimeter of square footing. |rarr| m"""
        return 4 * self.width


@dataclass
class RectangularFooting:
    """A class representation of rectangular footing.

    Parameters
    ----------
    width : float, unit=metre
        Width of foundation footing.
    length : float, unit=metre
        Length of foundation footing.

    Attributes
    ----------
    width : float, unit=metre
    length : float, unit=metre
    area : float, unit = :math:`m^2`
    perimeter : float, unit=metre

    See Also
    --------
    CircularFooting, SquareFooting

    Examples
    --------
    >>> from geolysis.foundation import RectangularFooting
    >>> rect_footing = RectangularFooting(width=1.2, length=1.4)
    >>> rect_footing.width
    1.2
    >>> rect_footing.length
    1.4
    >>> rect_footing.area
    1.68
    >>> rect_footing.perimeter
    5.2
    """

    width: float
    length: float

    @property
    @round_
    def area(self) -> float:
        """Area of rectangular footing. |rarr| :math:`m^2`"""
        return self.length * self.width

    @property
    @round_
    def perimeter(self) -> float:
        """Perimeter of rectangular footing. |rarr| m"""
        return 2 * (self.length + self.width)


@dataclass
class FootingSize:
    """Size of foundation footing.

    Parameters
    ----------
    thickness : float, unit=metre
        Thickness of foundation footing.
    footing_shape : _FootingShape
        Shape of foundation footing.

    Attributes
    ----------
    thickness : float, unit=metre
    width : float, unit=metre
    length : float, unit=metre
    footing_shape : _FootingShape
    area : float, unit = :math:`m^2`
    perimeter : float, unit=metre
    volume : float, unit = :math:`m^3`

    See Also
    --------
    FoundationSize

    Examples
    --------
    >>> from geolysis.foundation import FootingSize, SquareFooting
    >>> footing_shape = SquareFooting(width=1.2)
    >>> footing_size = FootingSize(thickness=0.45, footing_shape=footing_shape)
    >>> footing_size.thickness
    0.45
    >>> footing_size.width
    1.2
    >>> footing_size.length
    1.2
    >>> footing_size.area
    1.44
    >>> footing_size.perimeter
    4.8
    >>> footing_size.volume
    0.648
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

    @property
    def area(self) -> float:
        """Area of foundation footing. |rarr| :math:`m^2`"""
        return self.footing_shape.area

    @property
    def perimeter(self) -> float:
        """Perimeter of foundation footing. |rarr| m"""
        return self.footing_shape.perimeter

    @property
    @round_
    def volume(self) -> float:
        """Volume of foundation footing. |rarr| :math:`m^3`"""
        return self.area * self.thickness


@dataclass
class FoundationSize:
    """A simple class representing a foundation structure.

    Parameters
    ----------
    depth : float, unit=metre
        Depth of foundation.
    footing_size : FootingSize
        Represents the size of the foundation footing.

    Attributes
    ----------
    depth : float, unit=metre
    thickness : float, unit=metre
    width : float, unit=metre
    length : float, unit=metre
    footing_shape : _FootingShape
    footing_size : FootingSize
    area : float, unit = :math:`m^2`
    perimeter : float, unit=metre
    volume : float, unit = :math:`m^3`

    See Also
    --------
    FootingSize

    Examples
    --------
    >>> from geolysis.foundation import (FoundationSize, CircularFooting,
    ...                                  Shape, create_footing)
    >>> footing_size = create_footing(thickness=0.45, width=1.2,
    ...                               footing_shape=Shape.SQUARE)
    >>> foundation_size = FoundationSize(depth=1.5, footing_size=footing_size)
    >>> foundation_size.depth
    1.5
    >>> foundation_size.thickness
    0.45
    >>> foundation_size.length
    1.2
    >>> foundation_size.width
    1.2
    >>> foundation_size.area
    1.44
    >>> foundation_size.perimeter
    4.8
    >>> foundation_size.volume
    2.16
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

    @property
    def area(self) -> float:
        """Area of foundation. |rarr| :math:`m^2`"""
        return self.footing_size.area

    @property
    def perimeter(self) -> float:
        """Perimeter of foundation. |rarr| m"""
        return self.footing_size.perimeter

    @property
    @round_
    def volume(self) -> float:
        """Volume of foundation. |rarr| :math:`m^3`"""
        return self.area * self.depth


def create_footing(
    thickness: float,
    width: float,
    length: Optional[float] = None,
    footing_shape: Shape = Shape.SQUARE,
) -> FootingSize:
    """A factory function that encapsulate the creation of a foundation
    footing.

    Parameters
    ----------
    thickness : float, unit=metre
        Thickness of foundation footing.
    width : float, unit=metre
        Width of foundation footing.
    length : float, optional, unit=metre
        Length of foundation footing.
    footing_shape : Shape, default=Shape.SQUARE
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
    >>> from geolysis.foundation import create_footing, Shape
    >>> square_footing = create_footing(thickness=0.3, width=1.2,
    ...                                 footing_shape=Shape.SQUARE)
    >>> square_footing
    FootingSize(thickness=0.3, footing_shape=SquareFooting(width=1.2))
    >>> square_footing.footing_shape
    SquareFooting(width=1.2)

    >>> circ_footing = create_footing(thickness=0.4, width=1.4,
    ...                               footing_shape=Shape.CIRCLE)
    >>> circ_footing
    FootingSize(thickness=0.4, footing_shape=CircularFooting(diameter=1.4))
    >>> circ_footing.footing_shape
    CircularFooting(diameter=1.4)

    >>> rect_footing = create_footing(thickness=0.5, width=1.3, length=1.4,
    ...                               footing_shape=Shape.RECTANGLE)
    >>> rect_footing
    FootingSize(thickness=0.5, footing_shape=RectangularFooting(width=1.3, length=1.4))
    >>> rect_footing.footing_shape
    RectangularFooting(width=1.3, length=1.4)

    >>> create_footing(thickness=0.5, width=1.3, footing_shape=Shape.RECTANGLE)
    Traceback (most recent call last):
        ...
    FootingCreationError: The length of the footing must be provided

    >>> create_footing(thickness=0.5, width=1.3, footing_shape="hexagonal")
    Traceback (most recent call last):
        ...
    FootingCreationError: Supported footing shapes are SQUARE, RECTANGLE, and CIRCLE
    """
    _footing_shape: _FootingShape

    match footing_shape:
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
    footing_shape: Shape = Shape.SQUARE,
) -> FoundationSize:
    """A factory function that encapsulate the creation of a foundation.

    Parameters
    ----------
    depth : float, unit=metre
        Depth of foundation.
    thickness : float, unit=metre
        Thickness of foundation footing.
    width : float, unit=metre
        Width of foundation footing.
    length : float, optional, unit=metre
        Length of foundation footing.
    footing_shape : Shape, default=Shape.SQUARE
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
    >>> from geolysis.foundation import Shape, create_foundation
    >>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
    ...                                     width=1.2, footing_shape=Shape.SQUARE)
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
