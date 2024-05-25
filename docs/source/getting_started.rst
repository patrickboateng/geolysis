:html_theme.sidebar_secondary.remove:

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

.. tab-set::

    .. tab-item:: Windows
        :sync: win

        .. code::

            C:\> pip install geolysis

    .. tab-item:: Unix
        :sync: unix

        .. code::

            $ pip3 install geolysis

Version Check
=============

To see whether ``geolysis`` is already installed or to check if an
install has worked, run the following in a Python shell::

    >>> import geolysis as gl
    >>> print(gl.__version__) # doctest: +SKIP

or from the command line:

.. tab-set::

    .. tab-item:: Windows
        :sync: win

        .. code:: shell

            C:\> py -c "import geolysis; print(geolysis.__version__)"

    .. tab-item:: Unix
        :sync: unix

        .. code:: shell

            $ python3 -c "import geolysis; print(geolysis.__version__)"

You'll see the version number if ``geolysis`` is installed and an
error message otherwise.

Quick Start
===========

Prerequisites
-------------

You need to know `Python <https://docs.python.org/3/tutorial/>`_ and
a little bit of soil mechanics in order to work through the examples.

Learning Objective
------------------

After reading, you should be able to:

- Perform basic soil analysis such as soil classification, bearing
  capacity analysis, and standard penetration tests analysis.

Soil Classification
-------------------

**AASHTO** classification example with **Group Index (GI)**:

>>> from geolysis.core.soil_classifier import AASHTO

>>> aashto_clf = AASHTO(liquid_limit=30.2, plasticity_index=6.3,
...                     fines=11.18)
>>> aashto_clf.group_index()
0.0
>>> aashto_clf.soil_class
'A-2-4(0)'
>>> aashto_clf.soil_desc
'Silty or clayey gravel and sand'

**AASHTO** classification example without **Group Index (GI)**:

>>> aashto_cls = AASHTO(liquid_limit=45, plasticity_index=29,
...                     fines=60, add_group_idx=False)
>>> aashto_cls.group_index()
13.0
>>> aashto_cls.soil_class
'A-7-6'
>>> aashto_cls.soil_desc
'Clayey soils'

**USCS** classification example with soil grading:

>>> from geolysis.core.soil_classifier import USCS
>>> uscs_cls = USCS(liquid_limit=30.8, plastic_limit=20.7, fines=10.29,
...                 sand=81.89, gravel=7.83, d_10=0.07, d_30=0.3, d_60=0.8)
>>> uscs_cls.soil_class
'SW-SC'
>>> uscs_cls.soil_desc
'Well graded sand with clay'

**USCS** classification example without soil grading:

>>> uscs_cls = USCS(liquid_limit=34.1, plastic_limit=21.1,
...                 fines=47.88, sand=37.84, gravel=14.8)
>>> uscs_cls.soil_class
'SC'
>>> uscs_cls.soil_desc
'Clayey sands'

Allowable Bearing Capacity Analysis
-----------------------------------

.. currentmodule:: geolysis

Calculating the allowable bearing capacity of soil for pad
foundations using ``Bowles`` correlations:

>>> from geolysis.core.abc_4_cohl_soils import BowlesABC4PadFoundation
>>> from geolysis.core.foundation import create_foundation, Shape

>>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
...                                     width=1.2, footing_shape=Shape.SQUARE)
>>> bowles_abc = BowlesABC4PadFoundation(corrected_spt_number=17.0,
...                                      tol_settlement=20.0,
...                                      foundation_size=foundation_size)
>>> bowles_abc.bearing_capacity()
341.1083

Other correlations for calculating bearing capacities are:

- :class:`~geolysis.core.abc_4_cohl_soils.BowlesABC4MatFoundation`
- :class:`~geolysis.core.abc_4_cohl_soils.MeyerhofABC4PadFoundation`
- :class:`~geolysis.core.abc_4_cohl_soils.MeyerhofABC4MatFoundation`
- :class:`~geolysis.core.abc_4_cohl_soils.TerzaghiABC4PadFoundation`
- :class:`~geolysis.core.abc_4_cohl_soils.TerzaghiABC4MatFoundation`

Standard Penetration Tests Analysis
-----------------------------------

Calculating SPT :math:`N_{design}` from a list of SPT N-values:

>>> from geolysis.core.spt import WeightedSPT
>>> spt_numbers = [7.0, 15.0, 18.0]
>>> spt_avg = WeightedSPT(spt_numbers=spt_numbers)
>>> spt_avg.spt_n_design()
9.3673

Other correlations for calculating SPT :math:`N_{design}` are:

- :class:`~geolysis.core.spt.AverageSPT`
- :class:`~geolysis.core.spt.MinSPT`

Standardizing SPT N-values depending on the field procedure used:

>>> from geolysis.core.spt import EnergyCorrection
>>> energy_cor = EnergyCorrection(recorded_spt_number=30, energy_percentage=0.6,
...                               hammer_efficiency=0.6, borehole_diameter_correction=1.0,
...                               sampler_correction=1.0, rod_length_correction=0.75)
>>> energy_cor.correction
0.75
>>> energy_cor.corrected_spt_number
22.5

Correcting SPT N-values for overburden pressure influence:

>>> from geolysis.core.spt import GibbsHoltzOPC
>>> opc_cor = GibbsHoltzOPC(std_spt_number=22.5, eop=100.0)
>>> opc_cor.correction
2.0588
>>> opc_cor.corrected_spt_number
23.1615

Other correlations for calculating Overburden Pressure Corrections are:

- :class:`~geolysis.core.spt.BazaraaPeckOPC`
- :class:`~geolysis.core.spt.PeckOPC`
- :class:`~geolysis.core.spt.LiaoWhitmanOPC`
- :class:`~geolysis.core.spt.SkemptonOPC`

Correcting SPT N-values for water (dilatancy) influence:

>>> from geolysis.core.spt import DilatancyCorrection
>>> dil_cor = DilatancyCorrection(spt_number=22.5)
>>> dil_cor.corrected_spt_number
18.75
