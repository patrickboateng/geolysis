.. :html_theme.sidebar_secondary.remove:

.. currentmodule:: geolysis

***************
Getting Started
***************

Installation
============

``geolysis`` supports Python 3.10 - 3.12. We also recommend using a
`virtual environment <https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments>`_
in order to isolate your project dependencies from other projects and
the system.

``geolysis`` can be installed via `pip <https://pypi.org/project/geolysis>`_
as follows for the supported operating systems.

.. code:: shell

    pip install geolysis # "pip3 install geolysis" for unix systems

Version Check
=============

To see whether ``geolysis`` is already installed or to check if an install has 
worked, run the following in a Python shell::

    >>> import geolysis as gl
    >>> print(gl.__version__) # doctest: +SKIP

or from the command line:

.. code:: shell

    python -c "import geolysis; print(geolysis.__version__)"
    # python3 -c "import geolysis; print(geolysis.__version__)" for unix systems

You'll see the version number if ``geolysis`` is installed and an error message 
otherwise.

Quick Start
===========

Prerequisites
-------------

You need to know `Python <https://docs.python.org/3/tutorial/>`_ and
a little bit of soil mechanics in order to understand the following examples. 

Learning Objective
------------------

After reading, you should be able to:

- Perform basic soil analysis such as soil classification, bearing
  capacity analysis, and standard penetration tests analysis.

Soil Classification
-------------------

**AASHTO** classification example with **Group Index (GI)**:

.. code:: python

    >>> from geolysis.soil_classifier import create_soil_classifier

    >>> aashto_clf = create_soil_classifier(liquid_limit=30.2,
    ...                                     plastic_limit=23.9,
    ...                                     fines=11.18, clf_type="AASHTO")
    >>> clf = aashto_clf.classify()
    >>> clf.soil_symbol
    'A-2-4(0)'
    >>> clf.soil_description
    'Silty or clayey gravel and sand'

**AASHTO** classification example without **Group Index (GI)**:

.. code:: python

    >>> aashto_clf = create_soil_classifier(liquid_limit=45.0,
    ...                                     plastic_limit=16.0,
    ...                                     fines=60.0, 
    ...                                     add_group_idx=False,
    ...                                     clf_type="AASHTO")
    >>> clf = aashto_clf.classify()
    >>> clf.soil_symbol
    'A-7-6'
    >>> clf.soil_description
    'Clayey soils'

**USCS** classification example with soil grading:

.. code:: python

    >>> from geolysis.soil_classifier import create_soil_classifier
    >>> uscs_clf = create_soil_classifier(liquid_limit=30.8, 
    ...                                   plastic_limit=20.7, 
    ...                                   fines=10.29, sand=81.89, 
    ...                                   d_10=0.07, d_30=0.3, d_60=0.8,
    ...                                   clf_type="USCS")
    >>> clf = uscs_clf.classify()
    >>> clf.soil_symbol
    'SW-SC'
    >>> clf.soil_description
    'Well graded sand with clay'

**USCS** classification example without soil grading:

.. code:: python

    >>> uscs_clf = create_soil_classifier(liquid_limit=34.1, 
    ...                                   plastic_limit=21.1,
    ...                                   fines=47.88, sand=37.84, 
    ...                                   clf_type="USCS")
    >>> clf = uscs_clf.classify()
    >>> clf.soil_symbol
    'SC'
    >>> clf.soil_description
    'Clayey sands'

Ultimate Bearing Capacity Estimation
------------------------------------

Calculating the ultimate bearing capacity of soil using ``Hansen's``
correlation:

.. code:: python

    >>> from geolysis.bearing_capacity.ubc import ( 
    ...                    create_ultimate_bearing_capacity)
    >>> hansen_ubc = create_ultimate_bearing_capacity(
    ...                friction_angle=20.0,
    ...                cohesion=20.0,
    ...                moist_unit_wgt=18.0,
    ...                depth=1.5, width=2.0, shape="square", 
    ...                ubc_type="HANSEN",
    ...            )
    >>> hansen_ubc.bearing_capacity()
    798.41

Other available ultimate bearing capacity types are ``TERZAGHI`` and ``VESIC``

Allowable Bearing Capacity Estimation
-------------------------------------

Calculating the allowable bearing capacity of soil for pad foundations using 
``Bowles`` correlations:

.. code:: python

    >>> from geolysis.bearing_capacity.abc.cohl import \
    ...                       create_allowable_bearing_capacity
    >>> bowles_abc = create_allowable_bearing_capacity(
    ...                  corrected_spt_n_value=17.0,
    ...                  tol_settlement=20.0,
    ...                  depth=1.5, width=1.2, shape="SQUARE",
    ...                  foundation_type="pad",
    ...                  abc_type="BOWLES"
    ...                  )
    >>> bowles_abc.bearing_capacity()
    341.11

Other available allowable bearing capacity types are ``MEYERHOF`` and
``TERZAGHI``.

Standard Penetration Tests Analysis
-----------------------------------

Calculating SPT :math:`N_{design}` from a list of SPT N-values:

.. code:: python

    >>> from geolysis.spt import SPTDesign
    >>> spt_design = SPTDesign(spt_n_values=[7.0, 15.0, 18.0])
    >>> spt_design.average_spt_n_design()
    13.3
    >>> spt_design.minimum_spt_n_design()
    7.0
    >>> spt_design.weighted_spt_n_design()
    9.4

Standardizing SPT N-values depending on the field procedure used:

.. code:: python

    >>> from geolysis.spt import EnergyCorrection
    >>> energy_corr = EnergyCorrection(recorded_spt_n_value=30,
    ...                                energy_percentage=0.6,
    ...                                borehole_diameter=65.0,
    ...                                rod_length=3.0)
    >>> energy_corr.corrected_spt_n_value()
    22.5

Correcting SPT N-values for overburden pressure influence using 
``Gibbs & Holtz (1957)`` correlation:

.. code:: python

    >>> from geolysis.spt import GibbsHoltzOPC
    >>> opc_corr = GibbsHoltzOPC(std_spt_n_value=22.5, eop=100.0)
    >>> opc_corr.corrected_spt_n_value()
    23.2

Other correlations for calculating Overburden Pressure Corrections are:

- :class:`~geolysis.spt.BazaraaPeckOPC`
- :class:`~geolysis.spt.PeckOPC`
- :class:`~geolysis.spt.LiaoWhitmanOPC`
- :class:`~geolysis.spt.SkemptonOPC`

Correcting SPT N-values for water (dilatancy) influence:

.. code::

    >>> from geolysis.spt import DilatancyCorrection
    >>> dil_corr = DilatancyCorrection(std_spt_n_value=22.5)
    >>> dil_corr.corrected_spt_n_value()
    18.8
