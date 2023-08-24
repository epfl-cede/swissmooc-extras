#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/sync_tracking_logs.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py sync_tracking_logs
