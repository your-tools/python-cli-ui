Changelog
----------

v0.10.2
+++++++

* Fix calling `cli_ui.dot()` without `fileobj` argument.

v0.10.1
+++++++

* Switch to `poetry`_ for packaging and dependency management.

v0.10.0
+++++++

* Add a ``sort`` argument to the ``ask_choices()`` function to disable sorting
  the list of choices. Patch by ``@smandon``.
* CI: Drop Python 3.4, add Python 3.8, switch to GitHub Actions

v0.9.1
++++++

* Relax type constraints for the ``info_table()`` function.

v0.9.0
++++++

* Relax constraints on the ``Token`` type.
* Expose the ``MessageRecorder`` class, not the ``pytest`` fixture.

v0.8.0
++++++

Highlights
~~~~~~~~~~

* **Breaking change**: Rename main package from ``ui`` to ``cli_ui``. This name is less likely to
  cause clash with existing code::

    # old (<= 0.7)
    import ui
    ui.info("This is", ui.green, "green")

    # new (>= 0.8)
    import cli_ui
    cli_ui.info("This is", cli_ui.green, "green")



* **Breaking change**:  use `colorama` instead of hard-coding ANSI sequences names and values
  of `cli_ui` constants. All existing names have been kept, but some of the values changed slighlty.

* ``ask_`` functions now take a variable number of tokens as first argument.
  This allows to color the prompt when requiring input from the user, for instance::

    res = cli_ui.ask_yes_no(
      "Deploy to",
      cli_ui.bold, "production", cli_ui.reset, "?",
      default=False
    )

* **Breaking change**: Because of this new feature, the list of choices used by
  ``ask_choice`` is now a named keyword argument::

    # Old (<= 0.7)
    ask_choice("select a fruit", ["apple", "banana"])
    # New (>= 0.8)
    ask_choice("select a fruit", choices=["apple", "banana"])


Other Changes
~~~~~~~~~~~~~~

* Annotate everything with ``mypy``.
* Use ``black`` for automatic code formatting.
* If you nedd the ``record_message()`` pytest fixture in your own tests, you can now
  import it with ``from cli_ui.tests import message_recorder``.

v0.7.4
++++++

* Remove buggy ``entry_points`` from ``setup.py``.

v0.7.3
++++++

* Switch to ``dmenv``. This makes it possible to use ``cli-ui`` with ``colorama >= 4.0``.

v0.7.2
++++++

* Switch to `poetry <https://poetry.eustace.io>`_ .

v0.7.1
++++++

* Fix crash in ``ask_password`` when password was empty.
* Let the :py:exc:`KeyboardInterrupt`` exception propagate back to the caller instead of catching
  it ourselves and returning ``None``. Reported by Théo Delrieu.

v0.7.0
++++++

* Add ``ask_password`` and ``read_pasword``. Patch by @drazisil

v0.6.1
++++++

* Fix metadata (owner moved from TankerApp to TankerHQ)

v0.6.0
++++++

* Export ``Color`` class.

v0.5.0
++++++

* Export a ``Symbol`` class, to use when you do not want to force
  color as  with ``UnicodeSequence``

v0.4.0
++++++

* Expose the previously private ``UnicodeSequence`` class.

v0.3.0
++++++

* Add ``info_section``

* Cosmetic changes about prefixes for ``debug``, ``warn`` and ``error``
  messages. (See `#6 <https://github.com/TankerHQ/python-cli-ui/pull/6>`_
  for the details)


v0.2.0
++++++

* Add ``cli_ui.setup`` to configure things like verbosity and when to
  use colored output (#3)

* Add a ``message_recorder`` in ``cli_ui.tests.conf`` that can
  be used as a ``pytest`` fixture in other projects.

v0.1.0
+++++++

First public release.
