#!/bin/bash
SLEEP_SEC=${1:-"3000"}

python3 ./batch_discover.py &
sleep ${SLEEP_SEC}    # 50 minutes
killall -9 python3
killall -9 chromedriver
