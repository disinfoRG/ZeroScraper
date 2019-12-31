#!/bin/bash

python3 ./batch_discover.py &
sleep 3480  # 58 minutes
killall python3
killall chromedriver
