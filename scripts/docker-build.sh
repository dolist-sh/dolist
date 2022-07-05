!#bin/bash

docker build -t app ./app/. --network=host  # Use host network to prevent issue when running in VPN
docker build -t server ./server/. --network=host