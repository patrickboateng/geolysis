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

``geolab`` is an open-source software for geotechnical engineering analysis that offers a suite of powerful tools and features for soil analysis and modeling. 

Features
--------

- Provides soil classification based on ``USCS`` and ``AASHTO`` standards.
- Bearing capacity analysis can be performed in both from results obtained from laboratory or field tests.
- Estimates important soil engineering properties, aiding in decision-making.
- Settlement analysis tools predict and model soil settlements under various loads and conditions.
- Supports finite element modelling of soil behaviour under different conditions.

.. note::

   Not all features mentioned above are availabe.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: :octicon:`paper-airplane;1.5em;sd-text-info` Getting Started
      :link: quickstart
      :link-type: doc

      Start here if you are new to geolab. Learn about the syntax and the Microsoft Excel addin.

   .. grid-item-card:: :octicon:`book;1.5em;sd-text-info` API Reference
      :link: api/index
      :link-type: doc

      This is a description of all classes, methods, properties, and functions that geolab offers.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   quickstart
   api/index

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
