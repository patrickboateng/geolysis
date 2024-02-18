from typing import TypeAlias

from geolysis.utils import FloatOrInt

__all__ = [
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
    "FoundationSize",
]


class CircularFooting:
    """
    Circular Footing Size.

    :param FloatOrInt diameter: Diameter of foundation footing. (m)
    """

    def __init__(self, diameter: FloatOrInt) -> None:
        self._diameter = diameter

    @property
    def diameter(self) -> FloatOrInt:
        """
        Diameter of foundation footing. (m)
        """
        return self._diameter

    @diameter.setter
    def diameter(self, __val: FloatOrInt):
        self._diameter = __val

    @property
    def width(self) -> FloatOrInt:
        """
        Diameter of foundation footing. (m)
        """
        return self._diameter

    @width.setter
    def width(self, __val: FloatOrInt):
        self.diameter = __val


class SquareFooting:
    """
    Square Footing Size.

    :param FloatOrInt width: Width of foundation footing. (m)
    """

    def __init__(self, width: FloatOrInt):
        self._width = width
        self._length = width

    @property
    def width(self) -> FloatOrInt:
        """
        Width of foundation footing. (m)
        """
        return self._width

    @width.setter
    def width(self, __val: FloatOrInt):
        self._width = __val
        self._length = __val

    @property
    def length(self) -> FloatOrInt:
        """
        Length of foundation footing. (m)
        """
        return self._length

    @length.setter
    def length(self, __val: FloatOrInt):
        self.width = __val  # This will set the _width and _length attributes


class RectangularFooting:
    """
    Rectangular Footing Size.

    :param FloatOrInt width: Width of foundation footing. (m)
    :param FloatOrInt length: Length of foundation footing. (m)
    """

    def __init__(
        self,
        width: FloatOrInt,
        length: FloatOrInt,
    ) -> None:
        self._width = width
        self._length = length

    @property
    def width(self) -> FloatOrInt:
        """
        Width of foundation footing. (m)
        """
        return self._width

    @width.setter
    def width(self, __val: FloatOrInt):
        self._width = __val

    @property
    def length(self) -> FloatOrInt:
        """
        Length of foundation footing. (m)
        """
        return self._length

    @length.setter
    def length(self, __val: FloatOrInt):
        self._length = __val


_FootingShape: TypeAlias = SquareFooting | RectangularFooting | CircularFooting


class FoundationSize:
    """
    A simple class representing a foundation structure.

    :param FloatOrInt depth: Depth of foundation footing. (m)
    :param _FootingShape footing_shape: Represents the shape of the
        foundation footing.
    """

    def __init__(
        self,
        depth: FloatOrInt,
        footing_shape: _FootingShape,
    ) -> None:
        self._depth = depth
        self.footing_shape = footing_shape

    @property
    def depth(self) -> FloatOrInt:
        """
        Depth of foundation footing. (m)
        """
        return self._depth

    @depth.setter
    def depth(self, __val: FloatOrInt):
        self._depth = __val

    @property
    def width(self) -> FloatOrInt:
        """
        Width of foundation footing. (m)
        """
        return self.footing_shape.width

    @width.setter
    def width(self, __val: FloatOrInt):
        self.footing_shape.width = __val

    @property
    def length(self) -> FloatOrInt:
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
