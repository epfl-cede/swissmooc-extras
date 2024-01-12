#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/course_xml_dump.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py course_db_renew_course_table -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org epfl -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org ethz -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org ffhs -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org implicit_bias -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org sms -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org tdr -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org unige -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org unili -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org usi -v 2
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump --org zhaw -v 2
