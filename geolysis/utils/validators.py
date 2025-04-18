"""validators"""
import operator
from typing import Callable, TypeAlias, Optional

from .exceptions import ValidationError

Number: TypeAlias = int | float


def _num_validator(bound: float, /, *,
                   compare_symbol: str,
                   compare_fn: Callable,
                   exc_type: Callable,
                   err_msg: str):
    def dec(fn):
        def wrapper(obj, val):
            if not compare_fn(val, bound):
                msg = f"{fn.__name__} must be {compare_symbol} {bound}"
                raise exc_type(err_msg if err_msg else msg)
            fn(obj, val)

        return wrapper

    return dec


def _len_validator(bound: float, /, *,
                   compare_symbol: str,
                   compare_fn: Callable,
                   exc_type: Callable,
                   err_msg: str):
    def dec(fn):
        def wrapper(obj, val):
            _len = len(val)
            if not compare_fn(_len, bound):
                msg = f"Length of '{fn.__name__}' must be {compare_symbol} {bound}"
                raise exc_type(err_msg if err_msg else msg)
            fn(obj, val)

        return wrapper

    return dec


def min_len(m_len: int, /, *,
            exc_type=ValidationError,
            err_msg: Optional[str] = None):
    return _len_validator(m_len, compare_symbol=">=",
                          compare_fn=operator.ge,
                          exc_type=exc_type, err_msg=err_msg)


def lt(val: Number, /, *, exc_type=ValidationError,
       err_msg: Optional[str] = None):
    return _num_validator(val, compare_symbol="<",
                          compare_fn=operator.lt,
                          exc_type=exc_type,
                          err_msg=err_msg)


def le(val: Number, /, *, exc_type=ValidationError,
       err_msg: Optional[str] = None):
    return _num_validator(val, compare_symbol="<=",
                          compare_fn=operator.le,
                          exc_type=exc_type,
                          err_msg=err_msg)


def eq(val: Number, /, *, exc_type=ValidationError,
       err_msg: Optional[str] = None):
    return _num_validator(val, compare_symbol="==",
                          compare_fn=operator.eq,
                          exc_type=exc_type,
                          err_msg=err_msg)


def ne(val: Number, /, *, exc_type=ValidationError,
       err_msg: Optional[str] = None):
    return _num_validator(val, compare_symbol="!=",
                          compare_fn=operator.ne,
                          exc_type=exc_type,
                          err_msg=err_msg)


def ge(val: Number, /, *, exc_type=ValidationError,
       err_msg: Optional[str] = None):
    return _num_validator(val, compare_symbol=">=",
                          compare_fn=operator.ge,
                          exc_type=exc_type,
                          err_msg=err_msg)


def gt(val: Number, /, *, exc_type=ValidationError,
       err_msg: Optional[str] = None):
    return _num_validator(val, compare_symbol=">",
                          compare_fn=operator.gt,
                          exc_type=exc_type,
                          err_msg=err_msg)
