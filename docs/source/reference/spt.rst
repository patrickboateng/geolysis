************
geolysis.spt
************

.. py:currentmodule:: geolysis.spt

.. autoenum:: HammerType

-------

.. autoenum:: SamplerType

-------

.. autoenum:: OPCType

-------

.. autoclass:: SPTNDesign

-------

.. autoclass:: EnergyCorrection
    :members: correction, corrected_spt_n_value, standardized_spt_n_value

--------

.. autoclass:: GibbsHoltzOPC
    :members: correction, corrected_spt_n_value

---------

.. autoclass:: BazaraaPeckOPC
    :members: correction, corrected_spt_n_value

----------

.. autoclass:: PeckOPC
    :members: correction, corrected_spt_n_value

----------

.. autoclass:: LiaoWhitmanOPC
    :members: correction, corrected_spt_n_value

-----------

.. autoclass:: SkemptonOPC
    :members: correction, corrected_spt_n_value

-----------

.. autoclass:: DilatancyCorrection
    :members: corrected_spt_n_value

------------

.. autofunction:: create_spt_correction
