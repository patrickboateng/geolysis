class ValidationError(ValueError):
    """Exception raised when a validation error occurs."""


class SettlementError(ValueError):
    """Raised when tolerable settlement is greater than the maximum
    allowable settlement.
    """
