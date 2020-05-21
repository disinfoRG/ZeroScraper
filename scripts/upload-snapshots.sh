#!/bin/bash
DATE=${1:-"yesterday"}
NS_DUMP=./zs-dump.py
YESTERDAY=$(date --date=$DATE '+%Y-%m-%d')
BATCH_SIZE=100
SNAPSHOT_TABLE=${2:-"ArticleSnapshot"}
OUTPUT_FILE="ArticleSnapshot$(echo ${YESTERDAY} | sed -e 's/\-//g').jsonl.bz2"
S3_DESTINATION="${S3_DESTINATION_DIR}/${OUTPUT_FILE}"

python3 ${NS_DUMP} -t ${SNAPSHOT_TABLE} -r 1d:${YESTERDAY} --batch-size ${BATCH_SIZE} | bzip2 -9 > ${OUTPUT_FILE}
s3cmd put --acl-public ${OUTPUT_FILE} ${S3_DESTINATION}
rm ${OUTPUT_FILE}
