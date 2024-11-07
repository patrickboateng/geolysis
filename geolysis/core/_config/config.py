import enum
from typing import Any, Callable, NamedTuple

import pint

from geolysis.core._config import validators


class CustomQuantity(pint.UnitRegistry.Quantity):
    pass


class CustomUnit(pint.UnitRegistry.Unit):
    pass


class UnitRegistry(
    pint.registry.GenericUnitRegistry[CustomQuantity, CustomUnit]
):
    Quantity = CustomQuantity
    Unit = CustomUnit


class UnitSystem(enum.StrEnum):
    CGS = "cgs"
    MKS = "mks"
    BRITISH_IMPERIAL = "imperial"
    US_IMPERIAL = "US"
    SI = "SI"


UnitReg = UnitRegistry(system=UnitSystem.SI, cache_folder=":auto:")
Quantity = UnitReg.Quantity


########################################################


class Option(enum.StrEnum):
    DP = enum.auto()
    UNIT_SYSTEM = enum.auto()


class RegisteredOption(NamedTuple):
    key: str
    defval: Any
    doc: str
    validator: Callable | None


_global_config = {}
_registered_options: dict[str, RegisteredOption] = {}
_reserved_keys: list[str] = []


def _get_registered_option(opt: Option) -> Any:
    return _registered_options.get(opt)


def get_option(opt: Option) -> Any:
    return _global_config[opt]


def set_option(opt: Option, val: Any) -> None:
    _opt = _get_registered_option(opt)

    if _opt and _opt.validator:
        _opt.validator(val)

    _global_config[opt] = val


def reset_option(opt: Option):
    val = _registered_options[opt].defval
    set_option(opt, val)


def register_option(opt: Option, defval: Any, doc="", validator=None):
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


register_option(Option.DP, defval=4, validator=validators.instance_of(int))
register_option(Option.UNIT_SYSTEM, defval=UnitSystem.SI)
