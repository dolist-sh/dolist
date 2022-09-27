#!/bin/bash
set -e

S3_BUCKET_NAME=$1 

PROXY_ID=$(sudo docker ps -qf "name=nginx")
APP_ID=$(sudo docker ps -qf "name=dolist_app")
SERVER_ID=$(sudo docker ps -qf "name=dolist_server")
WORKER_ID=$(sudo docker ps -qf "name=dolist_worker")
DB_ID=$(sudo docker ps -qf "name=postgres")


CONTAINER_IDS=($PROXY_ID $APP_ID $SERVER_ID $WORKER_ID $DB_ID)
CONTAINER_NAMES=("proxy" "app" "server" "worker" "db")
UNIX_TIMESTAMP=$(date +%s)


for i in ${!CONTAINER_IDS[*]}; 
    # https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html
    do 
        sudo docker logs ${CONTAINER_IDS[i]} > logs_${CONTAINER_NAMES[i]}_${CONTAINER_IDS[i]}_${UNIX_TIMESTAMP}.txt; 
        aws s3 mv ./logs_${CONTAINER_NAMES[i]}_${CONTAINER_IDS[i]}_${UNIX_TIMESTAMP}.txt s3://${S3_BUCKET_NAME}/logs_${CONTAINER_NAMES[i]}_${CONTAINER_IDS[i]}_${UNIX_TIMESTAMP}.txt;
    done
exit 0

