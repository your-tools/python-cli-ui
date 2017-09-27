Usage
=====

.. module:: ui

Requirements
-------------

``python-cli-ui`` is available on `Pypi <https://pypi.org/project/python-cli-ui/>`_
and is compatible with Python **3.3** and higher.

It depends on ``colorama`` and ``unidecode`` for Windows support, and on
``tabulate`` for the :func:`info_table` function.

API
----

Configuration
+++++++++++++

.. autofunction:: setup


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

* Sequence of Unicode characters:

  * ``check``: ✓ (green, replaced by 'ok' on Windows)
  * ``cross``: ❌ (red, replaced by 'ko' on Windows)
  * ``ellipsis``:  … (no color, replaced by '...' on Windows)

  You can create your own sequences using :class:`UnicodeSequence`:

.. autoclass:: UnicodeSequence

  ::

      >>> up_arrow = ui.UnicodeSequence(ui.blue, "↑", "+")
      >>> ui.info(up_arrow, "2 commits")
      ↑ 2 commits # on Linux
      + 2 commits # on Windows



Informative messages
++++++++++++++++++++

.. autofunction:: info

   ::

      >>> ui.info("this is", ui.red, "red")


Functions below take the same arguments as the :func:`info` function

.. autofunction:: info_section

   ::

      >>> ui.info_section("Section one")
      >>> ui.info("Starting stuff")

      Section one
      ------------

      Starting stuff

.. autofunction:: info_1
.. autofunction:: info_2
.. autofunction:: info_3


.. autofunction:: debug


Error messages
++++++++++++++

Functions below use ``sys.stderr`` by default:

.. autofunction:: error
.. autofunction:: warning
.. autofunction:: fatal

Progress messages
+++++++++++++++++

.. autofunction:: dot

.. autofunction:: info_count

   ::

      >>> ui.info_count(4, 12)
      * ( 5/12)

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

      >>> ui.info("John said:")
      >>> ui.info(ui.indent("First, we take Manhattan.\nThen we take Berlin!")

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
.. autofunction:: ask_choice
.. autofunction:: ask_yes_no

   ::

         >>> ui.ask_yes_no("With cream?", default=False)
         :: With cream? (y/N)


Misc
++++


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



.. autofunction:: did_you_mean

   ::

      >>> user_input = "Joohn"
      >>> names = ["Alice", "John", "Bob"]
      >>> ui.did_you_mean("Invalid name: %s" % user_input, user_input, choices)
      Invalid name: Joohn
      Did you mean: John?


.. _pytest:

Testing with pytest
-------------------

.. autofunction:: ui.tests.conftest.message_recorder

::

    from ui.tests.conftest import message_recorder


    def foo():
        ui.info("Fooing")


    def test_foo(message_recorder):
         foo()
         assert message_recorder.find("Fooing")
