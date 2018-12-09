set -x
set -e

which black && black --check .
MYPYPATH=stubs mypy --ignore-missing-imports --strict cli_ui
pyflakes cli_ui/__init__.py cli_ui/tests/test_cli_ui.py
pytest
sphinx-build -W docs docs/_build/html
