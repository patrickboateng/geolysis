import enum

__version__ = "0.1.3"
ERROR_TOLERANCE = 0.01
DECIMAL_PLACES = 3


class GeotechEng(enum.IntFlag):
    """Represents a set of ``Geotechnical Engineers``."""

    BAZARAA = 1
    GIBBS = 2
    HANSEN = 4
    HOUGH = 8
    KULLHAWY = 16
    LIAO = 32
    MEYERHOF = 64
    SKEMPTON = 128
    STROUD = 256
    TERZAGHI = 512
    VESIC = 1024
    WOLFF = 2048

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


# Make it possible to write geolab.BAZARAA after importing
# or running geolab.
# import geolab
# from geolab import GeotechEng
# geolab.BAZARAA is GeotechEng.BAZARAA returns True
globals().update(GeotechEng.__members__)
