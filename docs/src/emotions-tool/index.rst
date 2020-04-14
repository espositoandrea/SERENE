Quick Start
===========

Installation
------------

To use the tool, download its compiled binary from the repository and execute it
from a console.

Requirements
~~~~~~~~~~~~

The tool has been tested on **Ubuntu Xenial 16.04**. The `Affdex API`_ is only
available on Windows and Ubuntu Xenial 16.04, so compatibility with other
Operative Systems is not guaranteed.

.. _Affdex API: https://github.com/Affectiva/cpp-sdk-samples/releases

From source with CMake
~~~~~~~~~~~~~~~~~~~~~~

Clone and open the `GitHub repository`_ in a console, using the following
commands:

.. _GitHub repository: https://github.com/espositoandrea/Bachelor-Thesis

.. code-block:: shell

   git clone https://github.com/espositoandrea/Bachelor-Thesis.git
   cd Bachelor-Thesis

Open the directory containing the tool's source code:

.. code-block:: shell

   cd emotions

Finally, create and compile the CMakeProject:

.. code-block:: shell

   mkdir bin
   cd bin
   cmake -DAFFDEX_DIR=/path/to/affdex/ -G "CodeBlocks - Unix Makefiles" ..
   make


Usage
-----

The tool can be used through CLI (or executed by another script).

::

    ./emotions [<option>...] IMAGE...

The argument ``IMAGE`` can be repeated several times. It must be either a data
URI or the path to a file containing a data URI. The available options are:

-h, --help   Get the help message
