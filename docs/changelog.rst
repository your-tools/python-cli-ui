Changelog
----------

v0.14.1
+++++++

* Development branch is now called ``main``.
* Fix #66 - only call ``colorama.init()`` on Windows.

v0.14.0 (2021-04-20)
++++++++++++++++++++

* **breaking**:  Remove buggy workarounds on Windows.
  Colors will now be off by default unless ``cli_setup()`` is called
  with ``color="always"``. Configurations that are known to work are
  ``cmd.exe`` and ``git-bash`` when using ``winpty``.

* **breaking**:  ``colorama.init()`` is called unconditionally when ``cli_ui`` is
  imported

v0.13.0 (2021-04-19)
++++++++++++++++++++

* Move out of `TankerHQ` GitHub organization

v0.12.0 (2021-02-11)
+++++++++++++++++++++

* Fix using `info_table` with `keys="headers"`

v0.11.0 (2020-07-23)
++++++++++++++++++++

* Remove Python 3.5 compat
* Add a ``__repr__`` method to some of the classes

v0.10.3 (2020-04-29)
++++++++++++++++++++

* Mark this package as typed

v0.10.2 (2020-02-10)
++++++++++++++++++++

* Fix calling `cli_ui.dot()` without `fileobj` argument.

v0.10.1 (2020-02-04)
++++++++++++++++++++

* Switch to `poetry`_ for packaging and dependency management.

v0.10.0 (2019-12-02)
++++++++++++++++++++

* Add a ``sort`` argument to the ``ask_choices()`` function to disable sorting
  the list of choices. Patch by ``@smandon``.
* CI: Drop Python 3.4, add Python 3.8, switch to GitHub Actions

v0.9.1 (2018-12-18)
+++++++++++++++++++

* Relax type constraints for the ``info_table()`` function.

v0.9.0 (2018-12-18)
++++++++++++++++++++

* Relax constraints on the ``Token`` type.
* Expose the ``MessageRecorder`` class, not the ``pytest`` fixture.

v0.8.0 (2018-12-14)
+++++++++++++++++++

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
  of `cli_ui` constants. All existing names have been kept, but some of the values changed slightly.

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
* If you need the ``record_message()`` pytest fixture in your own tests, you can now
  import it with ``from cli_ui.tests import message_recorder``.

v0.7.4 (2018-11-22)
+++++++++++++++++++

* Remove buggy ``entry_points`` from ``setup.py``.

v0.7.3 (2018-11-06)
++++++++++++++++++++

* Switch to ``dmenv``. This makes it possible to use ``cli-ui`` with ``colorama >= 4.0``.

v0.7.2 (2018-10-11)
+++++++++++++++++++

* Switch to `poetry <https://poetry.eustace.io>`_ .

v0.7.1 (2018-03-29)
++++++++++++++++++++

* Fix crash in ``ask_password`` when password was empty.
* Let the :py:exc:`KeyboardInterrupt`` exception propagate back to the caller instead of catching
  it ourselves and returning ``None``. Reported by Théo Delrieu.

v0.7.0 (2018-03-06)
+++++++++++++++++++++

* Add ``ask_password`` and ``read_password``. Patch by @drazisil

v0.6.1 (2017-12-07)
+++++++++++++++++++

* Fix metadata (owner moved from TankerApp to TankerHQ)

v0.6.0 (2017-10-30)
+++++++++++++++++++

* Export ``Color`` class.

v0.5.0 (2017-10-04)
++++++++++++++++++++

* Export a ``Symbol`` class, to use when you do not want to force
  color as  with ``UnicodeSequence``

v0.4.0 (2017-09-27)
+++++++++++++++++++

* Expose the previously private ``UnicodeSequence`` class.

v0.3.0 (2017-09-13)
+++++++++++++++++++

* Add ``info_section``

* Cosmetic changes about prefixes for ``debug``, ``warn`` and ``error``
  messages. (See `#6 <https://github.com/TankerHQ/python-cli-ui/pull/6>`_
  for the details)


v0.2.0 (2017-09-01)
++++++++++++++++++++

* Add ``cli_ui.setup`` to configure things like verbosity and when to
  use colored output (#3)

* Add a ``message_recorder`` in ``cli_ui.tests.conf`` that can
  be used as a ``pytest`` fixture in other projects.

v0.1.0 (2017-08-25)
+++++++++++++++++++

First public release
