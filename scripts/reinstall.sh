#!/usr/bin/env bash
set -e

pyenv  virtualenvs-delete `cat .python-version`
scripts/setup_pyenv.sh
scripts/install.sh
