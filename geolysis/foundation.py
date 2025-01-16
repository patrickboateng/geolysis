import enum
from typing import TypeAlias, Optional, Final, Any

from geolysis.utils import inf

__all__ = ["create_foundation", "FoundationSize", "Shape", "StripFooting",
           "CircularFooting", "SquareFooting", "RectangularFooting"]


class _Field:
    def __init__(self, *, attr: str, obj: Optional[str] = None,
                 doc: Optional[str] = None):
        self.ref_attr = attr
        self.ref_obj = obj
        self.fget: Final = getattr
        self.fset: Final = setattr
        self.fdel: Final = delattr
        self.__doc__ = doc

    def __get__(self, obj, objtype=None) -> Any:
        if self.ref_obj is not None:
            ref_obj = self.fget(obj, self.ref_obj)
            return self.fget(ref_obj, self.ref_attr)
        return self.fget(obj, self.ref_attr)

    def __set__(self, obj, value) -> None:
        if self.ref_obj is not None:
            ref_obj = self.fget(obj, self.ref_obj)
            self.fset(ref_obj, self.ref_attr, value)
        else:
            self.fset(obj, self.ref_attr, value)

    #: TODO: check deleter
    def __delete__(self, obj) -> None:
        self.fdel(obj, self.property_name)

    def __set_name__(self, objtype, property_name) -> None:
        self.property_name = property_name


class Shape(enum.StrEnum):
    """"""

    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


class StripFooting:
    def __init__(self, width: float, length: float = inf) -> None:
        self._width = width
        self._length = length
        self._shape_ = Shape.STRIP

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, val: float):
        self._width = val

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, val: float):
        self._length = val

    @property
    def shape_(self) -> Shape:
        return self._shape_


class CircularFooting:
    """A class representation of circular footing.

    .. seealso::

        :class:`SquareFooting`, :class:`RectangularFooting`

    .. note::

        The ``width`` and ``length`` properties refer to the diameter of the
        circular footing. This is to make it compatible with the protocol square
        and rectangular footing follow.

    >>> from geolysis.foundation import CircularFooting
    >>> circ_footing = CircularFooting(diameter=1.2)
    >>> circ_footing.diameter
    1.2
    >>> circ_footing.width
    1.2
    >>> circ_footing.length
    1.2
    """

    width = _Field(attr="diameter", doc="Diameter of footing.")
    length = _Field(attr="diameter", doc="Diameter of footing.")

    def __init__(self, diameter: float):
        """
        :param float diameter: Diameter of foundation footing. (m)
        """
        self._diameter = diameter
        self._shape_ = Shape.CIRCLE

    @property
    def diameter(self) -> float:
        return self._diameter

    @diameter.setter
    def diameter(self, val):
        self._diameter = val

    @property
    def shape_(self) -> Shape:
        return self._shape_


class SquareFooting:
    """A class representation of square footing.

    .. seealso::

        :class:`CircularFooting`, :class:`RectangularFooting`

    .. code::

        >>> from geolysis.foundation import SquareFooting
        >>> sq_footing = SquareFooting(width=1.2)
        >>> sq_footing.width
        1.2
        >>> sq_footing.length
        1.2
    """

    length = _Field(attr="width", doc="Width of footing. (m)")

    def __init__(self, width: float):
        """
        :param float width: Width of foundation footing. (m)
        """
        self._width = width
        self._shape_ = Shape.SQUARE

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, val: float):
        self._width = val

    @property
    def shape_(self) -> Shape:
        return self._shape_


class RectangularFooting:
    """A class representation of rectangular footing.

    .. seealso::

        :class:`CircularFooting`, :class:`SquareFooting`

    .. code::

        >>> from geolysis.foundation import RectangularFooting
        >>> rect_footing = RectangularFooting(width=1.2, length=1.4)
        >>> rect_footing.width
        1.2
        >>> rect_footing.length
        1.4
    """

    def __init__(self, width: float, length: float):
        """
        :param float width: Width of foundation footing. (m)
        :param float length: Length of foundation footing. (m)
        """
        self._width = width
        self._length = length
        self._shape_ = Shape.RECTANGLE

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, val: float):
        self._width = val

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, val: float):
        self._length = val

    @property
    def shape_(self) -> Shape:
        return self._shape_


FootingSize: TypeAlias = (
        StripFooting | CircularFooting | SquareFooting | RectangularFooting)


class FoundationSize:
    """A simple class representing a foundation structure.


    >>> from geolysis.foundation import (
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

    width = _Field(attr="width", obj="footing_size")
    length = _Field(attr="length", obj="footing_size")
    footing_shape = _Field(attr="shape_", obj="footing_size")

    def __init__(self, depth: float, footing_size: FootingSize,
                 eccentricity: float = 0.0) -> None:
        """
        :param float depth: Depth of foundation. (m)
        :param FootingSize footing_size: Represents the size of the foundation
            footing.
        """
        self._depth = depth
        self._footing_size = footing_size
        self._eccentricity = eccentricity

    @property
    def depth(self) -> float:
        return self._depth

    @depth.setter
    def depth(self, val: float):
        self._depth = val

    @property
    def eccentricity(self) -> float:
        return self._eccentricity

    @eccentricity.setter
    def eccentricity(self, val: float):
        self._eccentricity = val

    @property
    def footing_size(self) -> FootingSize:
        return self._footing_size

    @footing_size.setter
    def footing_size(self, val: FootingSize):
        self._footing_size = val

    @property
    def effective_width(self) -> float:
        return self.width - 2 * self.eccentricity


def create_foundation(depth: float, width: float,
                      length: Optional[float] = None,
                      eccentricity: float = 0.0,
                      footing_shape: Shape | str = Shape.SQUARE) -> FoundationSize:
    """A factory function that encapsulate the creation of a foundation
    footing.

    :param float depth: Depth of foundation. (m)
    :param float width: Width of foundation footing (m)
    :param float length: Length of foundation footing, defaults to None. (m)
    :param float eccentricity: Eccentricity of foundation, defaults to 0.0. (m)
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

    return FoundationSize(depth=depth, eccentricity=eccentricity,
                          footing_size=footing_size)
