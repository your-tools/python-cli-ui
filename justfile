default:
    just --list --unsorted

setup:
    python -m poetry install

lint:
    python -m poetry run black --check .
    python -m poetry run isort --check .
    python -m poetry run flake8  .
    python -m poetry run mypy

test:
    python -m poetry run pytest

format:
    python - m poetry run black .
    python - m poetry run isort .


build-doc:
    cd docs ; python -m poetry run sphinx-build -W . _build/html

dev-doc:
    cd docs ; python -m poetry run sphinx-autobuild . _build/html

deploy-doc: build-doc
    ghp-import --push --force --no-jekyll docs/_build/html/

