from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Literal, Optional, Protocol

from geolysis.constants import GDict
from geolysis.constants import UnitRegistry as ureg
from geolysis.utils import FloatOrInt

__all__ = [
    "create_footing",
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
    "FootingSize",
    "FoundationSize",
]


class FootingCreationError(TypeError):
    pass


class _FootingShape(Protocol):

    @property
    @abstractmethod
    def width(self) -> FloatOrInt: ...

    @width.setter
    def width(self, __val: FloatOrInt): ...

    @property
    @abstractmethod
    def length(self) -> FloatOrInt: ...

    @length.setter
    def length(self, __val: FloatOrInt): ...


@dataclass
class CircularFooting:
    """A class representation of circular footing.

    Parameters
    ----------
    width : float, unit=metre
        Diameter of foundation footing.

    Attributes
    ----------
    width : float, unit=metre
    length : float, unit=metre
    UNITS : GDict
        Unit registry for attributes and values returned from
        functions.

    See Also
    --------
    SquareFooting, RectangularFooting

    Notes
    -----
    The ``width`` and ``length`` properties refer to the diameter
    of the circular footing. This is to make it compatible with the
    protocol square and rectangular footing follow.
    """

    width: float
    UNITS: ClassVar = GDict(width=ureg.m, length=ureg.m)

    @property
    def length(self) -> float:
        """Diameter of foundation footing."""
        return self.width

    @length.setter
    def length(self, __val: float):
        self.width = __val


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
    UNITS : GDict
        Unit registry for attributes and values returned from
        functions.

    See Also
    --------
    CircularFooting, RectangularFooting
    """

    width: float
    UNITS: ClassVar = GDict(width=ureg.m, length=ureg.m)

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
    width : float, unit=metre
        Width of foundation footing.
    length : float, unit=metre
        Length of foundation footing.

    Attributes
    ----------
    width : float, unit=metre
    length : float, unit=metre
    UNITS : GDict
        Unit registry for attributes and values returned from
        functions.

    See Also
    --------
    CircularFooting, SquareFooting
    """

    width: float
    length: float
    UNITS: ClassVar = GDict(width=ureg.m, length=ureg.m)


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
    UNITS : GDict
        Unit registry for attributes and values returned from
        functions.

    See Also
    --------
    FoundationSize
    """

    thickness: FloatOrInt
    footing_shape: _FootingShape
    UNITS: ClassVar = GDict(thickness=ureg.m, width=ureg.m, length=ureg.m)

    @property
    def width(self) -> FloatOrInt:
        """Width of foundation footing."""
        return self.footing_shape.width

    @width.setter
    def width(self, __val: FloatOrInt):
        self.footing_shape.width = __val

    @property
    def length(self) -> FloatOrInt:
        """Length of foundation footing."""
        return self.footing_shape.length

    @length.setter
    def length(self, __val: FloatOrInt):
        self.footing_shape.length = __val


@dataclass
class FoundationSize:
    """A simple class representing a foundation structure.

    Parameters
    ----------
    depth : float, unit=metre
        Depth of foundation footing.
    footing_shape : _FootingShape
        Represents the shape of the foundation footing.

    Attributes
    ----------
    depth : float, unit=metre
    thickness : float, unit=metre
    width : float, unit=metre
    length : float, unit=metre
    footing_size : FootingSize
    UNITS : GDict
        Unit registry for attributes and values returned from
        functions.

    See Also
    --------
    FootingSize
    """

    depth: float
    footing_size: FootingSize
    UNITS: ClassVar = GDict(
        depth=ureg.m, thickness=ureg.m, width=ureg.m, length=ureg.m
    )

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


def create_footing(
    thickness: float,
    width: float,
    length: Optional[float] = None,
    footing_type: Literal["square", "rectangular", "circular"] = "square",
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
    footing_type : {"square", "rectangular", "circular"}, default="square"
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
        >>> from geolysis.foundation import create_footing
        >>> square_footing = create_footing(thickness=0.3, width=1.2,
        ...                                 footing_type="square")
        >>> square_footing
        FootingSize(thickness=0.3, footing_shape=SquareFooting(width=1.2))
        >>> square_footing.footing_shape
        SquareFooting(width=1.2)
        >>> square_footing.width
        1.2
        >>> square_footing.length
        1.2
    """
    footing_shape: _FootingShape

    if footing_type == "square":
        footing_shape = SquareFooting(width=width)
    elif footing_type == "circular":
        footing_shape = CircularFooting(width=width)
    elif footing_type == "rectangular" and length is not None:
        footing_shape = RectangularFooting(width=width, length=length)
    else:
        err_msg = (
            "Supported footing types are square, rectangular, and circular"
            "if rectangular footing is specified, the length parameter should"
            "be a valid value not None"
        )
        raise FootingCreationError(err_msg)

    return FootingSize(thickness=thickness, footing_shape=footing_shape)
