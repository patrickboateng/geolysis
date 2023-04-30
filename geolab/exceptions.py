class PSDValueError(ArithmeticError):
    """Exception raised when soil aggregates does not approximately sum to 100%."""


class PIValueError(ArithmeticError):
    """Exception raised when `PI != LL - PL`.

    - PI: Plasticity Index
    - LL: Liquid Limit
    - PL: Plastic Limit
    """


class FoundationTypeError(TypeError):
    """Exception raised when an invalid foundation type is provided."""


class AllowableSettlementError(ValueError):
    """Exception raised when allowable settlement is greater than `25.4mm`"""
