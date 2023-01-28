#!/usr/bin/env bash

PYTHONVERSION=`cat .python-version | grep -E -o "^[^/]+"`
VIRTUALENV=`cat .python-version`
pyenv virtualenv ${PYTHONVERSION} ${VIRTUALENV}
pyenv version
