class _InstanceOfValidator:
    def __init__(self, type) -> None:
        self.type = type

    def __call__(self, val):
        if not isinstance(val, self.type):
            raise TypeError(
                f"Must be {self.type!s}, got {val!s} that is {type(val)!s}"
            )


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
