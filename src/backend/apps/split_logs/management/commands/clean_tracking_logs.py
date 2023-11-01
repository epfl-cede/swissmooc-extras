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


class Command(SMSCommand):
    help = "Feed ClickHouse database with tracking log files"
    "This command clean the logs and prepare it for inserting"
    "to Clickhouse"

    # command to inset data
    # cat /data/tracking/original-docker/epfl/campus-zh-swarm-node-21{6,7}/tracking.log-2023*.cleaned | \
    # clickhouse-client -h zh-campus-clickhouse -d insights --query="INSERT INTO epfl_tracking FORMAT JSONEachRow"

    def add_arguments(self, parser) -> None:
        parser.add_argument('--instance', type=str, default="epfl")

    def handle(self, *args, **options):
        self.setOptions(**options)

        logger.info(f"{options['instance']=}")

        for file_gz in sorted(glob.glob(f"/data/tracking/original-docker/{options['instance']}/*/*.gz")):
            self.clean_file(file_gz)

    def clean_file(self, file_gz: str) -> None:
        end_time = datetime(2023, 9, 21, 6, 0, 18, 0, tzinfo=timezone.utc)
        errors = 0
        new_f_name = f"{file_gz[:-3]}.cleaned"
        new_f = open(new_f_name, "w")
        with gzip.open(file_gz, "rb") as f_in:
            for line in f_in.readlines():
                line = line.decode('utf-8').strip()
                line = line[line.index('{'):]
                j = json.loads(line)
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

                # skip garbage course_id field, usually comes with garbage queries from home-made hackers
                try:
                    course_id.index('course-v1:')
                except ValueError:
                    continue

                j['course_id'] = course_id
                j['org_id'] = org_id

                t = parse(j['time'])
                j['time'] = t.replace(tzinfo=None).isoformat()

                # skip recordes already in database
                if t > end_time: continue

                if 'event' in j:
                    if type(j['event']) is list:
                        j['event_array'] = j['event']
                    if type(j['event']) is str:
                        if j['event'][0] == '{':
                            try:
                                event_hash = json.loads(j['event'])
                                if 'POST' in event_hash:
                                    del event_hash['POST']
                                if 'GET' in event_hash:
                                    del event_hash['GET']
                                j['event_hash'] = event_hash
                            except json.decoder.JSONDecodeError:
                                errors += 1
                        else:
                            j['event_string'] = j['event']

                    del j['event']
                    # delete all other usless keys
                    for k in [
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
                    ]:
                        try:
                            del j[k]
                        except KeyError:
                            pass

                new_f.write(json.dumps(j) + "\n")

        print(f"{new_f_name=} {errors=}")
