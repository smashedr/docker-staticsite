#!/usr/bin/env bash

set -e

bash gen-cert.sh

python3 configure.py

nginx -g "daemon off;"
