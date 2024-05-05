***************
Getting Started
***************

Installation
============

We recommend using the latest version of python. ``geolysis`` supports
python 3.10 and newer. We also recommend using a `virtual environment 
<https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments>`_
in order to isolate your project dependencies from other projects and
the system.

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
