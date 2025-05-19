"""validators"""
import operator
from functools import wraps
from typing import Any, Callable, Iterable, TypeAlias, List, Tuple, Sequence

from .exceptions import ErrorMsg, ValidationError

Number: TypeAlias = int | float


class _Validator:

    def __init__(self, bound: Any, /, *,
                 symbol: str,
                 check: Callable,
                 exc_type: Callable,
                 err_msg: str):
        self.bound = bound
        self.symbol = symbol
        self.check = check
        self.exc_type = exc_type
        self.err_msg = err_msg

    def check_val(self, val, fname: str):
        raise NotImplementedError

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(obj, val):
            if isinstance(val, List | Tuple):
                for v in val:
                    self.check_val(v, fn.__name__)
            else:
                self.check_val(val, fn.__name__)

            fn(obj, val)

        return wrapper


class _NumValidator(_Validator):

    def check_val(self, v: Number, fname: str):
        if not self.check(v, self.bound):
            msg = ErrorMsg(msg=self.err_msg,
                           param_name=fname,
                           param_value=v,
                           symbol=self.symbol,
                           param_value_bound=self.bound)
            raise self.exc_type(msg)


class _LenValidator(_Validator):

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(obj, val: Sequence):
            if not self.check(len(val), self.bound):
                msg = ErrorMsg(msg=self.err_msg,
                               param_name=fn.__name__,
                               param_value=val,
                               symbol=self.symbol,
                               param_value_bound=self.bound)
                msg = "Length of " + msg
                raise self.exc_type(msg)
            fn(obj, val)

        return wrapper


class _InValidator(_Validator):
    def check_val(self, v, fname):
        if not self.check(self.bound, v):
            msg = ErrorMsg(msg=self.err_msg,
                           param_name=fname,
                           param_value=v,
                           symbol=self.symbol,
                           param_value_bound=self.bound)
            raise self.exc_type(msg)


def in_(bound: Iterable[Any], /, *, exc_type=ValidationError, err_msg=None):
    return _InValidator(bound, symbol="in", check=operator.contains,
                        exc_type=exc_type, err_msg=err_msg)


def min_len(bound: int, /, *, exc_type=ValidationError, err_msg=None):
    return _LenValidator(bound, symbol=">=", check=operator.ge,
                         exc_type=exc_type, err_msg=err_msg)


def lt(bound: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(bound, symbol="<", check=operator.lt,
                         exc_type=exc_type, err_msg=err_msg)


def le(bound: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(bound, symbol="<=", check=operator.le,
                         exc_type=exc_type, err_msg=err_msg)


def eq(bound: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(bound, symbol="==", check=operator.eq,
                         exc_type=exc_type, err_msg=err_msg)


def ne(bound: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(bound, symbol="!=", check=operator.ne,
                         exc_type=exc_type, err_msg=err_msg)


def ge(bound: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(bound, symbol=">=", check=operator.ge,
                         exc_type=exc_type, err_msg=err_msg)


def gt(bound: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(bound, symbol=">", check=operator.gt,
                         exc_type=exc_type, err_msg=err_msg)
