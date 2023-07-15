geolab
==========

``geolab`` is an open-source software for geotechnical engineering analysis and modelling.

.. image:: https://img.shields.io/badge/PyPi-Pato546-blue?style=flat-square&logo=pypi&logoColor=white 
   :alt: pypi
   :target: https://pypi.org/user/Pato546/

.. image:: https://img.shields.io/pypi/l/geolab?style=flat-square
   :alt: license

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336
  :alt: isort
  :target: https://pycqa.github.io/isort/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square
  :alt: black
  :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/code%20formatter-docformatter-fedcba.svg?style=flat-square
  :alt: docformatter
  :target: https://github.com/PyCQA/docformatter

.. image:: https://img.shields.io/badge/%20style-google-3666d6.svg?style=flat-square
  :alt: style guide
  :target: https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings

.. image:: https://img.shields.io/github/repo-size/patrickboateng/geolab?style=flat-square&labelColor=ef8336
  :alt: repo size

.. image:: https://img.shields.io/pypi/dm/geolab?style=flat-square
   :alt: downloads

``geolab`` is an open-source software for geotechnical engineering that offers a suite of 
powerful tools and features for soil analysis and modeling. It provides soil classification based 
on both USCS and AASHTO standards, bearing capacity analysis, estimation of soil engineering properties, 
settlement analysis, and finite element modeling. The software assists geotechnical engineers in their 
day-to-day work, enabling them to perform a wide range of tasks with ease and make informed decisions 
about design and construction. ``geolab`` enhances efficiency and effectiveness, allowing engineers to 
design and build better projects with confidence.

Features
--------

- Provides soil classification based on `USCS` and `AASHTO` standards.
- Bearing capacity analysis can be performed, both from results obtained from **laboratory** or **field**.
- Estimates important soil engineering properties, aiding in decision-making.
- Settlement analysis tools to predict and model soil settlements under various loads and conditions.
- Supports finite element modelling of soil behaviour under different conditions.

.. contents:: 
.. ## Table of Contents

.. - [Installation](#installation)
.. - [Usage Example](#usage-example)
.. - [Release History](#release-history)
.. - [Contributing](#contributing)
.. - [License](#license)
.. - [Contact Information](#contact-information)
.. - [Links](#links)
.. - [Todo](#todo)

Installation
------------

.. note:: 

  This install does not work yet. Project is still under **rapid** development.

.. code::

  pip install geolab

Usage example
-------------

.. doctest::

  >>> from geolab.soil_classifier import aashto, uscs
  >>> uscs(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88, sand=37.84, gravels=14.28)
  'SC'
  >>> aashto(liquid_limit=34.1, plastic_limit=21.1, plasticity_index=13, fines=47.88)
  'A-6(3)'

Release History
---------------

* 0.1.0
  - **rapid** development.

Contributing
------------

#. `Fork it <https://github.com/patrickboateng/geolab/fork>`_
#. Create your feature branch (``git checkout -b feature``)
#. Commit your changes (``git commit -am 'Add some fooBar'``)
#. Push to the branch (``git push origin feature``)
#. Create a new Pull Request

License
-------

Distributed under the ``MIT license``. See `LICENSE <./LICENSE.txt>`_ for more information.

Contact Information
-------------------

- Email: boatengpato.pb@gmail.com, 
- LinkedIn: https://linkedin.com/in/patrickboateng/

.. note::

  For questions or comments about geolab, please contact boatengpato.pb@gmail.com

Links
-----

- `Documentation <https://>`_
- `PyPi <https://>`_
- `Source Code <https://github.com/patrickboateng/geolab/>`_
- `Issue Tracker <https://>`_
- `Website <https://>`_

.. Todo
.. ----

.. - [x] Soil Classifier
.. - [x] Bearing Capacity Analysis
.. - [x] Estimating Soil Engineering Parameters
.. - [ ] Settlement Analysis
.. - [ ] Modelling the behavior of Soils under loads using ``FEM``
