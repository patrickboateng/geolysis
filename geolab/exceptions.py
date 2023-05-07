class PSDValueError(ArithmeticError):
    """Exception raised when soil aggregates does not approximately sum to
    100%."""


class PIValueError(ArithmeticError):
    """Exception raised when `PI` is not equal to `LL - PL`.

    - PI: Plasticity Index
    - LL: Liquid Limit
    - PL: Plastic Limit
    """


class SoilTypeError(TypeError):
    """Exception raised when an invalid soil type is provided"""


class FoundationTypeError(TypeError):
    """Exception raised when an invalid foundation type is provided."""


class AllowableSettlementError(ValueError):
    """Exception raised when allowable settlement is greater than `25.4mm`"""
