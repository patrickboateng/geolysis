from typing import Unpack, TypedDict, NotRequired, Any, Optional


class _ErrorParams(TypedDict):
    param_name: NotRequired[str]
    param_value: NotRequired[Any]
    param_type: NotRequired[Any]


class ErrorMsg(str):

    @staticmethod
    def __new__(cls, msg):
        return super().__new__(cls, msg)


class EnumErrorMsg(ErrorMsg):

    @staticmethod
    def __new__(cls, *args, msg: Optional[str] = None,
                **kwargs: Unpack[_ErrorParams]):
        err_msg = msg if msg else (
            f"Invalid value for {kwargs['param_name']}: {kwargs['param_value']}, "
            f"Supported types are: {list(kwargs['param_type'])}")

        return super().__new__(cls, err_msg)


class ValidationError(ValueError):
    """Exception raised when a validation error occurs."""


class SettlementError(ValueError):
    """Raised when tolerable settlement is greater than the maximum
    allowable settlement.
    """
