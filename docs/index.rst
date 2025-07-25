.. :html_theme.sidebar_secondary.remove:
.. currentmodule:: geolysis

**********************
geolysis documentation
**********************

.. toctree::
   :maxdepth: 2
   :hidden:

   User Guide               <user_guide/index>
   Contributor's Guide      <dev_guide/index>
   Release notes            <release_notes/index>
   API Reference            <reference/geolysis/index>

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

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Soil Classification**
     - AASHTO Classification System
   * -
     - Unified Soil Classification System
   * - **Standard Penetration Test (SPT) Analysis**
     - SPT Energy Correction
   * -
     - SPT Overburden Pressure Correction
   * -
     - SPT Dilatancy Correction
   * -
     - SPT N-Design Calculation
   * - **Bearing Capacity Estimation**
     - Allowable Bearing Capacity Estimation
   * -
     - Ultimate Bearing Capacity Estimation

Quick Example
=============

>>> from geolysis.soil_classifier import create_uscs_classifier
>>> uscs_clf = create_uscs_classifier(liquid_limit=34.1,
...                                   plastic_limit=21.1,
...                                   fines=47.88,
...                                   sand=37.84, )
>>> clf = uscs_clf.classify()
>>> clf.symbol
'SC'
>>> clf.description
'Clayey sands'


>>> from geolysis.soil_classifier import create_aashto_classifier
>>> aashto_clf = create_aashto_classifier(liquid_limit=34.1,
...                                     plastic_limit=21.1,
...                                     fines=47.88, )
>>> clf = aashto_clf.classify()
>>> clf.symbol
'A-6(4)'
>>> clf.description
'Clayey soils'

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
