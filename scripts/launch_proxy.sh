#!/bin/bash

cp $1 /etc/nginx/nginx.conf

systemctl reload nginx