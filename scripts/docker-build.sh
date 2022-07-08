#!/bin/bash

set -e

docker build -t app ./app/. --no-cache --network=host 
docker build -t server ./server/. --no-cache --network=host

exit 0