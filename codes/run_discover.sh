#!/bin/bash

python3 ./batch_discover.py &
sleep 3000  # 50 minutes
killall -9 python3
killall -9 chromedriver
