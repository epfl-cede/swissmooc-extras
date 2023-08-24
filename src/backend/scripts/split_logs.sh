#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/split_logs.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py split_logs_fetch_new
python /data/swissmooc-extras/src/backend/manage.py split_logs_split --platform new --limit 100
python /data/swissmooc-extras/src/backend/manage.py split_logs_encrypt --platform new --limit 100
python /data/swissmooc-extras/src/backend/manage.py split_logs_upload --platform new --limit 100
