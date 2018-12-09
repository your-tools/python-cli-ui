set -x
set -e

black --check .
pyflakes cli_ui/__init__.py cli_ui/tests/test_cli_ui.py
pytest
sphinx-build -W docs docs/_build/html