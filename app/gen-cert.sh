#!/usr/bin/env bash

set -e

if [ -f /ssl/ssl.crt ] && [ -f /ssl/ssl.key ]; then
    echo "Using existing certs:"
    ls -lah /ssl
    exit
fi

rm -rf /ssl/ssl.*
[[ ! -d /ssl ]] && mkdir -p /ssl

subj="
C=US
ST=Washington
localityName=Seattle
O=cssnr
organizationalUnitName=Hosting
commonName=ssl.cssnr.com
emailAddress=ssl@cssnr.com
"

openssl req -nodes -new -x509 -subj "${subj//$'\n'//}" -keyout "/ssl/ssl.key" -out "/ssl/ssl.crt"
echo "Generated new SSL certs:"
ls -lah /ssl
