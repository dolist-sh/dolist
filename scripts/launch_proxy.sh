#!/bin/bash

set -e

cp $1 /etc/nginx/nginx.conf

systemctl reload nginx