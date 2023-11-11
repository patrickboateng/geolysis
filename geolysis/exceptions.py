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


class PSDValueError(ArithmeticError):
    """Exception raised when soil aggregates does not approximately
    sum to 100%.
    """


class AllowableSettlementError(ValueError):
    """Exception raised when allowable settlement is greater than
    ``25.4mm``.
    """


class EngineerTypeError(TypeError):
    """Exception raised when a particular engineer is not allowed."""


class FootingShapeError(TypeError):
    """Exception raised when footing shape is not allowed."""
