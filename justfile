poetry := "python -m poetry"
poetry_run := poetry + " run"

default:
    just --list --unsorted

setup:
    {{ poetry }} install

lint:
    {{ poetry_run }} black --check .
    {{ poetry_run }} isort --check .
    {{ poetry_run }} flake8  .
    {{ poetry_run }} mypy

test:
    {{ poetry_run }} pytest

format:
    {{ poetry_run }} black .
    {{ poetry_run }} isort .


build-doc:
    {{ poetry_run }} sphinx-build -W docs/ docs/_build/html

dev-doc:
    {{poetry_run }} sphinx-autobuild docs/ docs/_build/html

deploy-doc: build-doc
    {{ poetry_run }} ghp-import \
        --no-jekyll \
        --remote github \
        docs/_build/html/
    git push github gh-pages --force --no-verify
