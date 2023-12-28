import enum

__version__ = "0.2.0"
ERROR_TOLERANCE = 0.01


class GeotechEng(enum.IntEnum):
    """Represents a set of ``Geotechnical Engineers``."""

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


# Make it possible to write geolab.BAZARAA after importing
# or running geolab.
# import geolab
# from geolab import GeotechEng
# geolab.BAZARAA is GeotechEng.BAZARAA -> True
globals().update(GeotechEng.__members__)
