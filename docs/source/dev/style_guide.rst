******************
Python Style Guide
******************

Docstring Structure for Classes
===============================

- Short Description
- Long Description
- Parameter Info
- Usage Example if any
- Autosummary of public members (properties/attributes & methods)
- Reference if any

Docstring Structure for Functions
=================================

- Short Description
- Long Description
- Parameter Info
- Usage Example
- Reference

.. TODO: Add docstring examples for functions and classes

"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

Importing
=========

``geolysis`` can be imported as follows: ::

    >>> import geolysis as gl

Most functions/classes of ``geolysis`` are found within submodules: ::

    >>> spt_corr = gl.spt.SPTCorrections()

A list of submodules and functions is found on the 
:doc:`API Reference </reference/geolysis/index>`  page.

The :mod:`geolysis.spt` submodule provides a set of functions and 
classes for analyzing and correcting SPT N-values. ::

    >>> corrected_spt_n_vals = [7.0, 15.0, 18.0]
    >>> gl.spt.weighted_avg_spt_n_val(corrected_spt_n_vals)
    9.0

It is recommended to import submodules as follows: ::

    >>> from <pkg> import <submodule>
    >>> from geolysis import spt

Also it is recommended to import functions/classes as follows: ::

    >>> from <pkg>.<submodule> import function, class
    >>> from geolysis.spt import weighted_avg_spt_n_val, SPTCorrections

Or: ::

    >>> from <pkg>.<subpkg>.<submodule> import object
    >>> from geolysis.bearing_capacity.abc import BowlesABC1997
