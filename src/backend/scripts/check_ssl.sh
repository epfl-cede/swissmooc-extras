#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/check_ssl.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py check_ssl -v 2
