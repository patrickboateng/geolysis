from enum import Enum
from functools import wraps
from typing import Any, Callable, NamedTuple

from pint import UnitRegistry

__all__ = ["ERROR_TOL"]

#: Allowable error tolerance for mathematical values
#: returned from functions (or methods).
ERROR_TOL: float = 0.01

ureg = UnitRegistry()
Q_ = ureg.Quantity

print(dir(ureg.sys.imperial))


class UnitSystem(Enum):
    """Physical unit systems."""

    CGS = "cgs"
    MKS = "mks"
    IMPERIAL = "imperial"
    SI = "SI"

    @property
    def Pressure(self):
        if self is self.CGS:
            return "barye"

        if self is self.MKS or self is self.SI:
            return "kN/m**2"

        if self is self.IMPERIAL:
            return "psi"


class assign_unit:
    def __init__(
        self,
        default_unit: Q_ | str,
        *,
        cgs_unit: Q_ | str | None = None,
        mks_unit: Q_ | str | None = None,
        imperial_unit: Q_ | str | None = None,
        si_unit: Q_ | str | None = None,
    ):
        self.default_unit = default_unit
        self.cgs_unit = cgs_unit
        self.mks_unit = mks_unit
        self.imperial_unit = imperial_unit
        self.si_unit = si_unit

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            ret = fn(*args, **kwargs)
            to = None
            ureg.default_system = Config.get_option("unit_system").value
            match ureg.default_system:
                case UnitSystem.CGS.value:
                    to = self.cgs_unit
                case UnitSystem.MKS.value:
                    to = self.mks_unit
                case UnitSystem.IMPERIAL.value:
                    to = self.imperial_unit
                case UnitSystem.SI.value:
                    to = self.si_unit
                case _:
                    raise ValueError
            return Q_(ret, self.default_unit).to_base_units().to_compact(to)  # type: ignore

        return wrapper


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
Config.register_option("unit_system", UnitSystem.CGS)
