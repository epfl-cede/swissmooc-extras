#!/bin/bash

logger run /home/ubuntu/sms-extras/sms_app.sh
source /home/ubuntu/sms_app.env >> /dev/null 2>&1
source /home/ubuntu/sms-extras/venv/bin/activate

cd /home/ubuntu/sms-extras/sms_app

python manage.py course_xml_dump
