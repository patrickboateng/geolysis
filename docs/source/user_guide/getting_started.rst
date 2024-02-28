***************
Getting Started
***************

Installation
============

``geolysis`` can be installed via `pip <https://pypi.org/project/geolysis>`_ 
as follows for the supported operating systems.

.. tabs::

    .. group-tab:: Windows

        .. code::

            C:\> pip install geolysis

    .. group-tab:: Linux/Unix

        .. code::

            $ pip3 install geolysis

Version Check
=============

To see whether ``geolysis`` is already installed or to check if an install 
has worked, run the following in a Python shell: ::

    >>> import geolysis as gl
    >>> print(gl.__version__)

or, from the command line: 

.. tabs:: 

    .. group-tab:: Windows

        .. code::

            C:\> py -c "import geolysis; print(geolysis.__version__)"

    .. group-tab:: Linux/Unix

        .. code::

            $ python3 -c "import geolysis; print(geolysis.__version__)"

You'll see the version number if ``geolysis`` is installed and an
error message otherwise.

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
