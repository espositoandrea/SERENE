Introduction
============

Folder Structure
----------------

The ``server/`` folder contains all the source code of the developed server. Its
structure is the following (all described folders are subfolders of
``server/``).

``views/``
    This folder contains all the views developed for the server.
    
    ``views/layouts/``
        This folder contains the layouts used to define the views. 

``survey/``
    This folder contains all the required data for the survey.

``assets/``
    This folder contains all the static files that will be served without any
    modification. 
    
    ``assets/images/`` 
        A folder that contains all the images and illustrations used.
    
    ``assets/js/``
        A folder that contains all the external JavaScript files (needed by the
        extension).
    
    ``assets/style/``
        A folder that contains all the stylesheets of the server (written in
        SASS_).

.. _SASS: https://sass-lang.com/
