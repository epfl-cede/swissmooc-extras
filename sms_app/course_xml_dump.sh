#!/bin/bash

logger run /data/swissmooc-extras/course_xml_dump.sh
source /data/swissmooc-extras.env >> /dev/null 2>&1
source /data/swissmooc-extras/venv/bin/activate

cd /data/swissmooc-extras/sms_app

python manage.py course_xml_dump
