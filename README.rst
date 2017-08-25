python-cli-ui
=============

Tools for nice user interfaces in the terminal.


Demo:
-----


Run ``python3 ui.py`` and be amazed!

Or just watch the `asciinema recording <https://asciinema.org/a/112368>`_


Usage
-----



.. code-block:: python

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


FAQ
---

Python2 support?
~~~~~~~~~~~~~~~~

* No. If you need this, feel free to create your own fork :)

Windows support?
~~~~~~~~~~~~~~~~

* Yes! Should work in `mintty` and `cmd.exe` at least.

Documentation?
~~~~~~~~~~~~~~

Use the source, Luke!
