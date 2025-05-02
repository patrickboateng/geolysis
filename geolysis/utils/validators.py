"""validators"""
import operator
from functools import wraps
from typing import Any, Callable, Iterable, TypeAlias

from .exceptions import ErrorMsg, ValidationError

Number: TypeAlias = int | float


class _Validator:

    def __init__(self, bound: Any, /, *,
                 symbol: str,
                 func: Callable,
                 exc_type: Callable,
                 err_msg: str):
        """

        """
        self.bound = bound
        self.symbol = symbol
        self.func = func
        self.exc_type = exc_type
        self.err_msg = err_msg


class _NumValidator(_Validator):

    def _check_val(self, v: Number, fname: str):
        if not self.func(v, self.bound):
            msg = ErrorMsg(msg=self.err_msg,
                           param_name=fname,
                           param_value=v,
                           symbol=self.symbol,
                           param_value_bound=self.bound)
            raise self.exc_type(msg)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(obj, val):
            if isinstance(val, Iterable):
                for v in val:
                    self._check_val(v, fn.__name__)
            else:
                self._check_val(val, fn.__name__)

            fn(obj, val)

        return wrapper


class _LenValidator(_Validator):
    def _check_val(self, v: Iterable[Any], fname: str):
        if not self.func(len(v), self.bound):
            msg = ErrorMsg(msg=self.err_msg,
                           param_name=fname,
                           param_value=v,
                           symbol=self.symbol,
                           param_value_bound=self.bound)
            msg = "Length of " + msg
            raise self.exc_type(msg)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(obj, val: Iterable):
            self._check_val(val, fn.__name__)
            fn(obj, val)

        return wrapper


class _InValidator(_Validator):
    def _check_val(self, v, fname):
        if not self.func(self.bound, v):
            msg = ErrorMsg(msg=self.err_msg,
                           param_name=fname,
                           param_value=v,
                           symbol=self.symbol,
                           param_value_bound=self.bound)
            raise self.exc_type(msg)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(obj, val):
            self._check_val(val, fn.__name__)
            fn(obj, val)

        return wrapper


def in_(val: Iterable[Any], /, *, exc_type=ValidationError, err_msg=None):
    return _InValidator(val, symbol="in", func=operator.contains,
                        exc_type=exc_type, err_msg=err_msg)


def min_len(val: int, /, *, exc_type=ValidationError, err_msg=None):
    return _LenValidator(val, symbol=">=", func=operator.ge,
                         exc_type=exc_type, err_msg=err_msg)


def lt(val: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(val, symbol="<", func=operator.lt,
                         exc_type=exc_type, err_msg=err_msg)


def le(val: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(val, symbol="<=", func=operator.le,
                         exc_type=exc_type, err_msg=err_msg)


def eq(val: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(val, symbol="==", func=operator.eq,
                         exc_type=exc_type, err_msg=err_msg)


def ne(val: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(val, symbol="!=", func=operator.ne,
                         exc_type=exc_type, err_msg=err_msg)


def ge(val: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(val, symbol=">=", func=operator.ge,
                         exc_type=exc_type, err_msg=err_msg)


def gt(val: Number, /, *, exc_type=ValidationError, err_msg=None):
    return _NumValidator(val, symbol=">", func=operator.gt,
                         exc_type=exc_type, err_msg=err_msg)
