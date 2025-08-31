import enum
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Annotated

from func_validator import (
    validate_func_args,
    MustBePositive,
    MustBeNonNegative,
    MustBeBetween,
    MustBeMemberOf,
)

from .utils import AbstractStrEnum, inf, isclose

__all__ = [
    "create_foundation",
    "Foundation",
    "FoundationType",
    "Shape",
    "StripFooting",
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
]

T = TypeVar("T")


class Shape(AbstractStrEnum):
    """Enumeration of foundation shapes.

     Each member represents a standard geometric shape commonly used
     in foundation design, which can affect bearing capacity and
     settlement calculations.
     """

    STRIP = enum.auto()
    """Strip (or continuous) foundation, typically long and narrow."""

    CIRCLE = enum.auto()
    """Circular foundation, often used for columns or piers."""

    SQUARE = enum.auto()
    """Square foundation, commonly used for isolated footings."""

    RECTANGLE = enum.auto()
    """Rectangular foundation, used when length and width differ significantly."""


class FoundationType(AbstractStrEnum):
    """
    Enumeration of foundation types.

    Each member represents a common type of foundation used in
    geotechnical engineering. Some members have aliases for
    alternative naming conventions.
    """

    PAD = enum.auto()
    """Pad foundation, a small, isolated footing supporting a single column."""

    ISOLATED = PAD
    """Alias for PAD foundation (isolated footing)."""

    MAT = enum.auto()
    """Mat foundation, a large, continuous slab supporting multiple columns or 
    walls.
    """

    RAFT = MAT
    """Alias for MAT foundation (raft foundation)."""


class FootingSize(ABC):
    _SHAPE: Shape

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
        """Return the shape of the foundation footing."""
        return self._SHAPE


class StripFooting(FootingSize):
    """A class representation of strip footing."""

    _SHAPE = Shape.STRIP

    def __init__(self, width: float, length: float = inf):
        """
        :param width: Width of foundation footing (m).
        :param length: Length of foundation footing (m).
        """
        self.width = width
        self.length = length

    @property
    def width(self) -> float:
        """Width of foundation footing (m)."""
        return self._width

    @width.setter
    @validate_func_args
    def width(self, val: Annotated[float, MustBePositive]) -> None:
        self._width = val

    @property
    def length(self) -> float:
        """Length of foundation footing (m)."""
        return self._length

    @length.setter
    @validate_func_args
    def length(self, val: Annotated[float, MustBePositive]) -> None:
        self._length = val


class CircularFooting(FootingSize):
    """A class representation of circular footing.

    !!! note

        The `width` and `length` properties refer to the diameter of the
        circular footing. This is to make it compatible with the protocol
        square and rectangular footing follow.
    """

    _SHAPE = Shape.CIRCLE

    def __init__(self, diameter: float):
        """
        :param diameter: Diameter of foundation footing (m).
        """
        self.diameter = diameter

    @property
    def diameter(self) -> float:
        """Diameter of foundation footing (m)."""
        return self._diameter

    @diameter.setter
    @validate_func_args
    def diameter(self, val: Annotated[float, MustBePositive]) -> None:
        self._diameter = val

    @property
    def width(self):
        """Diameter of foundation footing (m)."""
        return self.diameter

    # Not checking for positive as diameter setter already does that
    @width.setter
    def width(self, val: float):
        self.diameter = val

    # Not checking for positive as diameter setter already does that
    @property
    def length(self):
        """Diameter of foundation footing (m)."""
        return self.diameter

    @length.setter
    def length(self, val: float):
        self.diameter = val


class SquareFooting(FootingSize):
    """A class representation of square footing."""

    _SHAPE = Shape.SQUARE

    def __init__(self, width: float):
        """
        :param float width: Width of foundation footing (m).
        """
        self.width = width

    @property
    def width(self):
        """Width of foundation footing (m)."""
        return self._width

    @width.setter
    @validate_func_args
    def width(self, val: Annotated[float, MustBePositive]) -> None:
        self._width = val

    @property
    def length(self):
        """Width of foundation footing (m)."""
        return self.width

    # Not checking for positive as width setter already does that
    @length.setter
    def length(self, val):
        self.width = val


class RectangularFooting(FootingSize):
    """A class representation of rectangular footing."""

    _SHAPE = Shape.RECTANGLE

    def __init__(self, width: float, length: float):
        """
        :param width: Width of foundation footing (m).
        :param length: Length of foundation footing (m).
        """
        self.width = width
        self.length = length

    @property
    def width(self) -> float:
        """Width of foundation footing (m)."""
        return self._width

    @width.setter
    @validate_func_args
    def width(self, val: Annotated[float, MustBePositive]) -> None:
        self._width = val

    @property
    def length(self) -> float:
        """Length of foundation footing (m)."""
        return self._length

    @length.setter
    @validate_func_args
    def length(self, val: Annotated[float, MustBePositive]) -> None:
        self._length = val


