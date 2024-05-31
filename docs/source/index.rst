:html_theme.sidebar_secondary.remove:

***************************
geolysis.core documentation
***************************

.. toctree::
   :hidden:

   Getting Started     <getting_started>
   API Reference       <reference/geolysis/core/index>
   Contributor's Guide <dev/index>
   Release notes       <release_notes/index>
   About Us            <about>

``geolysis.core`` is an open-source software that provides features
for analyzing geotechnical results obtained from laboratory and field
tests. Some of the features implemented include soil classification,
standard penetration test analysis (such as SPT :math:`N_{design}` and
SPT N-value corrections), and calculating the allowable bearing capacity
of soils from Standard Penetration Test N-values. There are more
features underway, which include settlement analysis, ultimate bearing
capacity analysis, etc.

``geolysis.core`` is the foundation application on which other parts
of the application will depend. Developers can also use  the
``geolysis.core`` package to power their applications.


As of the ``0.3.0`` release, ``geolysis`` only provides the ``core``
package which includes tools for geotechnical engineers to perform
analysis on results obtained from laboratory and field tests.

Check out the `about page <about.html>`_ for a more comprehensive
overview of the vision and mission of ``geolysis``.

.. note::

   We would like to inform you that our project is currently in the
   early stages and we are actively developing the core features and
   functionalities of the software, so kindly be patient if things
   change or features iterate and change quickly.

   Once ``geolysis.core`` hits ``1.0.0``, it will slow down considerably.

.. grid:: 3
   :gutter: 2

   .. grid-item-card::
      :link: getting_started
      :link-type: doc

      :fas:`person-running;1em;sd-text-info` Getting Started
      ^^^

      New to ``geolysis``? Check out the absolute beginner's guide.

   .. grid-item-card::
      :link: reference/geolysis/core/index
      :link-type: doc

      :fas:`code;1em;sd-text-info` API Reference
      ^^^

      This is a description of all packages, modules, classes, and
      functions that ``geolysis.core`` offers.

   .. grid-item-card::
      :link: dev/index
      :link-type: doc

      :fas:`terminal;1em;sd-text-info` Contributor's Guide
      ^^^

      Want to add to the codebase? Check out the contribution guidelines.

   .. grid-item-card::
      :link: release_notes/index
      :link-type: doc

      :fas:`history;1em;sd-text-info` Release notes
      ^^^

      Want to know how ``geolysis`` has evolved? Check out the release
      notes.

   .. grid-item-card::
      :link: about
      :link-type: doc

      :fas:`users;1em;sd-text-info` About Us
      ^^^

      Want to know more about the ``geolysis`` project? Checkout the about
      page for a comprehensive look at ``geolysis``.

   .. grid-item-card::
      :link: dev/style_guide
      :link-type: doc

      :fas:`pen-to-square;1em;sd-text-info` Style Guide
      ^^^

      Style guides for developing ``geolysis.core``.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
