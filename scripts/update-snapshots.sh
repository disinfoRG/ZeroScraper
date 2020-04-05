#!/bin/bash
DATE=${1:-"yesterday"}
NS_DUMP=./ns-dump.py
YESTERDAY=$(date --date=$DATE '+%Y-%m-%d')
SNAPSHOT_TABLE=ArticleSnapshot
OUTPUT_FILE="${SNAPSHOT_TABLE}$(echo ${YESTERDAY} | sed -e 's/\-//g').jsonl.bz2"
OUTPUT="/tmp/${OUTPUT_FILE}"
S3_DESTINATION="s3://0archive/user_tainan-sun-500796/${OUTPUT_FILE}"

python3 ${NS_DUMP} -t ${SNAPSHOT_TABLE} -r 1d:${YESTERDAY} | bzip2 -9 > ${OUTPUT} && s3cmd put --acl-public ${OUTPUT} ${S3_DESTINATION} && rm -f ${OUTPUT}
