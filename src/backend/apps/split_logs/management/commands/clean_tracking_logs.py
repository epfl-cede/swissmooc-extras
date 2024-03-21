# -*- coding: utf-8 -*-
import glob
import gzip
import json
import logging
from datetime import datetime
from datetime import timezone

from apps.split_logs.sms_command import SMSCommand  # type: ignore
from dateutil.parser import parse

logger = logging.getLogger(__name__)


EVENT_TYPES_VIDEO = [
    "play_video",
    "pause_video",
    "seek_video",
    "stop_video",
]
EVENT_TYPES_PROBLEM = [
    "problem_graded",
    "problem_show",
    "problem_check",
    "problem_save",
    "problem_reset",
]
USLESS_FIELDS = [
    "GET",
    "POST",
    'source',
    'container_id',
    'container_name',
    'swarm_node',
    'service_type',
    'service_name',
    'instance_type',
    'ip',
    'filename',
    'request_id',
    'session',
    'agent',
    'host',
    'referer',
    'accept_language',
]


class Command(SMSCommand):
    help = "Feed ClickHouse database with tracking log files"
    "This command clean the logs and prepare it for inserting"
    "to Clickhouse"

    # command to inset data
    # cat /data/tracking/original-docker/epfl/campus-zh-swarm-node-21{6,7}/tracking.log-2023*.cleaned | \
    # clickhouse-client -h zh-campus-clickhouse -d insights --query="INSERT INTO epfl_tracking FORMAT JSONEachRow"

    def add_arguments(self, parser) -> None:
        parser.add_argument('--instance', type=str, default="epfl")
        parser.add_argument('--events', type=str, default="video")

    def handle(self, *args, **options):
        self.setOptions(**options)

        logger.info(f"{options['instance']=}")

        if options["events"] == "video":
            event_types = EVENT_TYPES_VIDEO
        elif options["events"] == "problem":
            event_types = EVENT_TYPES_PROBLEM
        else:
            logger.error("Wrong --events argument")
            exit(1)

        for file_gz in sorted(glob.glob(f"/data/tracking/original-docker/{options['instance']}/*/*.gz")):
            self.clean_file(file_gz, event_types)

    def clean_file(self, file_gz: str, event_types: list) -> None:
        # end_time = datetime(2023, 9, 21, 6, 0, 18, 0, tzinfo=timezone.utc)
        errors = 0
        new_f_name = f"{file_gz[:-3]}.cleaned"
        new_f = open(new_f_name, "w")
        with gzip.open(file_gz, "rb") as f_in:
            for line in f_in.readlines():
                line = line.decode('utf-8').strip()
                line = line[line.index('{'):]
                j = json.loads(line)

                if j["event_type"] not in event_types:
                    continue

                try:
                    course_id = j['context']['course_id']
                    del j['context']['course_id']
                    org_id = j['context']['org_id']
                    del j['context']['org_id']
                    username = j['username']
                except KeyError:
                    course_id = ''
                    org_id = ''
                    username = ''

                # parse event string
                j['event'] = json.loads(j['event'])

                # skip rows without org_id, course_id or username
                if course_id == '' or org_id == '' or username == '':
                    continue

                j['course_id'] = course_id
                j['org_id'] = org_id

                t = parse(j['time'])
                j['time'] = t.replace(tzinfo=None).isoformat()

                # skip recordes already in database
                # if t > end_time: continue

                for k in USLESS_FIELDS:
                    try:
                        del j[k]
                    except KeyError:
                        pass

                new_f.write(json.dumps(j) + "\n")

        print(f"{new_f_name=} {errors=}")
