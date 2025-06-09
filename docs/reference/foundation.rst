*******************
geolysis.foundation
*******************

.. py:currentmodule:: geolysis.foundation

.. autoenum:: Shape

-------------

.. autoenum:: FoundationType

-------------

.. autoclass:: StripFooting
    :members: length, width, shape
    :no-undoc-members:

    .. rubric:: Attributes

    .. autosummary::

        ~StripFooting.length
        ~StripFooting.width
        ~StripFooting.shape


-------------

.. autoclass:: CircularFooting
    :members: diameter, length, width, shape
    :no-undoc-members:

    .. rubric:: Attributes

    .. autosummary::

        ~CircularFooting.diameter
        ~CircularFooting.length
        ~CircularFooting.width
        ~CircularFooting.shape

-------------

.. autoclass:: SquareFooting
    :members: length, width, shape
    :no-undoc-members:

    .. rubric:: Attributes

    .. autosummary::

        ~SquareFooting.length
        ~SquareFooting.width
        ~SquareFooting.shape

-------------

.. autoclass:: RectangularFooting
    :members: length, width, shape
    :no-undoc-members:

    .. rubric:: Attributes

    .. autosummary::

        ~RectangularFooting.length
        ~RectangularFooting.width
        ~RectangularFooting.shape

-------------

.. autoclass:: Foundation
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

        ~Foundation.footing_params

    .. rubric:: Attributes

    .. autosummary::

        ~Foundation.depth
        ~Foundation.eccentricity
        ~Foundation.effective_width
        ~Foundation.footing_shape
        ~Foundation.foundation_type
        ~Foundation.ground_water_level
        ~Foundation.length
        ~Foundation.width

-------------

.. autofunction:: create_foundation
