import enum
from typing import Annotated, Optional

from func_validator import MustBeMemberOf, validate_params

from geolysis.foundation import FoundationType, Shape, create_foundation
from geolysis.utils import AbstractStrEnum, inf

from ._core import AllowableBearingCapacity
from .bowles_abc import BowlesABC4MatFoundation, BowlesABC4PadFoundation
from .meyerhof_abc import MeyerhofABC4MatFoundation, MeyerhofABC4PadFoundation
from .terzaghi_abc import TerzaghiABC4MatFoundation, TerzaghiABC4PadFoundation


class ABCMethod(AbstractStrEnum):
    """Enumeration of allowable bearing capacity calculation methods.

    Each member represents a different method for determining
    the allowable bearing capacity of soil.
    """

    BOWLES = enum.auto()
    """Bowles's method for calculating allowable bearing capacity"""

    MEYERHOF = enum.auto()
    """Meyerhof's method for calculating allowable bearing capacity"""

    TERZAGHI = enum.auto()
    """Terzaghi's method for calculating allowable bearing capacity"""


abc_classes = {
    ABCMethod.BOWLES: {
        FoundationType.PAD: BowlesABC4PadFoundation,
        FoundationType.MAT: BowlesABC4MatFoundation,
    },
    ABCMethod.MEYERHOF: {
        FoundationType.PAD: MeyerhofABC4PadFoundation,
        FoundationType.MAT: MeyerhofABC4MatFoundation,
    },
    ABCMethod.TERZAGHI: {
        FoundationType.PAD: TerzaghiABC4PadFoundation,
        FoundationType.MAT: TerzaghiABC4MatFoundation,
    },
}


@validate_params
def create_abc_4_cohesionless_soils(
    corrected_spt_n_value: float,
    tol_settlement: float,
    depth: float,
    width: float,
    length: Optional[float] = None,
    eccentricity: float = 0.0,
    ground_water_level: float = inf,
    shape: Shape | str = "square",
    foundation_type: FoundationType | str = "pad",
    abc_method: Annotated[ABCMethod | str, MustBeMemberOf(ABCMethod)] = "bowles",
) -> AllowableBearingCapacity:
    r"""A factory function that encapsulate the creation of  allowable
     bearing capacities.

    :param corrected_spt_n_value: The corrected SPT N-value.
    :param tol_settlement: Tolerable settlement of foundation (mm).
    :param depth: Depth of foundation (m).
    :param width: Width of foundation footing (m).
    :param length: Length of foundation footing (m).
    :param eccentricity: The deviation of the foundation load from the
                         center of gravity of the foundation footing (m).
    :param ground_water_level: Depth of water below ground level (m).
    :param shape: Shape of foundation footing
    :param foundation_type: Type of foundation.
    :param abc_method: Type of allowable bearing capacity calculation to
                     apply.
    """
    abc_method = ABCMethod(abc_method)
    foundation_type = FoundationType(foundation_type)

    # exception from create_foundation will automaatically propagate
    # no need to catch and handle it.
    fnd_size = create_foundation(
        depth=depth,
        width=width,
        length=length,
        eccentricity=eccentricity,
        ground_water_level=ground_water_level,
        foundation_type=foundation_type,
        shape=shape,
    )
    abc_class = abc_classes[abc_method][foundation_type]

    return abc_class(
        corrected_spt_n_value=corrected_spt_n_value,
        tol_settlement=tol_settlement,
        foundation_size=fnd_size,
    )
