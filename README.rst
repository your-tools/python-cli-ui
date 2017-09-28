python-cli-ui
=============

Tools for nice user interfaces in the terminal.

.. image:: https://img.shields.io/travis/TankerApp/python-cli-ui.svg?branch=master
  :target: https://travis-ci.org/TankerApp/python-cli-ui

.. image:: https://img.shields.io/pypi/v/python-cli-ui.svg
  :target: https://pypi.org/project/python-cli-ui/

.. image:: https://img.shields.io/github/license/TankerApp/python-cli-ui.svg
  :target: https://github.com/TankerApp/python-cli-ui/blob/master/LICENSE


Documentation
-------------


See `python-cli-ui documentation <https://tankerapp.github.io/python-cli-ui>`_.

Demo
----


Watch the `asciinema recording <https://asciinema.org/a/112368>`_.


Usage
-----

.. code-block:: console

    $ pip install python-cli-ui

Example:

.. code-block:: python

    import ui

    # coloring:
    ui.info("This is", ui.red, "red",
            ui.reset, "and this is", ui.bold, "bold")

    # enumerating:
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        ui.info_count(i, len(list_of_things), thing)

    # progress indication:
    ui.info_progress("Done",  5, 20)
    ui.info_progress("Done", 10, 20)
    ui.info_progress("Done", 20, 20)

    # reading user input:
    with_sugar = ui.ask_yes_no("With sugar?", default=False)

    fruits = ["apple", "orange", "banana"]
    selected_fruit = ui.ask_choice("Choose a fruit", fruits)

    #  ... and more!
