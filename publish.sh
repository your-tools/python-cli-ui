#/bin/bash

set -x
set -e

(
  cd docs
  ./publish.sh
)

rm -fr dist/
python setup.py sdist bdist_wheel
twine upload dist/*
