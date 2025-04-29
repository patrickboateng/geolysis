from typing import Optional


class _ErrorMsg(str):

    @staticmethod
    def __new__(cls, msg, *args, **kwargs):
        return super().__new__(cls, msg)


class SetterErrorMsg(_ErrorMsg):

    @staticmethod
    def __new__(cls, *args, name, val, symbol, bound,
                msg: Optional[str] = None, **kwargs):
        if not msg:
            msg = f"{name}: {val} must be {symbol} {bound}"

        return super().__new__(cls, msg)


class EnumErrorMsg(_ErrorMsg):

    @staticmethod
    def __new__(cls, *args, name, val, bound,
                msg: Optional[str] = None, **kwargs):
        if not msg:
            msg = f"Invalid value for {name}: {val}, " \
                  f"Supported types are: {list(bound)}"

        return super().__new__(cls, msg)


class ValidationError(ValueError):
    """Exception raised when a validation error occurs."""


class SettlementError(ValidationError):
    """Raised when tolerable settlement is greater than the maximum
    allowable settlement.
    """
