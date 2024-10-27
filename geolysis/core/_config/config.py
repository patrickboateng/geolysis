import enum
from typing import Any, Callable, NamedTuple

from pint import UnitRegistry

from geolysis.core._config import validators

UNIT_REGISTRY = UnitRegistry()
Q_ = UNIT_REGISTRY.Quantity


class OPTION(enum.StrEnum):
    DP = enum.auto()
    UNIT_SYSTEM = enum.auto()


class UnitSystem(enum.StrEnum):
    """Physical unit systems."""

    CGS = enum.auto()
    MKS = enum.auto()
    IMPERIAL = enum.auto()
    SI = enum.auto()
    DEFAULT_UNIT = SI

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
            raise Exception(
                "Invalid UnitSystem. Available UnitSystems are CGS,"
                " MKS, IMPERIAL and SI."
            )
        return unit


class RegisteredOption(NamedTuple):
    key: str
    defval: Any
    doc: str
    validator: Callable | None


_global_config = {}
_registered_options: dict[str, RegisteredOption] = {}
_reserved_keys: list[str] = []


def _get_registered_option(opt: OPTION) -> Any:
    return _registered_options.get(opt)


def get_option(opt: OPTION) -> Any:
    return _global_config[opt]


def set_option(opt: OPTION, val: Any) -> None:
    _opt = _get_registered_option(opt)

    if _opt and _opt.validator:
        _opt.validator(val)

    _global_config[opt] = val


def reset_option(opt: OPTION):
    val = _registered_options[opt].defval
    set_option(opt, val)


def register_option(opt: OPTION, defval: Any, doc="", validator=None):
    import keyword

    if validator:
        validator(defval)

    if opt in _registered_options:
        raise Exception

    if opt in _reserved_keys:
        raise Exception

    if keyword.iskeyword(opt):
        raise ValueError

    _global_config[opt] = defval

    _registered_options[opt] = RegisteredOption(
        key=opt,
        defval=defval,
        doc=doc,
        validator=validator,
    )


register_option(OPTION.DP, defval=4, validator=validators.instance_of(int))
register_option(OPTION.UNIT_SYSTEM, defval=UnitSystem.SI)
