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

* Unicode characters:

  * ``check``: ✓
  * ``cross``: ❌
  * ``ellipsis``:  …

Informative messages
++++++++++++++++++++

.. autofunction:: info

   ::

      ui.info("this is", ui.red, "red")


Functions below take the same arguments as the :func:`info` function

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

      >>> info_count(4, 12)
      * ( 5/12)

.. autofunction:: info_progress

   ::

      >>> info_progress("Done", 5, 20)
      Done: 25%


Formatting
++++++++++

.. autofunction:: tabs

   ::

    ui.info("one", "\n",
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

      headers=["name", "score"]
      data = [
         [(bold, "John"), (green, 10.0)],
         [(bold, "Jane"), (green, 5.0)],
      ]

      >>> info_table(data, headers=headers)
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

         >>> ask_yes_no("With cream?", default=False)
         :: With cream? (y/N)


Misc
++++

.. autoclass:: Timer

   ::

      >>> @Timer("something")
          def do_something():
               foo()
               bar()
      # Or:
      >>> with Timer("something"):
              foo()
              bar()



.. autofunction:: did_you_mean

   ::

      input = "Joohn"
      names = ["Alice", "John", "Bob"]
      >>> did_you_mean("Invalid name: %s" % input, input, choices)
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
