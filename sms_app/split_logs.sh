#!/bin/bash

logger run /data/sms-extras/sms_app.sh
source /data/sms_app.env >> /dev/null 2>&1
source /data/sms-extras/venv/bin/activate

cd /data/sms-extras/sms_app

python manage.py split_logs_fetch_new
python manage.py split_logs_split --platform new --limit 100
python manage.py split_logs_encrypt --platform new --limit 100
python manage.py split_logs_upload --platform new --limit 100
