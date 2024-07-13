from collections import UserDict
from dataclasses import dataclass
from numbers import Number
from typing import Any, Callable, NamedTuple

__all__ = ["UNIT"]


class RegisteredOption(NamedTuple):
    key: str
    defval: Any
    doc: str
    validator: Callable | None


class _InstanceOfValidator:
    def __init__(self, type) -> None:
        self.type = type

    def __call__(self, val):
        if not isinstance(val, self.type):
            err_msg = (
                f"Must be {self.type!r}, got {val!r} that is {type(val)!r}"
            )
            raise TypeError(err_msg)


class validators:
    @staticmethod
    def instance_of(type):
        """A validator that raises a `TypeError` if the initializer
        is called with a wrong type for this particular option.

        Parameters
        ----------
        type : Any | tuple[Any]
            The type to check for.

        Raises
        ------
        TypeError
        """
        return _InstanceOfValidator(type)


class Config:
    _global_config = {}
    _registered_options: dict[str, RegisteredOption] = {}
    _reserved_keys: list[str] = []

    @classmethod
    def _get_registered_option(cls, opt: str) -> Any:
        return cls._registered_options.get(opt)

    @classmethod
    def get_option(cls, opt: str) -> Any:
        return cls._global_config[opt]

    @classmethod
    def set_option(cls, opt: str, val: Any) -> None:
        _opt = cls._get_registered_option(opt)

        if _opt and _opt.validator:
            _opt.validator(val)

        cls._global_config[opt] = val

    @classmethod
    def reset_option(cls, opt: str):
        val = cls._registered_options[opt].defval
        cls.set_option(opt, val)

    @classmethod
    def register_option(cls, opt: str, defval: Any, doc="", validator=None):
        import keyword

        opt = opt.casefold()

        if opt in cls._registered_options:
            raise Exception

        if opt in cls._reserved_keys:
            raise Exception

        if keyword.iskeyword(opt):
            raise ValueError

        if validator:
            validator(defval)

        cls._global_config[opt] = defval

        cls._registered_options[opt] = RegisteredOption(
            key=opt,
            defval=defval,
            doc=doc,
            validator=validator,
        )


Config.register_option("dp", 4, validator=validators.instance_of(int))
# Config.register_option(
#     "error_tol", 0.01, validator=validators.instance_of(Number)
# )


# The number of decimal places to round mathematical
# values returned from functions (or methods) to.
# DECIMAL_PLACES: int = 4

# Allowable error tolerance for mathematical values
# returned from functions (or methods).
# ERROR_TOL: float = 0.01


class SoilData(UserDict):
    def __getattr__(self, attr) -> Number:
        return self.data[attr]


@dataclass(init=False)
class UNIT:
    """Physical units manager for values returned by various functions
    (or methods) that returns a float.

    Notes
    -----
    These units are compatible with the `pint <https://pint.readthedocs.io/en/stable/index.html>`_
    library unit system.
    """

    #: meter
    m = "meter"

    #: millimeter
    mm = "millimeter"

    #: kilogram
    kg = "kilogram"

    #: degree
    deg = "degrees"

    #: square meter
    m2 = "m**2"

    #: cubic meter
    m3 = "m**3"

    #: kilo Pascal
    kPa = "kPa"

    #: kilo Newton per cubic meter
    kN_m3 = "kN/m**3"
