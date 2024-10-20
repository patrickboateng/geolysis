from geolysis.core._config.config import UnitSystem

from .abc_4_soils.abc_4_cohl_soils import (
    BowlesABC4MatFoundation,
    BowlesABC4PadFoundation,
    MeyerhofABC4MatFoundation,
    MeyerhofABC4PadFoundation,
    TerzaghiABC4MatFoundation,
    TerzaghiABC4PadFoundation,
)
from .ubc_4_soils.hansen_ubc import HansenUltimateBearingCapacity
from .ubc_4_soils.terzaghi_ubc import (
    TerzaghiUBC4CircFooting,
    TerzaghiUBC4RectFooting,
    TerzaghiUBC4SquareFooting,
    TerzaghiUBC4StripFooting,
)
from .ubc_4_soils.vesic_ubc import VesicUltimateBearingCapacity

#: Default unit for bearing capacity of soil.
DEFAULT_UNIT = UnitSystem.SI.Pressure
