class PSDValueError(ValueError):
    """Fines, Sand, and Gravels should approximately sum up to 100%

    `fines + sand + gravels = 100%`
    """


class PIValueError(ValueError):
    """`Liquid Limit - Plastic Limit = Plasticity Index`"""
