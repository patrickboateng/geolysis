from collections import UserString
from typing import Any


class _ErrorMsg(UserString):
    def __init__(self, *, param_name: str = None,
                 param_value: Any = None,
                 symbol: str = None,
                 param_value_bound: Any = None,
                 msg: str = None):
        if not msg:
            msg = f"{param_name}: {param_value!r} must be {symbol} {param_value_bound}"

        super().__init__(msg)

        self.param_name = param_name
        self.param_value = param_value
        self.symbol = symbol
        self.param_value_bound = param_value_bound

    @property
    def msg(self):
        return self.data

    def __add__(self, other):
        other = str(other)
        msg = self.msg + other
        return self.__class__(param_name=self.param_name,
                              param_value=self.param_value,
                              symbol=self.symbol,
                              param_value_bound=self.param_value_bound,
                              msg=msg)

    def __radd__(self, other):
        other = str(other)
        msg = other + self.msg
        return self.__class__(param_name=self.param_name,
                              param_value=self.param_value,
                              symbol=self.symbol,
                              param_value_bound=self.param_value_bound,
                              msg=msg)

    def __repr__(self) -> str:
        return f"ErrorMsg(param_name={self.param_name}, " \
               f"param_value={self.param_value}, " \
               f"symbol={self.symbol}, " \
               f"param_value_bound={self.param_value_bound}, msg={self.msg!r})"

    def to_dict(self) -> dict:
        return {
            "param_name": self.param_name,
            "param_value": self.param_value,
            "symbol": self.symbol,
            "param_value_bound": self.param_value_bound,
            "message": self.msg
        }


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
