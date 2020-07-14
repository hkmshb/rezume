rezume
======

This is a command line tool to easily create and validate a text-based resume. Inspired
by [JSON Resume](https://jsonresume.org), it currently supports only the yaml format.


Getting Started
---------------
Install rezume from Pypi

.. code-block::

    pip install rezume


Usage
-----
Create a new rezume in the current working directory

.. code-block::

    rezume init [FILENAME: default=rezume.yml]


Validate a rezume file:

.. code-block::

    rezume test [FILENAME: default=rezume.yml]
