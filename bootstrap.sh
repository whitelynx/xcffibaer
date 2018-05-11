#!/bin/sh

PROJECT_DIR="$(cd "$(dirname "$0")"; pwd)"
ENV_DIR="$PROJECT_DIR/venv"

[ -d "$ENV_DIR" ] || virtualenv "$ENV_DIR"

"$ENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"
"$ENV_DIR/bin/pip" install cairocffi[xcb] -U --force-reinstall --no-binary cairocffi
