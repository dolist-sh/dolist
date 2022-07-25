#!/bin/bash

set -e

GIT_ACCESS_TOKEN=$1 

docker build -t app ./app/. --no-cache --network=host 
docker build --build-arg GIT_ACCESS_TOKEN="${GIT_ACCESS_TOKEN}" -t server ./server/. --no-cache --network=host

exit 0