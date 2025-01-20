import operator
from typing import Callable, TypeAlias


class _NumberValidator:
    def __init__(self, bound: float,
                 compare_op: str,
                 compare_fn: Callable,
                 exc_type=ValueError,
                 err_msg=None) -> None:
        self.bound = bound
        self.compare_op = compare_op
        self.compare_fn = compare_fn
        self.exc_type = exc_type
        self.err_msg = err_msg

    def __call__(self, fn):
        def wrapper(obj, val):
            if not self.compare_fn(val, self.bound):
                if not self.err_msg:
                    msg = self.err_msg
                else:
                    msg = f"{fn.__name__} must be {self.compare_op} {self.bound}"
                raise self.exc_type(msg)
            return fn(obj, val)

        return wrapper


Number: TypeAlias = int | float


def lt(val: Number, /, *, exc_type=ValueError, err_msg=None):
    return _NumberValidator(val, "<", operator.lt, exc_type, err_msg)


def le(val: Number, /, *, exc_type=ValueError, err_msg=None):
    return _NumberValidator(val, "<=", operator.le, exc_type, err_msg)


def eq(val: Number, /, *, exc_type=ValueError, err_msg=None):
    return _NumberValidator(val, "==", operator.eq, exc_type, err_msg)


def ne(val: Number, /, *, exc_type=ValueError, err_msg=None):
    return _NumberValidator(val, "!=", operator.ne, exc_type, err_msg)


def ge(val: Number, /, *, exc_type=ValueError, err_msg=None):
    return _NumberValidator(val, ">=", operator.ge, exc_type, err_msg)


def gt(val: Number, /, *, exc_type=ValueError, err_msg=None):
    return _NumberValidator(val, ">", operator.gt, exc_type, err_msg)
