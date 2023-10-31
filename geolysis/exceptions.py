"""
.. currentmodule:: geolab.exceptions

=====================================
Exceptions (:mod:`geolab.exceptions`)
=====================================

.. autosummary:: 

    PSDValueError
    PIValueError
    AllowableSettlementError
    EngineerTypeError

"""


class PSDValueError(ArithmeticError):
    """Exception raised when soil aggregates does not approximately sum to
    100%.
    """


class PIValueError(ArithmeticError):
    """Exception raised when ``PI`` is not equal to ``LL - PL``."""


class AllowableSettlementError(ValueError):
    """Exception raised when allowable settlement is greater than ``25.4mm``."""


class EngineerTypeError(TypeError):
    """Exception raise when a particular engineer is not allowed."""
