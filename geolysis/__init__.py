__version__ = "0.4.2"


def error_msg_tmpl(obj, objtype) -> str:
    """Error message template for common errors."""
    msg = "{0} is not supported, Supported types are: {1}"
    objtypes = list(objtype)
    return msg.format(obj, objtypes)


from . import foundation, soil_classifier, spt, utils
