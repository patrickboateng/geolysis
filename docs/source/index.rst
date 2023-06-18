.. geolab documentation master file, created by
   sphinx-quickstart on Fri May 19 10:05:15 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


geolab: Geotechnical engineering analysis and modelling software
================================================================

.. image:: https://img.shields.io/badge/PyPi-Pato546-blue?style=flat-square&logo=pypi&logoColor=white 
   :alt: pypi
   :target: https://pypi.org/user/Pato546/

.. image:: https://img.shields.io/pypi/l/geolab?style=flat-square
   :alt: license

.. image:: https://img.shields.io/pypi/dm/geolab?style=flat-square
   :alt: downloads

geolab
------

`geolab` is an open-source software for geotechnical engineering that offers a suite of powerful tools and features for soil analysis and modeling. It provides soil classification based on both USCS and AASHTO standards, bearing capacity analysis, estimation of soil engineering properties, settlement analysis, and finite element modeling. The software assists geotechnical engineers in their day-to-day work, enabling them to perform a wide range of tasks with ease and make informed decisions about design and construction. `geolab` enhances efficiency and effectiveness, allowing engineers to design and build better projects with confidence.

Features
--------

- Provides soil classification based on `USCS` and `AASHTO` standards.
- Bearing capacity analysis can be performed in both from results obtained from laboratory or field tests.
- Estimates important soil engineering properties, aiding in decision-making.
- Settlement analysis tools predict and model soil settlements under various loads and conditions.
- Supports finite element modelling of soil behaviour under different conditions.


Installation
------------

Windows:

.. note:: 

    This install does not work yet. This project is under **rapid** development.

.. code:: bash

   pip install geolab

A simple usage example
----------------------

.. doctest:: 

   >>> from geolab.soil_classifier import aashto, uscs
   >>> uscs(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88, sand=37.84, gravels=14.28)
   'SC'
   >>> aashto(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88)
   'A-6(3)'

Release History
---------------

- 0.1.0
  - **rapid** development.


.. Contributing
.. ------------

.. #. [Fork it](https://github.com/patrickboateng/geolab/fork)
.. #. Create your feature branch (`git checkout -b feature`)
.. #. Commit your changes (`git commit -am 'Add some fooBar'`)
.. #. Push to the branch (`git push origin feature`)
.. #. Create a new Pull Request

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference
   soil_classification

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
