""" Basic foundation module.

Enums
=====

.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    Shape

Classes
=======

.. autosummary::
    :toctree: _autosummary

    StripFooting
    CircularFooting
    SquareFooting
    RectangularFooting
    FoundationSize

Functions
=========

.. autosummary::
    :toctree: _autosummary

    create_foundation
"""

import enum
from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from geolysis import error_msg_tmpl
from geolysis.utils import inf, enum_repr, isclose, validators

__all__ = ["create_foundation",
           "FoundationSize",
           "FoundationType",
           "Shape",
           "StripFooting",
           "CircularFooting",
           "SquareFooting",
           "RectangularFooting"]

T = TypeVar("T")


@enum_repr
class Shape(enum.StrEnum):
    """Enumeration of foundation shapes."""
    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


@enum_repr
class FoundationType(enum.StrEnum):
    """Enumeration of foundation types."""
    PAD = enum.auto()
    MAT = enum.auto()


class FootingSize(ABC):
    SHAPE: Shape

    @property
    @abstractmethod
    def width(self) -> float:
        raise NotImplementedError

    @width.setter
    def width(self, value: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def length(self) -> float:
        raise NotImplementedError

    @length.setter
    def length(self, value: float):
        raise NotImplementedError

    @property
    def shape(self) -> Shape:
        return self.SHAPE


class StripFooting(FootingSize):
    """A class representation of strip footing."""

    SHAPE = Shape.STRIP

    def __init__(self, width: float, length: float = inf) -> None:
        """
        :param width: Width of foundation footing. (m)
        :type width: float

        :param float length: Length of foundation footing, defaults to inf. (m)
        :type length: float
        """
        self.width = width
        self.length = length

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    @validators.gt(0.0)
    def width(self, val: float):
        self._width = val

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    @validators.ge(0.0)
    def length(self, val: float):
        self._length = val


class CircularFooting(FootingSize):
    """A class representation of circular footing.

    .. note::

        The ``width`` and ``length`` properties refer to the diameter of the
        circular footing. This is to make it compatible with the protocol
        square and rectangular footing follow.
    """

    SHAPE = Shape.CIRCLE

    def __init__(self, diameter: float):
        """
        :param float diameter: Diameter of foundation footing. (m)
        """
        self.diameter = diameter

    @property
    def diameter(self) -> float:
        return self._diameter

    @diameter.setter
    @validators.gt(0.0)
    def diameter(self, val: float):
        self._diameter = val

    @property
    def width(self):
        return self.diameter

    @width.setter
    def width(self, val: float):
        self.diameter = val

    @property
    def length(self):
        return self.diameter

    @length.setter
    def length(self, val: float):
        self.diameter = val


class SquareFooting(FootingSize):
    """A class representation of square footing."""

    SHAPE = Shape.SQUARE

    def __init__(self, width: float):
        """
        :param float width: Width of foundation footing. (m)
        """
        self.width = width

    @property
    def width(self):
        return self._width

    @width.setter
    @validators.gt(0)
    def width(self, val):
        self._width = val

    @property
    def length(self):
        return self.width

    @length.setter
    def length(self, val):
        self.width = val


class RectangularFooting(FootingSize):
    """A class representation of rectangular footing."""

    SHAPE = Shape.RECTANGLE

    def __init__(self, width: float, length: float):
        """
        :param width: Width of foundation footing. (m)
        :type width: float

        :param length: Length of foundation footing. (m)
        :type length: float
        """
        self.width = width
        self.length = length

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


class FoundationSize:
    """A simple class representing a foundation structure."""

    def __init__(self, depth: float,
                 footing_size: FootingSize,
                 eccentricity: float = 0.0,
                 ground_water_level: Optional[float] = None) -> None:
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
        self._ground_water_level = ground_water_level

    @property
    def depth(self) -> float:
        return self._depth

    @depth.setter
    @validators.gt(0.0)
    def depth(self, val: float) -> None:
        self._depth = val

    @property
    def width(self):
        return self.footing_size.width

    @width.setter
    def width(self, val: float):
        self.footing_size.width = val

    @property
    def length(self):
        return self.footing_size.length

    @length.setter
    def length(self, val: float):
        self.footing_size.length = val

    @property
    def footing_shape(self):
        return self.footing_size.shape

    @property
    def eccentricity(self) -> float:
        return self._eccentricity

    @eccentricity.setter
    @validators.ge(0.0)
    def eccentricity(self, val: float) -> None:
        self._eccentricity = val

    @property
    def ground_water_level(self) -> Optional[float]:
        return self._ground_water_level

    @ground_water_level.setter
    @validators.ge(0.0)
    def ground_water_level(self, val: float) -> None:
        self._ground_water_level = val

    @property
    def effective_width(self) -> float:
        """Returns the effective width of the foundation footing."""
        return self.width - 2.0 * self.eccentricity

    def footing_params(self) -> tuple[float, float, Shape]:
        """Returns the ``width``, ``length``, and ``shape`` of the
        foundation footing.

        .. note:: "width" is the effective width of the foundation footing.
        """
        width, length, shape = self.effective_width, self.length, self.footing_shape

        if not isclose(width, length) and shape != Shape.STRIP:
            shape = Shape.RECTANGLE

        return width, length, shape


def create_foundation(depth: float,
                      width: float,
                      length: Optional[float] = None,
                      eccentricity: float = 0.0,
                      ground_water_level: Optional[float] = None,
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
                               defaults to None.
    :type ground_water_level: float, optional

    :param shape: Shape of foundation footing, defaults to :class:`Shape.SQUARE`
    :type shape: Shape | str

    :raises ValueError: Raised when length is not provided for a rectangular
                        footing.
    :raises ValueError: Raised if an invalid footing shape is provided.
    """
    shape = str(shape).casefold()

    try:
        shape = Shape(shape)
    except ValueError as e:
        msg = error_msg_tmpl(shape, Shape)
        raise ValueError(msg) from e

    if shape is Shape.STRIP:
        footing_size = StripFooting(width=width)
    elif shape is Shape.SQUARE:
        footing_size = SquareFooting(width=width)
    elif shape is Shape.CIRCLE:
        footing_size = CircularFooting(diameter=width)
    else:  # RECTANGLE
        if not length:
            raise ValueError("Length of footing must be provided.")
        footing_size = RectangularFooting(width=width, length=length)
    # else:
    #     msg = error_msg_tmpl(shape, Shape)
    #     raise ValueError(msg)

    return FoundationSize(depth=depth,
                          eccentricity=eccentricity,
                          ground_water_level=ground_water_level,
                          footing_size=footing_size)
