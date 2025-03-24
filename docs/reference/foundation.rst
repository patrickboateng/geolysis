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

.. autoclass:: FoundationSize
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

        ~FoundationSize.footing_params

    .. rubric:: Attributes

    .. autosummary::

        ~FoundationSize.depth
        ~FoundationSize.eccentricity
        ~FoundationSize.effective_width
        ~FoundationSize.footing_shape
        ~FoundationSize.foundation_type
        ~FoundationSize.ground_water_level
        ~FoundationSize.length
        ~FoundationSize.width

-------------

.. autofunction:: create_foundation
