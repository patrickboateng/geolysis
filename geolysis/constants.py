import enum

ERROR_TOL = 0.01

GRAVEL = "G"
SAND = "S"
CLAY = "C"
SILT = "M"
WELL_GRADED = "W"
POORLY_GRADED = "P"
ORGANIC = "O"
LOW_PLASTICITY = "L"
HIGH_PLASTICITY = "H"


class EngineerTypeError(TypeError):
    pass


class GeotechEng(enum.IntEnum):
    """Represents a set of names of Geotechnical Engineers whose theories have
    been utilised in developing ``geolysis``.
    """

    BAZARAA = 1
    GIBBS = 2
    HANSEN = 3
    HOUGH = 4
    KULLHAWY = 5
    LIAO = 6
    MEYERHOF = 7
    SKEMPTON = 8
    STROUD = 9
    TERZAGHI = 10
    VESIC = 11
    WOLFF = 12
    PECK = 13
