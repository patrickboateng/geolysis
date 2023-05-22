class PSDValueError(ArithmeticError):
    """Exception raised when soil aggregates does not approximately sum to
    100%."""


class PIValueError(ArithmeticError):
    """Exception raised when ``PI`` is not equal to ``LL - PL``."""


class SoilTypeError(TypeError):
    """Exception raised when an invalid soil type is specified."""


class AllowableSettlementError(ValueError):
    """Exception raised when allowable settlement is greater than ``25.4mm``."""
