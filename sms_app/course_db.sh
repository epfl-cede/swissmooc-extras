#!/bin/bash

logger run /data/swissmooc-extras/course_db.sh
source /data/swissmooc-extras.env >> /dev/null 2>&1
source /data/swissmooc-extras/venv/bin/activate

cd /data/swissmooc-extras/sms_app

python manage.py course_db_renew_course_table
python manage.py course_db_dump_mongo
python manage.py course_db_dump_mysql
python manage.py course_db_encrypt
python manage.py course_db_upload
