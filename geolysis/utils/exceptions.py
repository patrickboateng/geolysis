from typing import Any
from collections import UserString


class _ErrorMsg(UserString):
    def __init__(self, name: str = None,
                 val: Any = None,
                 symbol: str = None,
                 bound: str = None,
                 msg: str = None):
        if not msg:
            msg = f"{name}: {val} must be {symbol} {bound}"

        self.name = name
        self.val = val
        self.symbol = symbol
        self.bound = bound
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


class SetterErrorMsg(_ErrorMsg):
    pass


class EnumErrorMsg(_ErrorMsg):
    pass


class ValidationError(ValueError):
    """Exception raised when a validation error occurs."""


class SettlementError(ValidationError):
    """Raised when tolerable settlement is greater than the maximum
    allowable settlement.
    """
