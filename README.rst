rezume
======

Rezume is a Python library to validate and easily create a `YAML <https://yaml.org>`_
based resume file that is `JSON Resume <https://jsonresume.org>`_ compatible according to
the `defined schema <https://jsoonresume.org/schema>`_.


Installation
------------

Install from `Pypi <https://pypi.org/project/rezume/>`_ by running this command:

.. code-block::

    pip install rezume


Dependencies
^^^^^^^^^^^^

Rezume requires Python 3.6+ and depends mainly on `pydantic <https://pypi.org/project/pydandic>`_
for data validation and `pyyaml <https://pypi.org/project/>`_ for processing YAML data.


Usage
-----

You can use ``rezume`` as a Python package as shown below:

.. code-block:: python

    from rezume import RezumeError, Rezume

    # sample (invalid) rezume data to validate
    rezume_data = { name: 'John Doe' }

    # check the validity of sample data
    if Rezume.is_valid(rezume_data):
        print('Validated successfully!')
    else:
        print('Invalid rezume')

    # alternatively, if we prefer catching exceptions
    try:
        Rezume.validate(rezume_data)
        print('Validated successfully!')
    except RezumeError as ex:
        print(f'Invalid rezume: {ex}')


To validate a rezume file instead:

.. code-block:: python

    from pathlib import Path
    from rezume import RezumeError, Rezume

    # path to sample file to validate
    rezume_file = Path('/path/to/sample/rezume-file.yml')

    # use
    Rezume.is_valid(rezume_file)    # returns boolean

    or
    Rezume.validate(rezume_file)    # throws exception if invalid


Furthermore, you can programmatically process a Rezume:

.. code-block:: python

    import json
    from pathlib import Path
    from rezume import RezumeError, Rezume

    # load and modify a standard JSON resume

    rezume = Rezume()

    json_file = Path('/path/to/json/resume-file.json')
    with json_file.open('r') as fp:
        data = json.load(fp)
        rezume.load_data(data)   # throws exception if invalid

    rezume.basics.name = 'John Doe (Verified)'
    print(rezume.dump_data())


    # or programmatically modify a YAML rezume file

    yaml_file = Path('/path/to/yaml/rezume-file.yml')
    try:
        rezume = Rezume()
        rezume.load(yaml_file)  # throws exception if invalid
    except RezumeError:
        print('Unable to process rezume file')
    else:
        rezume.basics.label = 'Pythonista'
        print(rezume.dump_data())


In addition, ``rezume`` can be used as a command line tool to create or validate
a YAML-based rezume file. Here is the output of ``rezume --help``

.. code-block:: bash

    Usage: rezume [OPTIONS] COMMAND [ARGS]...

    Options:
      --install-completion  Install completion for the current shell.
      --show-completion     Show completion for the current shell, to copy it or
                              customize the installation.

      --help                Show this message and exit.

    Commands:
      init   Initializes a new rezume.yml file
      serve  Serves a rezume for local viewing applying available themes
      test   Validates correctness of a rezume.yml file


License
-------

This project is licensed under the `BSD license <LICENSE>`_
