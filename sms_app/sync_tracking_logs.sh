#!/bin/bash

logger run /data/swissmooc-extras/sync_tracking.logs.sh
source /data/swissmooc-extras.env >> /dev/null 2>&1
source /data/swissmooc-extras/venv/bin/activate

cd /data/swissmooc-extras/sms_app

python manage.py sync_tracking_logs
