set -x
set -e

pyflakes ui/__init__.py ui/tests/test_ui.py
pytest
sphinx-build -W docs docs/_build/html
