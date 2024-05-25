******************
Python Style Guide
******************

We follow the `PEP8 <https://peps.python.org/pep-0008/>`_ style guide
for formatting Python code. Docstrings follow
`PEP257 <https://peps.python.org/pep-0257/>`_. Also Please
see `PEP258 <https://peps.python.org/pep-0258/>`_, "Docutils Design
Specification", for a detailed description of attributes and
additional docstrings.

`NumPy docstrings style guide <https://numpydoc.readthedocs.io/en/latest/format.html>`_
is used as the documentation format for documenting objects (``packages``,
``modules``, ``classes``, ``methods``, ``functions`` and ``GLOBAL variables``)
in this package. It is recommended to read the NumPy docstrings style
guide before contributing code to ``geolysis``.

The rest of the document describes additions and clarifications to
the PEP documents that we follow.

Indentation
===========

Use 4 spaces (no tabs) for indentation.

Import convention
=================

All imports should be at the top of the file grouped into 3 sections
and separated by blanklines. The sections should be, **system imports**,
**third party imports**, and **geolysis imports**.

It is recommended to import modules/submodules as follows::

    import module_name
    from pkg_name import module_name
    from pkg_name.subpkg import module_name

It is also recommended to import classes/functions as follows::

    from module_name import class_name, func_name
    from pkg_name.module_name import class_name, func_name

You can import the main ``geolysis`` namespace as::

    import geolysis as gl

You can also import the ``core`` package as::

    import geolysis.core as glc

Code Documentation
==================

Documenting Packages/Modules
----------------------------

Docstring sections for modules:

#. Short Summary
#. Extended summary
#. Routine listings
#. See also
#. Notes
#. References if any
#. Examples

Documenting Classes
-------------------

Docstring sections for classes:

#. `Short Summary <https://numpydoc.readthedocs.io/en/latest/format.html#short-summary>`_
#. `Extended Summary <https://numpydoc.readthedocs.io/en/latest/format.html#extended-summary>`_
#. `Parameters <https://numpydoc.readthedocs.io/en/latest/format.html#parameters>`_
#. `Attributes <https://numpydoc.readthedocs.io/en/latest/format.html#class-docstring>`_
#. `Raises if any <https://numpydoc.readthedocs.io/en/latest/format.html#raises>`_
#. `See Also <https://numpydoc.readthedocs.io/en/latest/format.html#see-also>`_
#. `Notes <https://numpydoc.readthedocs.io/en/latest/format.html#notes>`_
#. `References if any <https://numpydoc.readthedocs.io/en/latest/format.html#reference>`_
#. `Examples <https://numpydoc.readthedocs.io/en/latest/format.html#examples>`_

Summary of public methods is automatically added by `numpydoc <https://numpydoc.readthedocs.io/en/latest/install.html>`_
sphinx extension.

Objects in a class should be arranged in the following order:

#. Class Variables
#. Dunder Methods (eg. ``__init__``, ``__str__``, etc)
#. Private Methods/Properties (eg. ``_foo(self)``)
#. Public Properties
#. Instance Methods
#. Class Methods
#. Static Methods

Docstring Structure for Functions
---------------------------------

Docstring sections for functions/methods:

#. Short Summary
#. Extended Summary
#. Parameters (Do not include ``self`` as a parameter for methods)
#. Raises
#. Returns
#. See Also
#. Notes
#. References if any
#. Examples

Documenting Constants
---------------------

Docstring sections for module constants:

#. Short Summary
#. Extended Summary (optional)
#. See Also (optional)
#. References (optional)
#. Examples (optional)

.. note::

    Docstrings for constants (or primitive types) will not be visible
    in text terminals because the ``__doc__`` attribute is read-only,
    but will appear in the documentation built with Sphinx.
