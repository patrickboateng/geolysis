.. :html_theme.sidebar_secondary.remove:
.. currentmodule:: geolysis

**********************
geolysis documentation
**********************

.. note::

   We would like to inform you that our project is currently in the early stages 
   and we are actively developing the core features and functionalities of the 
   software, so kindly be patient if things change or features iterate and 
   change quickly.

   Once ``geolysis`` hits ``1.0.0``, it will slow down considerably in terms of
   breaking changes (i.e it will be backward compatible).


``geolysis`` is an open-source library for geotechnical analysis and modeling.
It offers tools for soil classification, Standard Penetration Test (SPT)
analysis, and bearing capacity estimation, among others.

Features
========

.. raw:: html
    :class: html-table-custom-style

    <table>
      <tr>
        <td rowspan="2" style="vertical-align: top;">
        <strong>Soil Classification</strong>
        </td>
        <td>AASHTO Classification System</td>
      </tr>
      <tr>
        <td>Unified Soil Classification System</td>
      </tr>
      <tr>
        <td rowspan="4" style="vertical-align: top;">
        <strong>Standard Penetration Test (SPT) Analysis</strong>
        </td>
        <td>SPT Energy Correction</td>
      </tr>
      <tr>
        <td>SPT Overburden Pressure Correction</td>
      </tr>
      <tr>
        <td>Dilatancy Correction</td>
      </tr>
      <tr>
        <td>SPT N-Design Calculation</td>
      </tr>
      <tr>
        <td rowspan="2" style="vertical-align: top;">
        <strong>Bearing Capacity Estimation</strong>
        </td>
        <td>Allowable Bearing Capacity Estimation</td>
      </tr>
      <tr>
        <td>Ultimate Bearing Capacity Estimation</td>
      </tr>
    </table>



Quick Example
=============

.. doctest::

   >>> from geolysis.soil_classifier import create_soil_classifier
   >>> uscs_clf = create_soil_classifier(liquid_limit=34.1,
   ...                                   plastic_limit=21.1,
   ...                                   fines=47.88,
   ...                                   sand=37.84,
   ...                                   clf_type="USCS")
   >>> clf = uscs_clf.classify()
   >>> clf
   SoilClf(symbol='SC', description='Clayey sands')
   >>> clf.symbol
   'SC'
   >>> clf.description
   'Clayey sands'

.. doctest::

   >>> from geolysis.soil_classifier import create_soil_classifier
   >>> aashto_clf = create_soil_classifier(liquid_limit=34.1, 
   ...                                     plastic_limit=21.1,
   ...                                     fines=47.88,
   ...                                     sand=37.84,  # Sand is optional for AASHTO classification
   ...                                     clf_type="AASHTO")
   >>> clf = aashto_clf.classify()
   >>> clf
   SoilClf(symbol='A-6(4)', description='Clayey soils')
   >>> clf.symbol
   'A-6(4)'
   >>> clf.description
   'Clayey soils'

.. toctree::
   :maxdepth: 2

   Getting Started <getting_started>

.. toctree::
   :maxdepth: 2

   Contributor's Guide <dev_guide/index>

.. toctree::
   :maxdepth: 2

   Release notes <release_notes/index>

.. toctree::
   :maxdepth: 2

   API Reference <reference/index>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
