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


EVENT_TYPE_VIDEO = 'video'
EVENT_TYPE_PROBLEM = 'problem'

EVENT_TYPES = {
    EVENT_TYPE_VIDEO: [
        "play_video",
        "pause_video",
        "seek_video",
        "stop_video",
    ],
    EVENT_TYPE_PROBLEM: [
        "problem_graded",
        "problem_show",
        "problem_check",
        "problem_save",
        "problem_reset",
    ]
}
_USLESS_FIELDS = [
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
    'event.POST',
    'event.GET',
    'context.enterprise_uuid',
    'context.course_id',
    'context.org_id',
]
USLESS_FIELDS = {
    EVENT_TYPE_VIDEO: _USLESS_FIELDS + [],
    EVENT_TYPE_PROBLEM: _USLESS_FIELDS + [
        'context.course_user_tags',
        'context.asides',
        'event.state',
        'event.answers',
        'event.correct_map',
        'event.submission',
    ]
}

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
            self.event_type = EVENT_TYPE_VIDEO
        elif options["events"] == "problem":
            self.event_type = EVENT_TYPE_PROBLEM
        else:
            logger.error("Wrong --events argument")
            exit(1)

        for file_gz in sorted(glob.glob(f"/data/tracking/original-docker/{options['instance']}/*/*.gz")):
            self.clean_file(file_gz)

    def clean_file(self, file_gz: str) -> None:
        # end_time = datetime(2023, 9, 21, 6, 0, 18, 0, tzinfo=timezone.utc)
        errors = 0
        new_f_name = f"{file_gz[:-3]}.cleaned"
        new_f = open(new_f_name, "w")
        with gzip.open(file_gz, "rb") as f_in:
            for line in f_in.readlines():
                line = line.decode('utf-8').strip()
                line = line[line.index('{'):]
                j = json.loads(line)

                if j["event_type"] not in EVENT_TYPES[self.event_type]:
                    continue

                # in case of problem we skip every row with context.path='/event'
                if self.event_type == 'problem':
                    if j['context']['path'] == '/event':
                        continue
                elif self.event_type == 'video':
                    j['event'] = json.loads(j['event'])

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

                # skip rows without org_id, course_id or username
                if course_id == '' or org_id == '' or username == '':
                    continue

                j['course_id'] = course_id
                j['org_id'] = org_id

                t = parse(j['time'])
                j['time'] = t.replace(tzinfo=None).isoformat()

                # skip recordes already in database
                # if t > end_time: continue

                for k in USLESS_FIELDS[self.event_type]:
                    try:
                        if '.' in k:
                            a, b = k.split('.')
                            del j[a][b]
                        else:
                            del j[k]
                    except KeyError:
                        pass

                new_f.write(json.dumps(j) + "\n")

        print(f"{new_f_name=} {errors=}")
