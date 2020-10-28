#!/usr/bin/env bash

set -e

bash gen-cert.sh
python3 configure.py

[[ -z "${HTML_ROOT}" ]] && HTML_ROOT="/data"
chmod -R g+w "${HTML_ROOT}"
chmod g+s "${HTML_ROOT}"

nginx -g "daemon off;"
