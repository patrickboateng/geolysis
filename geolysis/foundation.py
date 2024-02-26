from abc import abstractproperty
from typing import Protocol

from geolysis.utils import FloatOrInt

__all__ = [
    "CircularFooting",
    "SquareFooting",
    "RectangularFooting",
    "FoundationSize",
]


class _FootingShape(Protocol):

    @abstractproperty
    def width(self) -> FloatOrInt: ...

    @width.setter
    def width(self, __val: FloatOrInt): ...

    @abstractproperty
    def length(self) -> FloatOrInt: ...

    @length.setter
    def length(self, __val: FloatOrInt): ...


class CircularFooting:
    """
    Circular Footing Size.

    :param FloatOrInt width: Diameter of foundation footing. (m)

    .. note::

        The ``width`` and ``length`` properties refer to the diameter
        of the circular footing. This is to make it compatible with
        the protocol square and rectangular footing follow.
    """

    def __init__(self, width: FloatOrInt) -> None:
        self._width = width

    @property
    def width(self) -> FloatOrInt:
        """
        Diameter of foundation footing. (m)
        """
        return self._width

    @width.setter
    def width(self, __val: FloatOrInt):
        self.width = __val

    @property
    def length(self) -> FloatOrInt:
        """
        Diameter of foundation footing. (m)
        """
        return self._width

    @length.setter
    def length(self, __val: FloatOrInt):
        self.width = __val


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
        self.width = __val


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

        .. note::

            In the case of circular footing ``width`` refers to the
            diameter.
        """
        return self.footing_shape.width

    @width.setter
    def width(self, __val: FloatOrInt):
        self.footing_shape.width = __val

    @property
    def length(self) -> FloatOrInt:
        """
        Length of foundation footing. (m)

        .. note::

            In the case of circular footing ``length`` refers to the
            diameter.
        """
        return self.footing_shape.length

    @length.setter
    def length(self, __val: FloatOrInt):
        self.footing_shape.length = __val
