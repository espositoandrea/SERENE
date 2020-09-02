The Survey
==========

Rationale
---------

To avoid the continuos editing of a verbose HTML file, the survey structure has
been parametrized. This allows to edit freely the survey without editing the
HTML file, and for this reason assures a consistent look to all the survey's
questions.

For this, a basic schema of the survey data has been defined. Note that this
schema is in no way enforced: there's no checking of your data and any
properties not defined in this schema won't raise any error but will be ignored.
On the other side, any defined and required property that's not defined in the
configuration object could block the HTML generation or (in the worst case)
generate a wrong HTML structure.

The Schema
----------

The survey is generated using the exported object defined in the module
``survey-data.js``. Here is documented the structure of that object.

.. js:autoclass:: Survey
   :members:

.. js:autoclass:: Section
   :members:


.. js:autoclass:: Question
   :members:

.. js:autoclass:: BasicQuestion
   :members:

.. js:autoclass:: ChoiceDescription
   :members:
