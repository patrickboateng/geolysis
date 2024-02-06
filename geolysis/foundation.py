from typing import TypeAlias

from geolysis.utils import SupportsFloatOrIndex

__all__ = [
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
    "FoundationSize",
]


class CircularFooting:
    """
    Circular Footing Size.

    :param float diameter: Diameter of foundation footing. (m)
    """

    def __init__(self, diameter: SupportsFloatOrIndex) -> None:
        self._diameter = diameter

    @property
    def diameter(self) -> SupportsFloatOrIndex:
        """
        Diameter of foundation footing. (m)
        """
        return self._diameter

    @diameter.setter
    def diameter(self, __val: SupportsFloatOrIndex):
        self._diameter = __val

    @property
    def width(self) -> SupportsFloatOrIndex:
        """
        Diameter of foundation footing. (m)
        """
        return self._diameter

    @width.setter
    def width(self, __val: SupportsFloatOrIndex):
        self.diameter = __val


class SquareFooting:
    """
    Square Footing Size.

    :param SupportFloatOrIndex width: Width of foundation footing. (m)
    """

    def __init__(self, width: SupportsFloatOrIndex):
        self._width = width
        self._length = width

    @property
    def width(self) -> SupportsFloatOrIndex:
        """
        Width of foundation footing. (m)
        """
        return self._width

    @width.setter
    def width(self, __val: SupportsFloatOrIndex):
        self._width = __val
        self._length = __val

    @property
    def length(self) -> SupportsFloatOrIndex:
        """
        Length of foundation footing. (m)
        """
        return self._length

    @length.setter
    def length(self, __val: SupportsFloatOrIndex):
        self.width = __val  # This will set the _width and _length attributes


class RectangularFooting:
    """
    Rectangular Footing Size.

    :param SupportFloatOrIndex length: Length of foundation footing. (m)
    :param SupportFloatOrIndex width: Width of foundation footing. (m)
    """

    def __init__(
        self,
        width: SupportsFloatOrIndex,
        length=SupportsFloatOrIndex,
    ) -> None:
        self._width = width
        self._length = length

    @property
    def width(self) -> SupportsFloatOrIndex:
        """
        Width of foundation footing. (m)
        """
        return self._width

    @width.setter
    def width(self, __val: SupportsFloatOrIndex):
        self._width = __val

    @property
    def length(self) -> SupportsFloatOrIndex:
        """
        Length of foundation footing. (m)
        """
        return self._length

    @length.setter
    def length(self, __val: SupportsFloatOrIndex):
        self._length = __val


_FootingShape: TypeAlias = SquareFooting | RectangularFooting | CircularFooting


class FoundationSize:
    """
    A simple class representing a foundation structure.

    :param float depth: Depth of foundation footing. (m)
    :param FootingShape footing_shape: Represents the shape of the foundation footing.
    """

    def __init__(
        self,
        depth: SupportsFloatOrIndex,
        footing_shape: _FootingShape,
    ) -> None:
        self._depth = depth
        self.footing_shape = footing_shape

    @property
    def depth(self) -> SupportsFloatOrIndex:
        """
        Depth of foundation footing. (m)
        """
        return self._depth

    @depth.setter
    def depth(self, __val: SupportsFloatOrIndex):
        self._depth = __val

    @property
    def width(self) -> SupportsFloatOrIndex:
        """
        Width of foundation footing. (m)
        """
        return self.footing_shape.width

    @width.setter
    def width(self, __val: SupportsFloatOrIndex):
        self.footing_shape.width = __val

    @property
    def length(self) -> SupportsFloatOrIndex:
        """
        Length of foundation footing. (m)

        :raises AttributeError: Raises error if footing shape does not have a length
            attribute.
        """
        if isinstance(self.footing_shape, (SquareFooting, RectangularFooting)):
            return self.footing_shape.length

        else:
            err_msg = (
                f"{type(self.footing_shape)} have no attribute named length"
            )
            raise AttributeError(err_msg)
