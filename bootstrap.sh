#!/bin/sh

PROJECT_DIR="$(cd "$(dirname $0)"; pwd)"
ENV_DIR="$PROJECT_DIR/env"

[ -d "$ENV_DIR" ] || virtualenv "$ENV_DIR"

"$ENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"
