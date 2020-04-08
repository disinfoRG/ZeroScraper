#!/bin/bash

DB_USER=$(echo $DB_URL | sed -n 's/^mysql.*\/\/\([^:]*\):.*$/\1/p')
DB_PASS=$(echo $DB_URL | sed -n 's/^.*:\([^@]*\)@.*$/\1/p')
DB_HOST=$(echo $DB_URL | sed -n 's/^.*@\([^\/]*\)\/.*$/\1/p')
DB_NAME=$(echo $DB_URL | sed -n 's/^.*\/\([^\/]*\)$/\1/p')

NOW=$(date '+%Y%m%dT%H%M%S')

MYSQL_PWD=${DB_PASS} mysqldump -d -u ${DB_USER} -h ${DB_HOST} --single-transaction --quick --lock-tables=false ${DB_NAME} | bzip2 -9 | s3cmd put --acl-public - "${S3_DESTINATION_DIR}/schema${NOW}.sql.bz2"
MYSQL_PWD=${DB_PASS} mysqldump -t -u ${DB_USER} -h ${DB_HOST} --single-transaction --quick --lock-tables=false ${DB_NAME} alembic_version Article Site | bzip2 -9 | s3cmd put --acl-public - "${S3_DESTINATION_DIR}/data${NOW}.sql.bz2"
