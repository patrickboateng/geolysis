from collections import UserString
from typing import Any


class _ErrorMsg(UserString):
    def __init__(self, param_name: str = None,
                 param_value: Any = None,
                 symbol: str = None,
                 param_value_bound: Any = None,
                 msg: str = None):
        if not msg:
            msg = f"{param_name}: {param_value!r} must be {symbol} {param_value_bound}"

        self.param_name = param_name
        self.param_value = param_value
        self.symbol = symbol
        self.param_value_bound = param_value_bound
        self.msg = msg

        super().__init__(msg)

    def __add__(self, other):
        if isinstance(other, str):
            self.data = self.data + other
            self.msg = self.data
            return self
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, str):
            self.data = other + self.data
            self.msg = self.data
            return self
        return NotImplemented


class ErrorMsg(_ErrorMsg):
    pass


class ValidationError(ValueError):
    """Exception raised when a validation error occurs."""

    def __init__(self, error: ErrorMsg):
        super().__init__(error)
        self.error = error


class SettlementError(ValidationError):
    """Raised when tolerable settlement is greater than the maximum
    allowable settlement.
    """
