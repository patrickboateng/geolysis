*********************
How to classify soils
*********************

Importing objects
=================

.. code:: python

  >>> from geolysis.soil_classifier import AASHTO, USCS

AASHTO Soil Classification
==============================

The AASHTO classification system is useful for classifying soils for highways.
It categorizes soils for highways based on particle size analysis and
plasticity characteristics. It classifies both coarse-grained and fine-grained
soils into eight main groups (A1-A7) with subgroups, along with a separate
category (A8) for organic soils.

- ``A1 ~ A3`` (Granular Materials) :math:`\le` 35% pass No. 200 sieve
- ``A4 ~ A7`` (Silt-clay Materials) :math:`\ge` 36% pass No. 200 sieve

The Group Index ``(GI)`` is used to further evaluate soils within a group.
When calculating ``GI`` from the equation below, if any term in the parenthesis
becomes negative, it is drop and not given a negative value. The maximum values
of :math:`(F_{200} - 35)` and :math:`(F_{200} - 15)` are taken as 40 and
:math:`(LL - 40)` and :math:`(PI - 10)` as 20.

If the computed value for ``GI`` is negative, it is reported as zero.

In general, the rating for the pavement subgrade is inversely proportional to
the ``GI`` (lower the ``GI``, better the material). For e.g., a ``GI`` of zero
indicates a good subgrade, whereas a group index of 20 or greater shows a very
poor subgrade.

.. note::

    The ``GI`` must be mentioned even when it is zero, to indicate that the soil
    has been classified as per AASHTO system.

``AASHTO`` soil classification with Group Index (GI): ::

  >>> aashto_cls = AASHTO(liquid_limit=30.2, plasticity_index=6.3, fines=11.18)
  >>> # aashto_cls.soil_class -> Returns the AASHTO classification of the soil eg A-7-5(12)
  >>> # aashto_cls.soil_desc -> Returns the AASHTO description of the soil eg Clayey soils
  >>> aashto_cls.soil_class
  'A-2-4(0)'
  >>> aashto_cls.soil_desc
  'Silty or clayey gravel and sand'
  >>> print(f"{aashto_cls.soil_class} - {aashto_cls.soil_desc}")
  A-2-4(0) - Silty or clayey gravel and sand

``AASHTO`` soil classification without Group Index (GI): ::

  >>> aashto_cls = AASHTO(liquid_limit=45, plasticity_index=29, 
  ...                     fines=60, add_group_idx=False)
  >>> aashto_cls.soil_class
  'A-7-6'
  >>> aashto_cls.soil_desc
  'Clayey soils'
  >>> # You can still obtain the group index via the "group_index" method
  >>> aashto_cls.group_index()
  13
  >>> print(f"{aashto_cls.soil_class} - {aashto_cls.soil_desc}")
  A-7-6 - Clayey soils

USCS Soil Classification
============================

The Unified Soil Classification System, initially developed by Casagrande in
1948 and later modified in 1952, is widely utilized in engineering projects
involving soils. It is the most popular system for soil classification and is
similar to Casagrande's Classification System. The system relies on particle
size analysis and atterberg limits for classification.

In this system, soils are first classified into two categories:

- Coarse grained soils: If more than 50% of the soils is retained on No. 200
  (0.075 mm) sieve, it is designated as coarse-grained soil.

- Fine grained soils: If more than 50% of the soil passes through No. 200 sieve,
  it is designated as fine grained soil.

Highly Organic soils are identified by visual inspection. These soils are termed
as Peat. (:math:`P_t`)

.. list-table::
    :header-rows: 1

    * - Soil Symbols
      - Liquid Limit Symbols
      - Gradation Symbols

    * - G: Gravel
      - H: High Plasticity :math: `(LL > 50)`
      - W: Well-graded

    * - S: Sand
      - L: Low Plasticity :math:`(LL < 50)`
      - P: Poorly-graded

    * - M: Silt
      -
      -

    * - C: Clay
      -
      -

    * - O: Organic Clay
      -
      -

    * - Pt: Peat
      -
      -

``USCS`` soil classification with soil grading: ::

  >>> uscs_cls = USCS(liquid_limit=30.8, plastic_limit=20.7, fines=10.29,
  ...                 sand=81.89, gravel=7.83, d_10=0.07, d_30=0.3, d_60=0.8)
  >>> # uscs_cls.soil_class -> Returns the USCS classification of the soil eg SC
  >>> # uscs_cls.soil_desc -> Returns the USCS description of the soil eg Clayey sand
  >>> uscs_cls.soil_class 
  'SW-SC'
  >>> uscs_cls.soil_desc
  'Well graded sand with clay'
  >>> print(f"{uscs_cls.soil_class} - {uscs_cls.soil_desc}")
  SW-SC - Well graded sand with clay

``USCS`` soil classification without soil grading:

  >>> uscs_cls = USCS(liquid_limit=34.1, plastic_limit=21.1, fines=47.88,
  ...                 sand=37.84, gravel=14.8)
  >>> uscs_cls.soil_class
  'SC'
  >>> uscs_cls.soil_desc
  'Clayey sands'
  >>> print(f"{uscs_cls.soil_class} - {uscs_cls.soil_desc}")
  SC - Clayey sands
