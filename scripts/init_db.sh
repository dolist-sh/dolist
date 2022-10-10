#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 -host="localhost" --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE dolistdb;
EOSQL