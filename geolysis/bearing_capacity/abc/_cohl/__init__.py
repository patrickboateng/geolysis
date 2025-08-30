"""This package provides a factory function and utilities for creating
allowable bearing capacity calculations using methods like Bowles, Meyerhof,
and Terzaghi for various foundation types and shapes.
"""

import enum
from typing import Optional, Annotated

from func_validator import MustBeMemberOf, validate_func_args

from geolysis.foundation import FoundationType, Shape, create_foundation
from geolysis.utils import AbstractStrEnum, inf
from ._core import AllowableBearingCapacity
from .bowles_abc import BowlesABC4MatFoundation, BowlesABC4PadFoundation
from .meyerhof_abc import MeyerhofABC4MatFoundation, MeyerhofABC4PadFoundation
from .terzaghi_abc import TerzaghiABC4MatFoundation, TerzaghiABC4PadFoundation


class ABCType(AbstractStrEnum):
    """Enumeration of available allowable bearing capacity types."""

    BOWLES = enum.auto()
    MEYERHOF = enum.auto()
    TERZAGHI = enum.auto()


@validate_func_args
def create_abc_4_cohesionless_soils(
    corrected_spt_n_value: float,
    tol_settlement: float,
    depth: float,
    width: float,
    length: Optional[float] = None,
    eccentricity: float = 0.0,
    ground_water_level: float = inf,
    shape: Shape | str = "square",
    foundation_type: Annotated[
        FoundationType | str, MustBeMemberOf(FoundationType)
    ] = "pad",
    abc_type: Annotated[ABCType | str, MustBeMemberOf(ABCType)] = "bowles",
) -> AllowableBearingCapacity:
    r"""A factory function that encapsulate the creation of  allowable
     bearing capacities.

     **Bowles allowable bearing capacity for pad foundation equation is
     found below**:

     $$
     q_a(kPa) = 19.16(N_1)_{55} f_d\left(\dfrac{S}{25.4}\right),
                \ B \ \le \ 1.2m
     $$

     $$
     q_a(kPa) = 11.98(N_1)_{55}\left(\dfrac{3.28B + 1}{3.28B} \right)^2
                     f_d \left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m
     $$

     $$
     f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
     $$

     **Bowles allowable bearing capacity for mat foundation equation is
     found below**:

     $$
     q_a(kPa) = 11.98(N_1)_{55}f_d\left(\dfrac{S}{25.4}\right)
     $$

     $$
     f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
     $$

     **Meyerhof allowable bearing capacity for pad foundation equation is
     found below**:

     $$
     q_a(kPa) = 12N f_d\left(\dfrac{S}{25.4}\right), \ B \ \le 1.2m
     $$

     $$
     q_a(kPa) = 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d\left(
                \dfrac{S}{25.4}\right), \ B \ \gt 1.2m
     $$

     $$
     f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
     $$

     **Meyerhof allowable bearing capacity for mat foundation equation is
     found below**:

     $$
     q_a(kPa) = 8 N f_d\left(\dfrac{S}{25.4}\right)
     $$

     $$
     f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
     $$

     **Terzaghi allowable bearing capacity for pad foundation equation is
     found below**:

     $$
     q_a(kPa) = 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right),
                 \ B \ \le 1.2m
     $$

     $$
     q_a(kPa) = 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}
                 {c_w f_d}\left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m
     $$

     $$
     f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25
     $$

     $$
     c_w = 2 - \frac{D_w}{2B} \le 2, D_w \gt D_f
     $$

     $$
     c_w = 2 - \frac{D_f}{2B} \le 2, D_w \le D_f
     $$

     **Terzaghi allowable bearing capacity for mat foundation equation is
     found below**:

     $$
     q_a(kPa) = 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)
     $$

     $$
     f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25
     $$

     $$
     c_w = 2 - \frac{D_w}{2B} \le 2, D_w \gt D_f
     $$

     $$
     c_w = 2 - \frac{D_f}{2B} \le 2, D_w \le D_f
     $$

    | SYMBOL      | DESCRIPTION                               | UNIT    |
    |-------------|-------------------------------------------|---------|
    | $q_a$     | Allowable bearing capacity                | $kPa$ |
    | $N$       | Corrected SPT N-value                     | —       |
    | $f_d$     | Depth factor                              | —       |
    | $c_w$     | Water correction factor                   | —       |
    | $S$       | Tolerable settlement                      | $mm$  |
    | $B$       | Width of foundation footing               | $m$   |
    | $D_f$     | Depth of foundation footing               | $m$   |
    | $D_w$     | Depth of water below ground level         | $m$   |


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
    :param abc_type: Type of allowable bearing capacity calculation to
                     apply.

    :raises ValidationError: Raised if `abc_type` or `foundation_type`
                              is not supported.
    :raises ValidationError: Raised if an invalid footing `shape` is
                              provided.
    :raises ValueError: Raised when `length` is not provided for a
                         rectangular footing.
    """
    abc_type = ABCType(abc_type)
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

    abc_class = _get_allowable_bearing_capacity(abc_type, fnd_size.foundation_type)
    return abc_class(
        corrected_spt_n_value=corrected_spt_n_value,
        tol_settlement=tol_settlement,
        foundation_size=fnd_size,
    )


def _get_allowable_bearing_capacity(abc_type: ABCType, foundation_type: FoundationType):
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
        },
    }
    return abc_classes[abc_type][foundation_type]
