Quick Start
===========

Installation
------------

To install the tool, download the tool's folder and execute the following
commands (replace ``/path/to/analyzer/`` with the path to the downloaded
folder).

.. code-block:: sh
    :caption: How to install the tool

    cd /path/to/analyzer
    python3 -m pip install .

Usage
-----

The Command Line Interface
++++++++++++++++++++++++++

Once installed you can use this tool from your terminal using the command
``analyzer``.

.. code-block::
    :caption: The tool's CLI
    
    analyzer [-h] [--version] [-v] file users

.. NOTE:: You can execute the tool as a Python module, without installing it
   first. Download the tool's folder and execute the following commands (replace
   ``/path/to/analyzer/`` with the path to the downloaded folder).
   
   .. code-block:: sh
      :caption: How to execute the tool as a Python module

      cd /path/to/analyzer
      python3 -m data_processor --help


Process the JSON file

Positional Arguments
********************

file
    The file
users
    A JSON file containing the users

Optional Arguments
******************

-h, --help     show this help message and exit
--version      output version information and exit
-v, --verbose  increase output verbosity

The Code API
++++++++++++

Once installed you can use the tool as a Python module. Read the 
:ref:`code documentation <python-code-doc>` for more information on the API.
