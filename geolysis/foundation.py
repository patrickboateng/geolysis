import enum
from typing import TypeAlias, Optional, Final, Any

from geolysis.utils import inf
from geolysis import validators

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

    def __set_name__(self, objtype, property_name) -> None:
        self.property_name = property_name


class Shape(enum.StrEnum):
    """Enumeration of foundation shapes."""

    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


class StripFooting:
    """A class representation of strip footing."""

    def __init__(self, width: float, length: float = inf) -> None:
        """
        :param width: Width of foundation footing. (m)
        :type width: float

        :param float length: Length of foundation footing, defaults to inf. (m)
        :type length: float
        """
        self.width = width
        self.length = length
        self._shape = Shape.STRIP

    @property
    def width(self):
        return self._width

    @width.setter
    @validators.gt(0.0)
    def width(self, val):
        self._width = val

    @property
    def length(self):
        return self._length

    @length.setter
    @validators.ge(0.0)
    def length(self, val):
        self._length = val

    @property
    def shape(self):
        return self._shape

    
class CircularFooting:
    """A class representation of circular footing.

    .. note::

        The ``width`` and ``length`` properties refer to the diameter of the
        circular footing. This is to make it compatible with the protocol square
        and rectangular footing follow.
    """

    width = _Field(attr="diameter", doc="Diameter of foundation footing.")
    length = _Field(attr="diameter", doc="Diameter of foundation footing.")

    def __init__(self, diameter: float):
        """
        :param float diameter: Diameter of foundation footing. (m)
        """
        self.diameter = diameter
        self._shape = Shape.CIRCLE

    @property
    def diameter(self):
        return self._diameter
    
    @diameter.setter
    @validators.gt(0.0)
    def diameter(self, val):
        self._diameter = val

    @property
    def shape(self):
        return self._shape

    
class SquareFooting:
    """A class representation of square footing."""

    length = _Field(attr="width", doc="Width of foundation footing. (m)")

    def __init__(self, width: float):
        """
        :param float width: Width of foundation footing. (m)
        """
        self.width = width
        self._shape = Shape.SQUARE

    @property
    def width(self):
        return self._width

    @width.setter
    @validators.gt(0)
    def width(self, val):
        self._width = val

    @property
    def shape(self):
        return self._shape


class RectangularFooting:
    """A class representation of rectangular footing."""

    def __init__(self, width: float, length: float):
        """
        :param width: Width of foundation footing. (m)
        :type width: float

        :param length: Length of foundation footing. (m)
        :type length: float
        """
        self.width = width
        self.length = length
        self._shape = Shape.RECTANGLE

    @property
    def width(self):
        return self._width
    
    @width.setter
    @validators.gt(0.0)
    def width(self, val):
        self._width = val

    @property
    def length(self):
        return self._length
    
    @length.setter
    @validators.gt(0.0)
    def length(self, val):
        self._length = val

    @property
    def shape(self):
        return self._shape


FootingSize: TypeAlias = (
        StripFooting | CircularFooting | SquareFooting | RectangularFooting)


class FoundationSize:
    """A simple class representing a foundation structure."""

    width = _Field(attr="width", obj="footing_size", 
                   doc="Width of foundation footing. (m)")
    length = _Field(attr="length", obj="footing_size", 
                    doc="Length of foundation footing. (m)")
    footing_shape = _Field(attr="shape", obj="footing_size", 
                           doc="Shape of foundation footing.")

    def __init__(self, depth: float, footing_size: FootingSize,
                 eccentricity: float = 0.0) -> None:
        """
        :param depth: Depth of foundation. (m)
        :type depth: float

        :param footing_size: Represents the size of the foundation footing.
        :type footing_size: FootingSize

        :param eccentricity: The deviation of the foundation load on the center
                             of the center of gravity of the foundation footing, 
                             defaults to 0.0. This means that the foundation 
                             load aligns with the center of gravity of the 
                             foundation footing. (m)
        :type eccentricity: float, optional
        """
        self.depth = depth
        self.footing_size = footing_size
        self.eccentricity = eccentricity

    @property
    def depth(self) -> float:
        return self._depth
    
    @depth.setter
    @validators.gt(0.0)
    def depth(self, val: float) -> None:
        self._depth = val

    @property
    def eccentricity(self) -> float:
        return self._eccentricity
    
    @eccentricity.setter
    @validators.ge(0.0)
    def eccentricity(self, val: float) -> None:
        self._eccentricity = val

    @property
    def effective_width(self) -> float:
        """Returns the effective width of the foundation footing."""
        return self.width - 2.0 * self.eccentricity


def create_foundation(depth: float, width: float,
                      length: Optional[float] = None,
                      eccentricity: float = 0.0,
                      shape: Shape | str = Shape.SQUARE) -> FoundationSize:
    """A factory function that encapsulate the creation of a foundation.

    :param depth: Depth of foundation. (m)
    :type depth: float

    :param width: Width of foundation footing. (m)
    :type width: float

    :param length: Length of foundation footing, defaults to None. (m)
    :type length: float, optional

    :param eccentricity: The deviation of the foundation load on the center
                         of the center of gravity of the foundation footing, 
                         defaults to 0.0. This means that the foundation 
                         load aligns with the center of gravity of the 
                         foundation footing. (m)
    :type eccentricity: float, optional

    :param shape: Shape of foundation footing, defaults to :class:`Shape.SQUARE`
    :type shape: Shape | str

    :raises ValueError: Raised when length is not provided for a rectangular
                        footing.
    :raises TypeError: Raised if an invalid footing shape is provided.
    """

    if isinstance(shape, str):
        shape = Shape(shape.casefold())

    if shape is Shape.STRIP:
        footing_size = StripFooting(width=width)
    elif shape is Shape.SQUARE:
        footing_size = SquareFooting(width=width)
    elif shape is Shape.CIRCLE:
        footing_size = CircularFooting(diameter=width)
    elif shape is Shape.RECTANGLE:
        if not length:
            raise ValueError("Length of footing must be provided.")
        footing_size = RectangularFooting(width=width, length=length)
    else:
        raise TypeError("Invalid footing shape.")

    return FoundationSize(depth=depth, eccentricity=eccentricity,
                          footing_size=footing_size)
