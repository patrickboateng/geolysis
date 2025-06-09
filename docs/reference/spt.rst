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

.. autoclass:: SPT
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

        ~SPT.n_design

    .. rubric:: Attributes

    .. autosummary::

        ~SPT.corrected_spt_n_values

-------

.. autoclass:: EnergyCorrection
    :members:
    :no-undoc-members:

    .. rubric:: Methods

    .. autosummary::

          ~EnergyCorrection.correction
          ~EnergyCorrection.standardized_spt_n_value

    .. rubric:: Attributes

    .. autosummary::

          ~EnergyCorrection.borehole_diameter
          ~EnergyCorrection.borehole_diameter_correction
          ~EnergyCorrection.energy_percentage
          ~EnergyCorrection.hammer_efficiency
          ~EnergyCorrection.recorded_spt_n_value
          ~EnergyCorrection.rod_length
          ~EnergyCorrection.rod_length_correction
          ~EnergyCorrection.sampler_correction

--------

.. autoclass:: GibbsHoltzOPC
    :members: eop, std_spt_n_value, correction, corrected_spt_n_value

    .. rubric:: Methods

    .. autosummary::

          ~GibbsHoltzOPC.corrected_spt_n_value
          ~GibbsHoltzOPC.correction

    .. rubric:: Attributes

    .. autosummary::

          ~GibbsHoltzOPC.eop
          ~GibbsHoltzOPC.std_spt_n_value

---------

.. autoclass:: BazaraaPeckOPC
    :members: eop, std_spt_n_value, correction, corrected_spt_n_value, STD_PRESSURE

    .. rubric:: Methods

    .. autosummary::

      ~BazaraaPeckOPC.corrected_spt_n_value
      ~BazaraaPeckOPC.correction

    .. rubric:: Attributes

    .. autosummary::

      ~BazaraaPeckOPC.STD_PRESSURE
      ~BazaraaPeckOPC.eop
      ~BazaraaPeckOPC.std_spt_n_value

----------

.. autoclass:: PeckOPC
    :members: eop, std_spt_n_value, correction, corrected_spt_n_value

    .. rubric:: Methods

    .. autosummary::

        ~PeckOPC.corrected_spt_n_value
        ~PeckOPC.correction

    .. rubric:: Attributes

    .. autosummary::

        ~PeckOPC.eop
        ~PeckOPC.std_spt_n_value

----------

.. autoclass:: LiaoWhitmanOPC
    :members: eop, std_spt_n_value, correction, corrected_spt_n_value

    .. rubric:: Methods

    .. autosummary::

        ~LiaoWhitmanOPC.corrected_spt_n_value
        ~LiaoWhitmanOPC.correction

    .. rubric:: Attributes

    .. autosummary::

        ~LiaoWhitmanOPC.eop
        ~LiaoWhitmanOPC.std_spt_n_value

-----------

.. autoclass:: SkemptonOPC
    :members: eop, std_spt_n_value, correction, corrected_spt_n_value

    .. rubric:: Methods

    .. autosummary::

          ~SkemptonOPC.corrected_spt_n_value
          ~SkemptonOPC.correction

    .. rubric:: Attributes

    .. autosummary::

          ~SkemptonOPC.eop
          ~SkemptonOPC.std_spt_n_value

-----------

.. autoclass:: DilatancyCorrection
    :members: corrected_spt_n_value

    .. rubric:: Methods

    .. autosummary::

        ~DilatancyCorrection.corrected_spt_n_value

    .. rubric:: Attributes

    .. autosummary::

        ~DilatancyCorrection.corr_spt_n_value

------------

.. autofunction:: create_overburden_pressure_correction
