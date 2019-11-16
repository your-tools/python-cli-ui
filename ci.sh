set -x
set -e

which black && black --check .
mypy cli_ui
pyflakes cli_ui/__init__.py cli_ui/tests/test_cli_ui.py
pytest --cov . --cov-report term
sphinx-build -W docs docs/_build/html
