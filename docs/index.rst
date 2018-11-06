Python CLI UI
=============

.. module:: ui

Tools for nice user interfaces in the terminal.

Installation
-------------

``python-cli-ui`` is available on `Pypi <https://pypi.org/project/python-cli-ui/>`_
and is compatible with Python **3.4** and higher.

It depends on ``colorama`` and ``unidecode`` for Windows support, and on
``tabulate`` for the :func:`info_table` function.

.. note:: The name of the Pypi package is ``python-cli-ui``, but after you
          install it, you should use ``import ui`` to use it.

API
----

Configuration
+++++++++++++

.. autofunction:: setup

::

  >>> ui.debug("this will not be printed")
  <nothing>
  >>> ui.setup(verbose=True)
  >>> ui.debug("this will be printed")
  this will be printed


Constants
++++++++++

You can use any of these constants as a ``token`` in the following functions:

* Effects:

  * ``bold``
  * ``faint``
  * ``standout``
  * ``underline``
  * ``blink``
  * ``overline``
  * ``reset``

* Colors:

  * ``black``
  * ``blue``
  * ``brown``
  * ``darkblue``
  * ``darkgray``
  * ``darkgreen``
  * ``darkred``
  * ``darkyellow``
  * ``fuchsia``
  * ``fuscia``
  * ``green``
  * ``lightgray``
  * ``purple``
  * ``red``
  * ``teal``
  * ``turquoise``
  * ``white``
  * ``yellow``

.. note:: Each of these constants is an instance of :class:`Color`.

* Sequence of Unicode characters:

  * ``check``: ✓ (green, replaced by 'ok' on Windows)
  * ``cross``: ❌ (red, replaced by 'ko' on Windows)
  * ``ellipsis``:  … (no color, replaced by '...' on Windows)

  You can create your own colored sequences using :class:`UnicodeSequence`:

.. autoclass:: UnicodeSequence

  ::

      >>> up_arrow = ui.UnicodeSequence(ui.blue, "↑", "+")
      >>> ui.info(up_arrow, "2 commits")
      ↑ 2 commits # on Linux
      + 2 commits # on Windows

  Alternatively, if you do not want to force a color, you can use
  :class:`Symbol`:

.. autoclass:: Symbol

  ::

      >>> heart = ui.Symbol("❤", "<3")
      >>> ui.info("Thanks for using python-cli-ui", heart)
      Thanks for using python-cli-ui ❤  # on Linux
      Thanks for using python-cli-ui <3  # on Windows



Informative messages
++++++++++++++++++++

.. autofunction:: info

   ::

      >>> ui.info("this is", ui.red, "red")
      This is red


Functions below take the same arguments as the :func:`info` function

.. autofunction:: info_section

   ::

      >>> ui.info_section("Section one")
      >>> ui.info("Starting stuff")

      Section one
      ------------

      Starting stuff

.. autofunction:: info_1

   ::

      >>> ui.info_1("Message")
      :: Message

.. autofunction:: info_2

   ::

      >>> ui.info_2("Message")
      => Message

.. autofunction:: info_3

   ::

      >>> ui.info_3("Message")
      * Message

.. autofunction:: debug

    ::

      >>> ui.debug("Message")
      <nothing>


Error messages
++++++++++++++

Functions below use ``sys.stderr`` by default:

.. autofunction:: error

   ::

      >>> ui.error("Message")
      Error: message

.. autofunction:: warning

   ::

      >>> ui.warning("Message")
      Warning: message

.. autofunction:: fatal

   ::

      >>> ui.fatal("Message")
      Error: message
      exit()


Progress messages
+++++++++++++++++

.. autofunction:: dot

   ::

      >>> for in in rang(0, 5):
      >>>     ui.dot()
      ....<no newline>
      >>> ui.dot(last=True)
      .....

.. autofunction:: info_count

   ::

      >>> ui.info_count(4, 12, message)
      * ( 5/12) message

.. autofunction:: info_progress

   ::

      >>> ui.info_progress("Done", 5, 20)
      Done: 25%


Formatting
++++++++++

.. autofunction:: tabs

   ::

    >>> ui.info("one", "\n",
                ui.tabs(1), "two", "\n",
                ui.tabs(2), "three", "\n",
                sep="")
    one
      two
        three

.. autofunction:: indent

   ::

      >>> quote = (
            "First, we take Manhattan\n"
            "Then we take Berlin!"
      )
      >>> ui.info("John said:", ui.indent(quote))
      John said:
         First, we take Manhattan.
         Then we take Berlin!


.. autofunction:: info_table

   ::

      >>> headers=["name", "score"]
      >>> data = [
            [(bold, "John"), (green, 10.0)],
            [(bold, "Jane"), (green, 5.0)],
          ]

      >>> ui.info_table(data, headers=headers)
      name      score
      --------  --------
      John       10.0
      Jane        5.0


Asking for user input
+++++++++++++++++++++

.. autofunction:: read_input
.. autofunction:: ask_string

  ::

      >>> name = ui.ask_string("Enter your name")
      :: Enter your name
      <john>
      >>> name
      'john'

.. autofunction:: ask_choice

  ::

      >>> choices = ["apple", "banana", "orange"]
      >>> fruit = ui.ask_choice("Select a fruit", choices)
      :: Select a fruit
        1 apple
        2 banana
        3 orange
      <2>
      >>> fruit
      'banana'

.. autofunction:: ask_yes_no

   ::

         >>> with_cream = ui.ask_yes_no("With cream?", default=False)
         :: With cream? (y/N)
         <y>
         >>> with_cream
         True

.. autofunction:: read_password
.. autofunction:: ask_password

  ::

      >>> fav_food = ui.ask_password("Guilty pleasure?")
      :: Guilty pleasure?

      >>> fav_food
      'chocolate'

Displaying duration
+++++++++++++++++++


.. autoclass:: Timer

   ::

      >>> @ui.Timer("something")
          def do_something():
               foo()
               bar()
      # Or:
      >>> with ui.Timer("something"):
              foo()
              bar()
      * Something took 0h 3m 10s 430ms


Auto-correct
++++++++++++


.. autofunction:: did_you_mean

   ::

      >>> allowed_names = ["Alice", "John", "Bob"]
      >>> name = ui.ask_string("Enter a name")
      >>> if not name in allowed_names:
      >>>       ui.did_you_mean("Invalid name", user_input, choices)
      :: Enter a name
      <Joohn>
      Invalid name.
      Did you mean: John?

  Note: if the list of possible choices is short, consider using
  :func:`ask_choice` instead.


.. _pytest:

Testing with pytest
++++++++++++++++++++

.. autofunction:: ui.tests.conftest.message_recorder

::

    from ui.tests.conftest import message_recorder


    def foo():
        ui.info("Fooing")


    def test_foo(message_recorder):
         foo()
         assert message_recorder.find("Fooing")


Changelog
----------

v0.7.3
++++++

* Switch to ``dmenv``. This makes it possible to use ``python-cli-ui`` with ``colorama >= 4.0``.

v0.7.2
++++++

* Switch to `poetry <https://poetry.eustace.io>`_ .

v0.7.1
++++++

* Fix crash in ``ask_password`` when password was empty.
* Let the ``KeyboardInterrput`` exception propagate back to the caller instead of catching
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

* Add ``ui.setup`` to configure things like verbosity and when to
  use colored output (#3)

* Add a ``message_recorder`` in ``ui.tests.conf`` that can
  be used as a ``pytest`` fixture in other projects.

v0.1.0
+++++++

First public release.
