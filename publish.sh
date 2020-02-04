#/bin/bash

set -x
set -e

# Build and upload doc
poetry run sphinx-build -W docs docs/_build/html/
poetry run ghp-import \
        --push \
        --force \
        --no-jekyll \
        docs/_build/html/ \

# Build and upload source and wheel on pypi.org
rm -fr dist/
poetry build
poetry publish
