import enum
from abc import abstractmethod
from typing import Optional, Protocol, TypeVar

from geolysis import validators
from geolysis.utils import inf

__all__ = ["create_foundation", "FoundationSize", "Shape", "StripFooting",
           "CircularFooting", "SquareFooting", "RectangularFooting"]

T = TypeVar("T")


class _Field:
    """A field that references another field."""

    def __init__(self, *, ref_attr: str, ref_obj: Optional[str] = None,
                 doc: Optional[str] = None):
        self.ref_attr = ref_attr
        self.ref_obj = ref_obj
        self.__doc__ = doc

    def __get__(self, obj, objtype=None) -> T:
        if self.ref_obj is not None:
            ref_obj = getattr(obj, self.ref_obj)
            return getattr(ref_obj, self.ref_attr)
        return getattr(obj, self.ref_attr)

    def __set__(self, obj, value) -> None:
        if self.ref_obj is not None:
            ref_obj = getattr(obj, self.ref_obj)
            setattr(ref_obj, self.ref_attr, value)
        else:
            setattr(obj, self.ref_attr, value)

    def __set_name__(self, objtype, property_name) -> None:
        self.property_name = property_name


class Shape(enum.StrEnum):
    """Enumeration of foundation shapes."""
    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


class FootingSize(Protocol):
    @property
    @abstractmethod
    def width(self) -> float: ...

    @property
    @abstractmethod
    def length(self) -> float: ...

    @property
    @abstractmethod
    def shape(self) -> Shape: ...


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
    def width(self) -> float:
        return self._width

    @width.setter
    @validators.gt(0.0)
    def width(self, val):
        self._width = val

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    @validators.ge(0.0)
    def length(self, val):
        self._length = val

    @property
    def shape(self) -> Shape:
        return self._shape


class CircularFooting:
    """A class representation of circular footing.

    .. note::

        The ``width`` and ``length`` properties refer to the diameter of the
        circular footing. This is to make it compatible with the protocol
        square and rectangular footing follow.
    """

    _doc = "Refers to the diameter of the circular footing."

    width = _Field(ref_attr="diameter", doc=_doc)
    length = _Field(ref_attr="diameter", doc=_doc)

    del _doc

    def __init__(self, diameter: float):
        """
        :param float diameter: Diameter of foundation footing. (m)
        """
        self.diameter = diameter
        self._shape = Shape.CIRCLE

    @property
    def diameter(self) -> float:
        return self._diameter

    @diameter.setter
    @validators.gt(0.0)
    def diameter(self, val):
        self._diameter = val

    @property
    def shape(self) -> Shape:
        return self._shape


class SquareFooting:
    """A class representation of square footing."""

    length = _Field(ref_attr="width",
                    doc="Refers to the width of the square footing.")

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
    def width(self) -> float:
        return self._width

    @width.setter
    @validators.gt(0.0)
    def width(self, val):
        self._width = val

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    @validators.gt(0.0)
    def length(self, val):
        self._length = val

    @property
    def shape(self) -> Shape:
        return self._shape


class FoundationSize:
    """A simple class representing a foundation structure."""

    width = _Field(ref_attr="width", ref_obj="footing_size",
                   doc="Refers to the width of foundation footing.")
    length = _Field(ref_attr="length", ref_obj="footing_size",
                    doc="Refers to the length of foundation footing.")
    footing_shape = _Field(ref_attr="shape", ref_obj="footing_size",
                           doc="Refers to the shape of foundation footing.")

    def __init__(self, depth: float, footing_size: FootingSize,
                 eccentricity: float = 0.0,
                 ground_water_level: float = inf) -> None:
        """
        :param depth: Depth of foundation. (m)
        :type depth: float

        :param footing_size: Represents the size of the foundation footing.
        :type footing_size: FootingSize

        :param eccentricity: The deviation of the foundation load from the
                             center of gravity of the foundation footing,
                             defaults to 0.0. This means that the foundation 
                             load aligns with the center of gravity of the 
                             foundation footing. (m)
        :type eccentricity: float, optional

        :param ground_water_level: Depth of the water below ground level (m),
                                   defaults to inf.
        :type ground_water_level: float, optional
        """
        self.depth = depth
        self.footing_size = footing_size
        self.eccentricity = eccentricity
        self.ground_water_level = ground_water_level

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
    def ground_water_level(self) -> float:
        return self._ground_water_level

    @ground_water_level.setter
    @validators.ge(0.0)
    def ground_water_level(self, val: float) -> None:
        self._ground_water_level = val

    @property
    def effective_width(self) -> float:
        """Returns the effective width of the foundation footing."""
        return self.width - 2.0 * self.eccentricity


def create_foundation(depth: float, width: float,
                      length: Optional[float] = None,
                      eccentricity: float = 0.0,
                      ground_water_level: float = inf,
                      shape: Shape | str = Shape.SQUARE) -> FoundationSize:
    """A factory function that encapsulate the creation of a foundation.

    :param depth: Depth of foundation. (m)
    :type depth: float

    :param width: Width of foundation footing. In the case of a circular
                  footing, it refers to the footing diameter. (m)
    :type width: float

    :param length: Length of foundation footing, defaults to None. (m)
    :type length: float, optional

    :param eccentricity: The deviation of the foundation load from the
                         center of gravity of the foundation footing,
                         defaults to 0.0. This means that the foundation
                         load aligns with the center of gravity of the
                         foundation footing. (m)
    :type eccentricity: float, optional

    :param ground_water_level: Depth of the water below ground level (m),
                               defaults to inf.
    :type ground_water_level: float, optional

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
        raise TypeError(f"shape {shape} is not supported.")

    return FoundationSize(depth=depth, eccentricity=eccentricity,
                          ground_water_level=ground_water_level,
                          footing_size=footing_size)
