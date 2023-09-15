""""""

import enum

__version__ = "0.1.0"
ERROR_TOLERANCE = 0.01
DECIMAL_PLACES = 3


class GeotechEng(enum.IntEnum):
    BAZARAA = enum.auto()
    GIBBS = enum.auto()
    HANSEN = enum.auto()
    HOUGH = enum.auto()
    LIAO = enum.auto()
    MEYERHOF = enum.auto()
    WOLFF = enum.auto()
    SKEMPTON = enum.auto()
    STROUD = enum.auto()
    TERZAGHI = enum.auto()
    VESIC = enum.auto()
    KULLHAWY = enum.auto()

    def __str__(self) -> str:
        return self.name


globals().update(GeotechEng.__members__)
