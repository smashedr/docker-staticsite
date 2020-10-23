#!/usr/bin/env bash

set -e

if [ -f /ssl/ssl.crt ]; then
    echo "Using existing cert: /ssl/ssl.crt"
    exit
fi
rm -rf /ssl/ssl.key
if [ ! -d /ssl ];then
    mkdir /ssl
fi

subj="
C=US
ST=Washington
localityName=Seattle
O=cssnr
organizationalUnitName=Hosting
commonName=ssl.cssnr.com
emailAddress=admin@cssnr.com
"

openssl req  -nodes -new -x509 -subj "${subj//$'\n'//}" -keyout "/ssl/ssl.key" -out "/ssl/ssl.crt"
echo "Generated new SSL certs."
ls -lah /ssl
