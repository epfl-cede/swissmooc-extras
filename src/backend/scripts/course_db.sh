#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/course_db.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py course_db_renew_course_table
python /data/swissmooc-extras/src/backend/manage.py course_db_dump_mongo
python /data/swissmooc-extras/src/backend/manage.py course_db_dump_mysql
python /data/swissmooc-extras/src/backend/manage.py course_db_encrypt
python /data/swissmooc-extras/src/backend/manage.py course_db_upload
