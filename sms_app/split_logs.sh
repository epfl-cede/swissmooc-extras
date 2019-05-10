#!/bin/bash
set -ex

logger run /home/ubuntu/sms-exrtas/sms_app.sh
source /home/ubuntu/sms_app.env
source /home/ubuntu/sms-exrtas/venv/bin/activate

cd /home/ubuntu/sms-exrtas/sms_app

python manage.py split_logs_fetch_new
python manage.py split_logs_split --limit 100
python manage.py split_logs_encrypt --limit 100
python manage.py split_logs_upload
