Changelog
==========

v0.5.0
------

* Export a ``Symbol`` class, to use when you do not want to force
  color as  with ``UnicodeSequence``

v0.4.0
------

* Expose the previously private ``UnicodeSequence`` class.

v0.3.0
------

* Add ``info_section``

* Cosmetic changes about prefixes for ``debug``, ``warn`` and ``error``
  messages. (See `#6 <https://github.com/TankerApp/python-cli-ui/pull/6>`_
  for the details)


v0.2.0
------

* Add ``ui.setup`` to configure things like verbosity and when to
  use colored output (#3)

* Add a ``message_recorder`` in ``ui.tests.conf`` that can
  be used as a ``pytest`` fixture in other projects.

v0.1.0
-------

First public release.