class Foundation:
    """A simple class representing a foundation structure."""

    def __init__(
            self,
            depth: float,
            footing_size: FootingSize,
            eccentricity: float = 0.0,
            load_angle: float = 0.0,
            ground_water_level: Optional[float] = None,
            foundation_type: FoundationType = FoundationType.PAD,
    ) -> None:
        r"""
        :param depth: Depth of foundation (m).
        :param footing_size: Represents the size of the foundation footing.
        :param eccentricity: The deviation of the foundation load from
                             the center of gravity of the foundation
                             footing (m).
        :param load_angle: Inclination of the applied load with the
                           vertical ($\alpha^{\circ}$)
        :param ground_water_level: Depth of the water below ground level
                                   (m).
        :param foundation_type: Type of foundation.
        """
        self.depth = depth
        self.footing_size = footing_size
        self.eccentricity = eccentricity
        self.load_angle = load_angle

        self._ground_water_level = ground_water_level
        self.foundation_type = foundation_type

    @property
    def depth(self) -> float:
        """Depth of foundation (m)."""
        return self._depth

    @depth.setter
    @validate_func_args
    def depth(self, val: Annotated[float, MustBePositive]) -> None:
        self._depth = val

    @property
    def width(self) -> float:
        """Width of foundation footing (m)."""
        return self.footing_size.width

    @width.setter
    def width(self, val: Annotated[float, MustBePositive]):
        self.footing_size.width = val

    @property
    def length(self) -> float:
        """Length of foundation footing (m)."""
        return self.footing_size.length

    @length.setter
    def length(self, val: Annotated[float, MustBePositive]):
        self.footing_size.length = val

    @property
    def footing_shape(self) -> Shape:
        """Shape of foundation footing."""
        return self.footing_size.shape

    @property
    def eccentricity(self) -> float:
        """The deviation of the foundation load from the center of
        gravity of the foundation footing (m).
        """
        return self._eccentricity

    @eccentricity.setter
    @validate_func_args
    def eccentricity(self, val: Annotated[float, MustBeNonNegative]) -> None:
        self._eccentricity = val

    @property
    def load_angle(self) -> float:
        """Inclination of the applied load with the  vertical."""
        return self._load_angle

    @load_angle.setter
    @validate_func_args
    def load_angle(
            self,
            val: Annotated[float, MustBeBetween(min_value=0.0, max_value=90.0)]
    ) -> None:
        self._load_angle = val

    @property
    def ground_water_level(self) -> Optional[float]:
        """Depth of the water below ground level (m)."""
        return self._ground_water_level

    @ground_water_level.setter
    @validate_func_args
    def ground_water_level(self, val: Annotated[float, MustBePositive]):
        self._ground_water_level = val

    @property
    def foundation_type(self) -> FoundationType:
        """Type of foundation."""
        return self._foundation_type

    @foundation_type.setter
    @validate_func_args
    def foundation_type(
            self,
            val: Annotated[FoundationType, MustBeMemberOf(FoundationType)]
    ):
        self._foundation_type = val

    @property
    def effective_width(self) -> float:
        """Returns the effective width of the foundation footing (m)."""
        return self.width - 2.0 * self.eccentricity

    def footing_params(self) -> tuple[float, float, Shape]:
        """Returns the `effective_width`, `length`, and `footing_shape`
        of the foundation footing.
        """
        width, length, shape = (
            self.effective_width, self.length, self.footing_shape)

        if not isclose(width, length) and shape != Shape.STRIP:
            shape = Shape.RECTANGLE

        return width, length, shape


@validate_func_args
def create_foundation(
        depth: float,
        width: float,
        length: Optional[float] = None,
        eccentricity: float = 0.0,
        load_angle: float = 0.0,
        ground_water_level: Optional[float] = None,
        foundation_type: FoundationType = "pad",
        shape: Annotated[Shape | str, MustBeMemberOf(Shape)] = "square",
) -> Foundation:
    r"""A factory function that encapsulate the creation of a foundation.

    :param depth: Depth of foundation (m).
    :param width: Width of foundation footing. In the case of a circular
                  footing, it refers to the footing diameter (m).
    :param length: Length of foundation footing (m), defaults to None.
    :param eccentricity: The deviation of the foundation load from the
                         center of gravity of the foundation footing (m),
                         defaults to 0.0. This means that the foundation
                         load aligns with the center of gravity of the
                         foundation footing .
    :param load_angle: Inclination of the applied load with the  vertical
                           (:math:`\alpha^{\circ}`), defaults to 0.0.
    :param ground_water_level: Depth of the water below ground level (m),
                               defaults to None.
    :param foundation_type: Type of foundation footing, defaults to
                            :py:enum:mem:`~FoundationType.PAD`.
    :param shape: Shape of foundation footing, defaults to
                  :py:enum:mem:`~Shape.SQUARE`
    :raises ValueError: Raised when length is not provided for a
                        rectangular footing.
    :raises ValidationError: Raised if an invalid footing shape is
                             provided.
    """

    shape = Shape(str(shape).casefold())

    if shape is Shape.STRIP:
        footing_size = StripFooting(width=width)
    elif shape is Shape.SQUARE:
        footing_size = SquareFooting(width=width)
    elif shape is Shape.CIRCLE:
        footing_size = CircularFooting(diameter=width)
    else:  # RECTANGLE
        if not length:
            msg = "Length of rectangular footing must be provided."
            raise ValueError(msg)
        footing_size = RectangularFooting(width=width, length=length)

    return Foundation(
        depth=depth,
        eccentricity=eccentricity,
        load_angle=load_angle,
        ground_water_level=ground_water_level,
        foundation_type=foundation_type,
        footing_size=footing_size,
    )
