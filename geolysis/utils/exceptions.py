from typing import Unpack, TypedDict, NotRequired, Any, Optional


class _ErrorParams(TypedDict):
    param_name: NotRequired[str]
    param_value: NotRequired[Any]
    param_type: NotRequired[Any]


class EnumErrorMsg(str):

    @staticmethod
    def __new__(cls, *args, msg: Optional[str] = None,
                **kw: Unpack[_ErrorParams]):
        if msg:
            return super().__new__(cls, msg)

        # Assume kwargs contains values for param_name, param_value,
        # param_type, if not, KeyError exception is raised

        msg = (f"Invalid value for {kw['param_name']}: {kw['param_value']}, "
               f"Supported types are: {list(kw['param_type'])}")

        return super().__new__(cls, msg)


class ValidationError(ValueError):
    """Exception raised when a validation error occurs."""


class SettlementError(ValueError):
    """Raised when tolerable settlement is greater than the maximum
    allowable settlement.
    """
