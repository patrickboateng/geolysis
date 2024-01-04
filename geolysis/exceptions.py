"""
.. currentmodule:: geolab.exceptions

=====================================
Exceptions (:mod:`geolab.exceptions`)
=====================================

.. autosummary:: 

    PSDValueError
    AllowableSettlementError
    EngineerTypeError
    FootingShapeError

"""
from statistics import StatisticsError


class PSDValueError(ArithmeticError):
    pass


class AllowableSettlementError(ValueError):
    pass


class SoilClassificationError(ValueError):
    pass


class OverburdenPressureError(ValueError):
    pass


class EngineerTypeError(TypeError):
    pass


class EstimatorError(ValueError):
    pass


class FootingShapeError(TypeError):
    pass
