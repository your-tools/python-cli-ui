.. image::  https://tanker.io/images/github-logo.png
   :target: #readme

|

.. image:: https://img.shields.io/travis/TankerHQ/python-cli-ui.svg?branch=master
  :target: https://travis-ci.org/TankerHQ/python-cli-ui

.. image:: https://img.shields.io/pypi/pyversions/cli-ui.svg
  :target: https://pypi.org/project/cli-ui

.. image:: https://img.shields.io/pypi/v/cli-ui.svg
  :target: https://pypi.org/project/cli-ui/

.. image:: https://img.shields.io/github/license/TankerHQ/python-cli-ui.svg
  :target: https://github.com/TankerHQ/python-cli-ui/blob/master/LICENSE

.. image:: https://img.shields.io/badge/deps%20scanning-pyup.io-green
  :target: https://github.com/TankerHQ/python-cli-ui/actions

python-cli-ui
=============

Tools for nice user interfaces in the terminal.

Documentation
-------------


See `python-cli-ui documentation <https://TankerHQ.github.io/python-cli-ui>`_.

Demo
----


Watch the `asciinema recording <https://asciinema.org/a/112368>`_.


Usage
-----

.. code-block:: console

    $ pip install cli-ui

Example:

.. code-block:: python

    import cli_ui

    # coloring:
    cli_ui.info(
      "This is",
      cli_ui.red, "red", cli_ui.reset,
      "and this is",
      cli_ui.bold, "bold"
    )

    # enumerating:
    list_of_things = ["foo", "bar", "baz"]
    for i, thing in enumerate(list_of_things):
        cli_ui.info_count(i, len(list_of_things), thing)

    # progress indication:
    cli_ui.info_progress("Done",  5, 20)
    cli_ui.info_progress("Done", 10, 20)
    cli_ui.info_progress("Done", 20, 20)

    # reading user input:
    with_sugar = cli_ui.ask_yes_no("With sugar?", default=False)

    fruits = ["apple", "orange", "banana"]
    selected_fruit = cli_ui.ask_choice("Choose a fruit", choices=fruits)

    #  ... and more!
