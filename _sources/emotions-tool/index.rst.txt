Quick Start
===========

Installation
------------

To use the tool, download its compiled binary from the repository and execute it
from a console.

.. IMPORTANT:: The tool has been tested on **Ubuntu Xenial 16.04**. 
   
   The `Affdex SDK`_ is only available on Windows and Ubuntu Xenial 16.04, so
   compatibility with other Operative Systems is not guaranteed.

.. _Affdex SDK: https://github.com/Affectiva/cpp-sdk-samples/releases

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
   cmake -G "CodeBlocks - Unix Makefiles" ..
   make


Usage
-----

.. IMPORTANT:: To use the tool you must have the `Affdex SDK`_ installed on your
   machine. Then, you have to add ``/path/to/affdex-sdk/lib`` to the variable
   ``$LD_LIBRARY_PATH`` (on Ubuntu). 

   .. code-block:: shell

      export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/affdex-sdk/lib/

   The tool will then search, in its folder, for the folder
   ``lib/affdex-sdk/data/`` (that has to contain the data used by Affdex).

The tool can be used through CLI (or executed by another script).

::

    ./emotions [<option>...] IMAGE...
    ./emotions [<option>...] --file FILE

Where ``IMAGE`` is a :ref:`data URI <data-uri>`. The available
options are:

-h, --help             Get the help message
-f FILE, --file FILE   The file containing the images to be analyzed (as a data
                       URI)
