set -x
set -e

poetry run black --check .
poetry run isort --check .
poetry run mypy cli_ui
poetry run flake8 cli_ui/__init__.py cli_ui/tests/test_cli_ui.py
poetry run sphinx-build -W docs docs/_build/html
