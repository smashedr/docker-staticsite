#!/usr/bin/env sh

set -ex

python3 pyconf.py

nginx -g "daemon off;"
