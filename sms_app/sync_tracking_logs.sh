#!/bin/bash

logger run /data/sms-extras/sms_app.sh
source /data/sms-extras.env >> /dev/null 2>&1
source /data/sms-extras/venv/bin/activate

cd /data/sms-extras/sms_app

python manage.py sync_tracking_logs
