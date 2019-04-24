#!/bin/bash

echo script started at `date`

logger run /home/ubuntu/sms-exrtas/sms_app.sh
source /home/ubuntu/sms-exrtas/sms_app/sms_app.env
source /home/ubuntu/sms-exrtas/venv/bin/activate

cd /home/ubuntu/sms-exrtas/sms_app
python manage.py check_ssl
python manage.py fetch_new
python manage.py split --limit 100
#python manage.py encrypt --limit 100
