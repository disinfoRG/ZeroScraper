#!/bin/bash
cd scrapers
for python_file in *.py; do python $python_file --update_contents; done