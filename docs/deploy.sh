#!/bin/bash

set -ex

./build.sh
ghp-import _build/html/ -p -n -m "ghp-import automatic commit"
