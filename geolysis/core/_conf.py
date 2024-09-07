import enum
from typing import Any, Callable, NamedTuple

from pint import UnitRegistry

UNIT_REGISTRY = UnitRegistry()
Q_ = UNIT_REGISTRY.Quantity


class UnitSystem(enum.StrEnum):
    """Physical unit systems."""

    CGS = enum.auto()
    MKS = enum.auto()
    IMPERIAL = enum.auto()
    SI = "SI"

    @property
    def Pressure(self):
        if self is self.CGS:
            unit = UNIT_REGISTRY.barye
        elif self is self.MKS or self is self.SI:
            unit = UNIT_REGISTRY.kPa
        elif self is self.IMPERIAL:
            unit = UNIT_REGISTRY.psi
        else:
            # TODO: Add error msg
            raise Exception
        return unit


class RegisteredOption(NamedTuple):
    key: str
    defval: Any
    doc: str
    validator: Callable | None


_global_config = {}
_registered_options: dict[str, RegisteredOption] = {}
_reserved_keys: list[str] = []


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


def _get_registered_option(opt: str) -> Any:
    return _registered_options.get(opt)


def get_option(opt: str) -> Any:
    return _global_config[opt]


def set_option(opt: str, val: Any) -> None:
    _opt = _get_registered_option(opt)

    if _opt and _opt.validator:
        _opt.validator(val)

    _global_config[opt] = val


def reset_option(opt: str):
    val = _registered_options[opt].defval
    set_option(opt, val)


def register_option(opt: str, defval: Any, doc="", validator=None):
    import keyword

    opt = opt.casefold()

    if opt in _registered_options:
        raise Exception

    if opt in _reserved_keys:
        raise Exception

    if keyword.iskeyword(opt):
        raise ValueError

    if validator:
        validator(defval)

    _global_config[opt] = defval

    _registered_options[opt] = RegisteredOption(
        key=opt,
        defval=defval,
        doc=doc,
        validator=validator,
    )


register_option("dp", 4, validator=validators.instance_of(int))
register_option("unit_system", UnitSystem.SI)
