#!/bin/bash
set -e

S3_BUCKET_NAME=$1 

PROXY_ID=$(sudo docker ps -qf "name=dolist_proxy")
APP_ID=$(sudo docker ps -qf "name=dolist_app")
SERVER_ID=$(sudo docker ps -qf "name=dolist_server")
WORKER_ID=$(sudo docker ps -qf "name=dolist_worker")
DB_ID=$(sudo docker ps -qf "name=dolist_postgres")

CONTAINER_IDS=($PROXY_ID $APP_ID $SERVER_ID $WORKER_ID $DB_ID)
CONTAINER_NAMES=("proxy" "app" "server" "worker" "db")

mv_logs () {
    # $1: container id, $2: container name
    UNIX_TIMESTAMP=$(date +%s)
    FILE_NAME=logs_$2_$1_$UNIX_TIMESTAMP.txt
    sudo docker logs $1 > $FILE_NAME;

    # https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/mv.html
    aws s3 mv ./$FILE_NAME s3://${S3_BUCKET_NAME}/$FILE_NAME;
}

for i in ${!CONTAINER_IDS[*]}; 
    do 
        mv_logs ${CONTAINER_IDS[i]} ${CONTAINER_NAMES[i]}
    done
    
exit 0




