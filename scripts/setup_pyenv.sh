#!/usr/bin/env bash

PYTHONVERSION=`cat .python-version | grep -E -o "^[^/]+"`
VIRTUALENVSHORT=`cat .python-version | grep -E -o "[^/]+$"`
VIRTUALENVFULL=`cat .python-version`
PYENV_VERSION=${PYTHONVERSION}
pyenv virtualenv-delete -f ${VIRTUALENVSHORT}
pyenv virtualenv ${PYTHONVERSION} ${VIRTUALENVFULL}
unset PYENV_VERSION
pyenv version
