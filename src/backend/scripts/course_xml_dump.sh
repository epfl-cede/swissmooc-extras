#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/course_xml_dump.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py course_xml_dump
