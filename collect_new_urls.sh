#!/bin/bash
cd scrapers
for python_file in *.py; do python $python_file --collect_new_urls; done