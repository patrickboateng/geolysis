***************
Getting Started
***************

Installation
============

``geolysis`` can be installed via `pip <https://pypi.org/project/geolysis>`_ 
as follows for the supported operating systems.

.. tab-set:: 

    .. tab-item:: Windows
        :sync: win

        .. code::

            C:\> pip install geolysis

    .. tab-item:: Linux/Unix
        :sync: unix

        .. code::

            $ pip3 install geolysis

Version Check
=============

To see whether ``geolysis`` is already installed or to check if an install 
has worked, run the following in a Python shell: ::

    >>> import geolysis as gl
    >>> print(gl.__version__)

or, from the command line: 

.. tab-set:: 

    .. tab-item:: Windows
        :sync: win

        .. code:: shell

            C:\> py -c "import geolysis; print(geolysis.__version__)"

    .. tab-item:: Linux/Unix
        :sync: unix

        .. code:: shell

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
:doc:`API Reference </reference/index>`  page.

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
