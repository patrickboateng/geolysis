Developer Documentation
=======================

This page provides an overview of how the project is organized for both the
source code and documentation.

Layout of Project Source Code
-----------------------------

The ``geolysis`` folder contain all the source code for the project, and it is
the root (main package namespace) of the project.

- ``bearing_capacity`` package (folder) contains the code for bearing
  capacity analysis.
- ``utils`` package (folder) contains useful objects (exception classes,
   validators, decorators, etc) that are used across the project.
- ``foundation.py`` module contains classes for representing a foundation.
- ``soil_classifier.py`` module contains classes for soil classification.
- ``spt.py`` module contains classes for Standard Penetration Test Analysis.

Layout of Project Documentation
-------------------------------

The ``docs`` folder contain all the documentation files for the project, and
it is the root for the documentation.

- ``_static`` folder contain all the JavaScript, CSS, and images for the docs.
- ``_templates`` folder contain templates for customizing the docs. It is
  currently empty.
- ``dev_guide`` folder contain information for contributors.
- ``reference`` folder contain the code reference documentation.
- ``release_notes`` folder contain all the release notes.
- ``user_guide`` folder contain information for users.

All (or most) of the files found in the root of the ``geolysis`` and ``docs``
folders are metadata files.

.. toctree::
    :maxdepth: 2
    :hidden:

    Contributing        <../CONTRIBUTING.md>
    Code of Conduct     <../CODE_OF_CONDUCT.md>
    Style Guide         <style_guide.rst>
