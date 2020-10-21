.. raw:: html
   
   <h1 align="center">Automatic Detection of Usability Smells Through the Analysis of Interaction Logs</h1>
   <p align="center"><strong>Bachelor's Degree in “Computer Science and Digital Communication”</strong></>

   <p align="center">
      Andrea Esposito (677021)<br>
      <small>Author</small><br>
      <a href="mailto:a.esposito39@studenti.uniba.it">a.esposito39@studenti.uniba.it</a>
   </p>
   <p align="center">
      Prof. Giuseppe Desolda<br>
      Supervisor<br>
      <a href="mailto:giuseppe.desolda@uniba.it">giuseppe.desolda@uniba.it</a>
   </p>
   <p align="center">
      <img alt="Test" src="https://github.com/espositoandrea/Bachelor-Thesis/workflows/Test/badge.svg" />
   </p>

********
        
The Structure of the Repository
===============================

``emotions/``
   This folder contains the Emotion Analysis Tool (written in C++).

``extension/``
   This folder contains the source code of the browser extension (written in
   TypeScript).

``icon/``
   This folder contains the logo and the icons of the project.

``server/``
   This folder contains the server's source code (written in JavaScript).


The Browser Extension
=====================

A simple browser extension was created to collect data for the Thesis' research.
The plugin is available for both Google Chrome and Mozilla Firefox.

The extension has the single goal of collecting the data that will be analyzed
in the Thesis. A detailed list of what is collected can be found in
`What data is collected?`_.

The Structure of the Extension
------------------------------

This extension is structured in two main parts: the extension itself and a group
of server-side scripts.

The extension itself collects the data (see `What data is collected?`_). In
this phase, in order to reduce the amount of work of the client's browser, the
webcam snapshots are sent as raw images (as data URIs). The collected data
(along with the pictures' URIs) are then sent to a server-side script.

The server receives the data sent by the extension and analyzes all available
pictures. The pictures are then discarded and only the analysis results are
saved.

The Survey
----------

Right after the installation of the extension, the participant is asked to
complete a short demographic survey. This survey (that is managed by a
server-side script) is needed to search for correlations in groups of users
with common age, experiences, knowledge, etc.

What data is collected?
-----------------------

* Date/time data
   - Date and time of the interaction
* Keyboard data
   - Pressed/released keys
* Mouse data
   - Mouse position in pixels (assumed to start from `(0,0)`)
   - Pressed/released mouse buttons
* Navigation data
   - Current URL (protocol and domain only)
   - Current scroll position
      + Absolute position in pixels
      + Relative position (measured from the lowest point of the screen)
* User's emotions
   - Data got from Affectiva_, an Emotion Analysis
     engine, by analyzing a snapshot taken with the webcam

.. _Affectiva: https://affectiva.com/

How to Build
------------

Both the extension and the server-side scripts have been created as a node
package. To build both, all the dependencies must be installed first. To install
them, run `npm install` in both the folder ``browser-extension/`` and the folder
``browser-extension/src/server/``.

Once all the dependencies have been installed, the extension as a whole (both
the client-side plugin and the server-side scripts) can be built by running 
``npm run build`` in the folder ``browser-extension``.

To start the server, run ``npm start`` from the same folder (note: starting the
server will trigger another build of the server-side scripts to ensure they're
updated at the latest version).


