import enum
from typing import Final, Optional, Protocol, cast

import attrs

from geolysis.core.utils import INF, Number

__all__ = ["create_foundation"]


class custom_field:
    def __init__(
        self,
        *,
        ref_attr: str,
        ref_obj: Optional[str] = None,
        doc: Optional[str] = None,
    ):
        self.ref_attr = ref_attr
        self.ref_obj = ref_obj
        self.fget: Final = getattr
        self.fset: Final = setattr
        self.fdel: Final = delattr
        self.__doc__ = doc

    def __get__(self, obj, objtype=None) -> Number:
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
    STRIP = enum.auto()
    CIRCLE = enum.auto()
    SQUARE = enum.auto()
    RECTANGLE = enum.auto()


class FootingSize(Protocol):
    shape_: Shape
    width: float
    length: float


@attrs.define
class StripFooting(FootingSize):
    width: Number = attrs.field(
        converter=float,
        validator=attrs.validators.gt(0.0),
    )
    length: Number = attrs.field(
        default=INF,
        converter=float,
        validator=attrs.validators.gt(0.0),
    )
    shape_: Final[Shape] = attrs.field(
        default=Shape.STRIP,
        init=False,
        on_setattr=attrs.setters.frozen,
    )


@attrs.define
class CircularFooting(FootingSize):
    """A class representation of circular footing.

    :param float diameter: Diameter of foundation footing. (m)

    .. seealso::

        :class:`SquareFooting`, :class:`RectangularFooting`

    Notes
    -----
    The ``width`` and ``length`` properties refer to the diameter
    of the circular footing. This is to make it compatible with the
    protocol square and rectangular footing follow.

    Examples
    --------
    >>> from geolysis.core.foundation import CircularFooting
    >>> circ_footing = CircularFooting(diameter=1.2)
    >>> circ_footing.diameter
    1.2
    >>> circ_footing.width
    1.2
    >>> circ_footing.length
    1.2
    """

    diameter: Number = attrs.field(
        converter=float,
        validator=attrs.validators.gt(0.0),
    )
    width = cast(Number, custom_field(ref_attr="diameter"))
    length = cast(Number, custom_field(ref_attr="diameter"))
    shape_: Final[Shape] = attrs.field(
        default=Shape.CIRCLE,
        init=False,
        on_setattr=attrs.setters.frozen,
    )


@attrs.define
class SquareFooting(FootingSize):
    """A class representation of square footing.

    :param float width: Width of foundation footing. (m)

    .. seealso::

        :class:`CircularFooting`, :class:`RectangularFooting`

    Examples
    --------
    >>> from geolysis.core.foundation import SquareFooting
    >>> sq_footing = SquareFooting(width=1.2)
    >>> sq_footing.width
    1.2
    >>> sq_footing.length
    1.2
    """

    width: Number = attrs.field(
        converter=float,
        validator=attrs.validators.gt(0.0),
    )
    length = cast(Number, custom_field(ref_attr="width"))
    shape_: Final[Shape] = attrs.field(
        default=Shape.SQUARE,
        init=False,
        on_setattr=attrs.setters.frozen,
    )


@attrs.define
class RectangularFooting(FootingSize):
    """A class representation of rectangular footing.

    :param float width: Width of foundation footing. (m)
    :param float length: Length of foundation footing. (m)

    .. seealso::

        :class:`CircularFooting`, :class:`SquareFooting`

    Examples
    --------
    >>> from geolysis.core.foundation import RectangularFooting
    >>> rect_footing = RectangularFooting(width=1.2, length=1.4)
    >>> rect_footing.width
    1.2
    >>> rect_footing.length
    1.4
    """

    width: Number = attrs.field(
        converter=float,
        validator=attrs.validators.gt(0.0),
    )
    length: Number = attrs.field(
        converter=float,
        validator=attrs.validators.gt(0.0),
    )
    shape_: Final[Shape] = attrs.field(
        default=Shape.RECTANGLE,
        init=False,
        on_setattr=attrs.setters.frozen,
    )


@attrs.define
class FoundationSize:
    """A simple class representing a foundation structure.

    :param float depth: Depth of foundation. (m)
    :param FootingSize footing_size: Represents the size of the foundation
        footing.

    .. seealso::

        :class:`FootingSize`

    Examples
    --------
    >>> from geolysis.core.foundation import (
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

    depth: Number = attrs.field(
        converter=float,
        validator=attrs.validators.gt(0.0),
    )
    footing_size: FootingSize = attrs.field()
    eccentricity: Number = attrs.field(
        converter=float,
        default=0.0,
        validator=attrs.validators.ge(0.0),
    )
    width = custom_field(ref_attr="width", ref_obj="footing_size")
    length = custom_field(ref_attr="length", ref_obj="footing_size")
    footing_shape = custom_field(ref_attr="shape_", ref_obj="footing_size")

    @property
    def effective_width(self) -> float:
        return self.width - 2 * self.eccentricity


def create_foundation(
    depth: float,
    width: float,
    length: Optional[float] = None,
    eccentricity: float = 0.0,
    footing_shape: Shape | str = Shape.SQUARE,
) -> FoundationSize:
    """A factory function that encapsulate the creation of a foundation
    footing.

    :param float width: Width of foundation footing (m)
    :param float length: Length of foundation footing, defaults to None. (m)
    :param Shape | str footing_shape: Shape of foundation footing, defaults to
        :class:`Shape.SQUARE` or "square"

    :raises FootingCreationError: Exception raised when footing is not created
        successfully.

    :return: Size of foundation footing.
    :rtype: FootingSize

    Examples
    --------

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
            err_msg = "The length of the footing must be provided"
            raise ValueError(err_msg)
        footing_size = RectangularFooting(width=width, length=length)
    else:
        err_msg = (
            "Supported footing shapes are STRIP,"
            " SQUARE, RECTANGLE, and CIRCLE"
        )
        raise TypeError(err_msg)

    return FoundationSize(
        depth=depth,
        eccentricity=eccentricity,
        footing_size=footing_size,
    )
