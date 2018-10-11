set -x
set -e

poetry run pyflakes ui/__init__.py ui/tests/test_ui.py
poetry run pytest
poetry run sphinx-build -W docs docs/_build/html
