#!/bin/sh

PROJECT_DIR="$(cd "$(dirname "$0")"; pwd)"
VENV_NAME="$(cat .python-version)"
PYTHON_VER="3.7.4"

cd "$PROJECT_DIR"

if ! pyenv version; then
	if ! pyenv versions 2>/dev/null | grep $PYTHON_VER; then
		pyenv install $PYTHON_VER
	fi
	pyenv virtualenv $PYTHON_VER $VENV_NAME
fi

pyenv exec pip install -r "$PROJECT_DIR/requirements.txt"
pyenv exec pip install cairocffi[xcb] -U --force-reinstall --no-binary cairocffi

pyenv exec python xcffibaer_lib/ffi_build.py
