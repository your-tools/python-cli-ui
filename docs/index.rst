Python CLI UI
=============

.. toctree::
    :hidden:

    changelog


.. module:: cli_ui

Tools for nice user interfaces in the terminal.

.. contents::

Installation
-------------

``cli-ui`` is available on `Pypi <https://pypi.org/project/cli-ui/>`_
and is compatible with Python **3.4** and higher.

It depends on ``colorama`` and ``unidecode`` for Windows support, and on
``tabulate`` for the :func:`info_table` function.

API
----

Configuration
+++++++++++++

.. autofunction:: setup

::

  >>> cli_ui.debug("this will not be printed")
  <nothing>
  >>> cli_ui.setup(verbose=True)
  >>> cli_ui.debug("this will be printed")
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

      >>> up_arrow = cli_ui.UnicodeSequence(cli_ui.blue, "↑", "+")
      >>> cli_ui.info(up_arrow, "2 commits")
      ↑ 2 commits # on Linux
      + 2 commits # on Windows

  Alternatively, if you do not want to force a color, you can use
  :class:`Symbol`:

.. autoclass:: Symbol

  ::

      >>> heart = cli_ui.Symbol("❤", "<3")
      >>> cli_ui.info("Thanks for using cli-ui", heart)
      Thanks for using cli-ui ❤  # on Linux
      Thanks for using cli-ui <3  # on Windows



Informative messages
++++++++++++++++++++

.. autofunction:: info

   ::

      >>> cli_ui.info("this is", cli_ui.red, "red")
      This is red


Functions below take the same arguments as the :func:`info` function

.. autofunction:: info_section

   ::

      >>> cli_ui.info_section("Section one")
      >>> cli_ui.info("Starting stuff")

      Section one
      ------------

      Starting stuff

.. autofunction:: info_1

   ::

      >>> cli_ui.info_1("Message")
      :: Message

.. autofunction:: info_2

   ::

      >>> cli_ui.info_2("Message")
      => Message

.. autofunction:: info_3

   ::

      >>> cli_ui.info_3("Message")
      * Message

.. autofunction:: debug

    ::

      >>> cli_ui.debug("Message")
      <nothing>


Error messages
++++++++++++++

Functions below use ``sys.stderr`` by default:

.. autofunction:: error

   ::

      >>> cli_ui.error("Message")
      Error: message

.. autofunction:: warning

   ::

      >>> cli_ui.warning("Message")
      Warning: message

.. autofunction:: fatal

   ::

      >>> cli_ui.fatal("Message")
      Error: message
      exit()


Progress messages
+++++++++++++++++

.. autofunction:: dot

   ::

      >>> for in in range(0, 5):
      >>>     cli_ui.dot()
      ....<no newline>
      >>> cli_ui.dot(last=True)
      .....

.. autofunction:: info_count

   ::

      >>> cli_ui.info_count(4, 12, message)
      * ( 5/12) message

.. autofunction:: info_progress

   ::

      >>> cli_ui.info_progress("Done", 5, 20)
      Done: 25%


Formatting
++++++++++

.. autofunction:: tabs

   ::

    >>> cli_ui.info("one", "\n",
                cli_ui.tabs(1), "two", "\n",
                cli_ui.tabs(2), "three", "\n",
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
      >>> cli_ui.info("John said:", cli_ui.indent(quote))
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

      >>> cli_ui.info_table(data, headers=headers)
      name      score
      --------  --------
      John       10.0
      Jane        5.0


Asking for user input
+++++++++++++++++++++

.. autofunction:: read_input
.. autofunction:: ask_string

  ::

      >>> name = cli_ui.ask_string("Enter your name")
      :: Enter your name
      <john>
      >>> name
      'john'

.. autofunction:: ask_choice


  ::

      >>> choices = ["apple", "banana", "orange"]
      >>> fruit = cli_ui.ask_choice("Select a fruit", choices=choices)
      :: Select a fruit
        1 apple
        2 banana
        3 orange
      <2>
      >>> fruit
      'banana'


  .. versionchanged:: 0.10

      Add ``sort`` paramater to disable sorting the list of choices

  .. versionchanged:: 0.8

      ``choices`` is now a named keyword argument

  .. versionchanged:: 0.7

       The :py:exc:`KeyboardInterrupt` exception is no longer caught by this function.


.. autofunction:: ask_yes_no

   ::

         >>> with_cream = cli_ui.ask_yes_no("With cream?", default=False)
         :: With cream? (y/N)
         <y>
         >>> with_cream
         True

.. autofunction:: read_password
.. autofunction:: ask_password

  ::

      >>> fav_food = cli_ui.ask_password("Guilty pleasure?")
      :: Guilty pleasure?
      ****
      >>> fav_food
      'chocolate'

Displaying duration
+++++++++++++++++++


.. autoclass:: Timer

   ::

      >>> @cli_ui.Timer("something")
          def do_something():
               foo()
               bar()
      # Or:
      >>> with cli_ui.Timer("something"):
              foo()
              bar()
      * Something took 0h 3m 10s 430ms


Auto-correct
++++++++++++


.. autofunction:: did_you_mean

   ::

      >>> allowed_names = ["Alice", "John", "Bob"]
      >>> name = cli_ui.ask_string("Enter a name")
      >>> if not name in allowed_names:
      >>>       cli_ui.did_you_mean("Invalid name", user_input, choices)
      :: Enter a name
      <Joohn>
      Invalid name.
      Did you mean: John?

  Note: if the list of possible choices is short, consider using
  :func:`ask_choice` instead.



Testing
+++++++

.. autoclass:: cli_ui.tests.MessageRecorder
   :members:

::

    # Example with pytest

    # in conftest.py
    from cli_ui.tests import MessageRecorder
    import pytest

    @pytest.fixture()
    def message_recorder():
        message_recorder = MessageRecorder()
        message_recorder.start()
        yield message_recorder
        message_recorder.stop()


    # in foo.py
    def foo():
        cli_ui.info("Fooing")


    # in test_foo.py
    def test_foo(message_recorder):
         foo()
         assert message_recorder.find("Fooing")
