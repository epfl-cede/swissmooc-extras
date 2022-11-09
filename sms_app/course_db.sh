#!/bin/bash

logger run /data/sms-extras/sms_app.sh
source /data/sms_app.env >> /dev/null 2>&1
source /data/sms-extras/venv/bin/activate

cd /data/sms-extras/sms_app

python manage.py course_db_renew_course_table
python manage.py course_db_dump_mongo
python manage.py course_db_dump_mysql
python manage.py course_db_encrypt
python manage.py course_db_upload
