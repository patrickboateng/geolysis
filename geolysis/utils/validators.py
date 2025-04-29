"""validators"""
import operator
from typing import Callable, TypeAlias, Any, Iterable
from functools import wraps

from .exceptions import ValidationError, SetterErrorMsg

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
            msg = SetterErrorMsg(msg=self.err_msg,
                                 name=fname,
                                 val=v,
                                 symbol=self.symbol,
                                 bound=self.bound)
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
    def __call__(self, fn):
        @wraps(fn)
        def wrapper(obj, val):
            _len = len(val)
            if not self.func(_len, self.bound):
                msg = SetterErrorMsg(msg=self.err_msg,
                                     name=fn.__name__,
                                     val=val,
                                     symbol=self.symbol,
                                     bound=self.bound)
                msg = f"Length of {msg}"
                raise self.exc_type(msg)
            fn(obj, val)

        return wrapper


class _InValidator(_Validator):
    def __call__(self, fn):
        @wraps(fn)
        def wrapper(obj, val):
            if not self.func(self.bound, val):
                msg = SetterErrorMsg(msg=self.err_msg,
                                     name=fn.__name__,
                                     val=val,
                                     symbol=self.symbol,
                                     bound=self.bound)
                raise self.exc_type(msg)
            fn(obj, val)

        return wrapper


def contains(val: Iterable[Any], /, *, exc_type=ValidationError,
             err_msg: str = None):
    return _InValidator(val, symbol="in", func=operator.contains,
                        exc_type=exc_type, err_msg=err_msg)


def min_len(val: int, /, *, exc_type=ValidationError, err_msg: str = None):
    return _LenValidator(val, symbol=">=", func=operator.ge,
                         exc_type=exc_type, err_msg=err_msg)


def lt(val: Number, /, *, exc_type=ValidationError, err_msg: str = None):
    return _NumValidator(val, symbol="<", func=operator.lt,
                         exc_type=exc_type, err_msg=err_msg)


def le(val: Number, /, *, exc_type=ValidationError, err_msg: str = None):
    return _NumValidator(val, symbol="<=", func=operator.le,
                         exc_type=exc_type, err_msg=err_msg)


def eq(val: Number, /, *, exc_type=ValidationError, err_msg: str = None):
    return _NumValidator(val, symbol="==", func=operator.eq,
                         exc_type=exc_type, err_msg=err_msg)


def ne(val: Number, /, *, exc_type=ValidationError, err_msg: str = None):
    return _NumValidator(val, symbol="!=", func=operator.ne,
                         exc_type=exc_type, err_msg=err_msg)


def ge(val: Number, /, *, exc_type=ValidationError, err_msg: str = None):
    return _NumValidator(val, symbol=">=", func=operator.ge,
                         exc_type=exc_type, err_msg=err_msg)


def gt(val: Number, /, *, exc_type=ValidationError, err_msg: str = None):
    return _NumValidator(val, symbol=">", func=operator.gt,
                         exc_type=exc_type, err_msg=err_msg)
