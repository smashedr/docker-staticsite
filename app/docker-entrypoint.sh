#!/usr/bin/env bash

set -e

bash gen-cert.sh

python3 pyconf.py

nginx -g "daemon off;"
