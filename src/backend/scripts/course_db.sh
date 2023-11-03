#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/course_db.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py course_db_renew_course_table -v 2
python /data/swissmooc-extras/src/backend/manage.py course_db_dump_mongo -v 2
python /data/swissmooc-extras/src/backend/manage.py course_db_dump_mysql -v 2
python /data/swissmooc-extras/src/backend/manage.py course_db_encrypt -v 2
python /data/swissmooc-extras/src/backend/manage.py course_db_upload -v 2
python /data/swissmooc-extras/src/backend/manage.py course_db_clean -v 2
