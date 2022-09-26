#!/bin/bash
set -e

S3_BUCKET_NAME="dolist-log-dev"

APP_ID=$(sudo docker ps -qf "name=dolist_app")
SERVER_ID=$(sudo docker ps -qf "name=dolist_server")
WORKER_ID=$(sudo docker ps -qf "name=dolist_worker")
DB_ID=$(sudo docker ps -qf "name=postgres")


CONTAINER_IDS=($APP_ID $SERVER_ID $WORKER_ID $DB_ID)
CONTAINER_NAMES=("app" "server" "worker" "db")
UNIX_TIMESTAMP=$(date +%s)


for i in ${!CONTAINER_IDS[*]}; 
    # https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html
    # Write the log as a file and batch it to S3 via AWS CLI
    do 
        sudo docker logs ${CONTAINER_IDS[i]} > logs_${CONTAINER_NAMES[i]}_${CONTAINER_IDS[i]}_${UNIX_TIMESTAMP}.txt; 
        aws s3 mv ./logs_${CONTAINER_NAMES[i]}_${CONTAINER_IDS[i]}_${UNIX_TIMESTAMP}.txt s3://${S3_BUCKET_NAME}/logs_${CONTAINER_NAMES[i]}_${CONTAINER_IDS[i]}_${UNIX_TIMESTAMP}.txt;
    done

rm logs_*;
exit 0

