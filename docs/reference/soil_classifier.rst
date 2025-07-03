************************
geolysis.soil_classifier
************************

.. py:currentmodule:: geolysis.soil_classifier

.. autoexception:: SizeDistError

------------

.. autoenum:: USCSSymbol

------------

.. autoenum:: AASHTOSymbol

------------

.. autoclass:: AtterbergLimits
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

        ~AtterbergLimits.above_A_LINE
        ~AtterbergLimits.consistency_index
        ~AtterbergLimits.limit_plot_in_hatched_zone
        ~AtterbergLimits.liquidity_index

    .. rubric:: Attributes

    .. autosummary::

        ~AtterbergLimits.A_LINE
        ~AtterbergLimits.fine_material_type
        ~AtterbergLimits.liquid_limit
        ~AtterbergLimits.plastic_limit
        ~AtterbergLimits.plasticity_index

------------

.. autoclass:: PSD
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

        ~PSD.grade
        ~PSD.has_particle_sizes

    .. rubric:: Attributes

    .. autosummary::

        ~PSD.coarse_material_type
        ~PSD.coeff_of_curvature
        ~PSD.coeff_of_uniformity
        ~PSD.gravel

------------

.. autoclass:: AASHTO
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

        ~AASHTO.classify
        ~AASHTO.group_index

    .. rubric:: Attributes

    .. autosummary::

        ~AASHTO.fines

------------

.. autoclass:: USCS
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

        ~USCS.classify

------------

.. autofunction:: create_aashto_classifier
.. autofunction:: create_uscs_classifier
