#!/bin/bash

set -e

GIT_ACCESS_TOKEN=$1 

docker-compose build --build-arg GIT_ACCESS_TOKEN="${GIT_ACCESS_TOKEN}" --no-cache

exit 0