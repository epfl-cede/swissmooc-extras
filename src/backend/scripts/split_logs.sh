#!/bin/bash

logger run /data/swissmooc-extras/src/backend/scripts/split_logs.sh

source /data/swissmooc-extras/venv/bin/activate
python /data/swissmooc-extras/src/backend/manage.py split_logs_fetch_new -v 2

python /data/swissmooc-extras/src/backend/manage.py split_logs_split --limit 200 --org epfl -v 2
python /data/swissmooc-extras/src/backend/manage.py split_logs_split --limit 200 --org ffhs -v 2

python /data/swissmooc-extras/src/backend/manage.py split_logs_encrypt --limit 100 --org epfl -v 2
python /data/swissmooc-extras/src/backend/manage.py split_logs_encrypt --limit 100 --org ffhs -v 2
