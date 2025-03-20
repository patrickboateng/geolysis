""" Allowable bearing capacity package for cohesionless soils.

Enums
=====

.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    ABCType

Functions
=========

.. autosummary::
    :toctree: _autosummary

    create_allowable_bearing_capacity
"""

import enum
from typing import Optional

from geolysis.foundation import FoundationType, Shape, create_foundation
from geolysis.utils import enum_repr, inf

from ._core import AllowableBearingCapacity
from .bowles_abc import BowlesABC4MatFoundation, BowlesABC4PadFoundation
from .meyerhof_abc import MeyerhofABC4MatFoundation, MeyerhofABC4PadFoundation
from .terzaghi_abc import TerzaghiABC4MatFoundation, TerzaghiABC4PadFoundation


@enum_repr
class ABCType(enum.StrEnum):
    """Enumeration of available allowable bearing capacity types."""
    BOWLES = enum.auto()
    MEYERHOF = enum.auto()
    TERZAGHI = enum.auto()


def create_allowable_bearing_capacity(corrected_spt_n_value: float,
                                      tol_settlement: float,
                                      depth: float,
                                      width: float,
                                      length: Optional[float] = None,
                                      eccentricity: float = 0.0,
                                      ground_water_level: float = inf,
                                      shape: Shape | str = Shape.SQUARE,
                                      foundation_type: FoundationType | str =
                                      FoundationType.PAD,
                                      abc_type: Optional[
                                          ABCType | str] = None,
                                      ) -> AllowableBearingCapacity:
    """ A factory function that encapsulate the creation of  allowable bearing
    capacities.

    :param corrected_spt_n_value: The corrected SPT N-value.
    :type corrected_spt_n_value: float

    :param tol_settlement: Tolerable settlement of foundation (mm).
    :type tol_settlement: float

    :param depth: Depth of foundation (m).
    :type depth: float

    :param width: Width of foundation footing (m).
    :type width: float

    :param length: Length of foundation footing (m).
    :type length: float, optional

    :param eccentricity: The deviation of the foundation load from the center 
                         of gravity of the foundation footing (m), defaults to
                         0.0. This means that the foundation load aligns with
                         the center of gravity of the foundation footing.
    :type eccentricity: float, optional

    :param ground_water_level: Depth of water below ground level (m).
    :type ground_water_level: float, optional

    :param shape: Shape of foundation footing, defaults to
                  :attr:`~geolysis.foundation.Shape.SQUARE`.
    :type shape: str, optional

    :param foundation_type: Type of foundation, defaults to "pad".
    :type foundation_type: FoundationType | str, optional

    :param abc_type: Type of allowable bearing capacity calculation to apply.
                     Available values can be found in :class:`ABCType`,
                     defaults to None.
    :type abc_type:  ABCType | str, optional

    :raises ValueError: Raised if ``abc_type`` or ``foundation_type`` is not
                        supported.
    :raises ValueError: Raised when ``length`` is not provided for a rectangular
                        footing.
    :raises ValueError: Raised if an invalid footing ``shape`` is provided.
    """
    msg = (f"{abc_type=} is not supported, Supported "
           f"types are: {list(ABCType)}")

    if abc_type is None:
        raise ValueError(msg)

    try:
        abc_type = ABCType(str(abc_type).casefold())
    except ValueError as e:
        raise ValueError(msg) from e

    msg = (f"{foundation_type=} is not supported, Supported "
           f"types are: {list(FoundationType)}")

    try:
        foundation_type = FoundationType(str(foundation_type).casefold())
    except ValueError as e:
        raise ValueError(msg) from e

    # exception from create_foundation will automaatically propagate
    # no need to catch and handle it.
    fnd_size = create_foundation(depth=depth,
                                 width=width,
                                 length=length,
                                 eccentricity=eccentricity,
                                 ground_water_level=ground_water_level,
                                 foundation_type=foundation_type,
                                 shape=shape)
    abc_classes = {
        ABCType.BOWLES: {
            FoundationType.PAD: BowlesABC4PadFoundation,
            FoundationType.MAT: BowlesABC4MatFoundation,
        },
        ABCType.MEYERHOF: {
            FoundationType.PAD: MeyerhofABC4PadFoundation,
            FoundationType.MAT: MeyerhofABC4MatFoundation,
        },
        ABCType.TERZAGHI: {
            FoundationType.PAD: TerzaghiABC4PadFoundation,
            FoundationType.MAT: TerzaghiABC4MatFoundation,
        }
    }

    abc_class = abc_classes[abc_type][fnd_size.foundation_type]
    abc = abc_class(corrected_spt_n_value=corrected_spt_n_value,
                    tol_settlement=tol_settlement,
                    foundation_size=fnd_size)
    return abc
