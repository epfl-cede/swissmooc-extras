import re
import os
import logging
import json
from datetime import datetime

import boto3, botocore

from django.db import connections
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from migrate.models_hawthorn import (
    AuthUser,
    AuthUserProfile,
    AuthRegistration,
    StudentUserattribute,
    UserApiUserpreference,
)
from migrate.helpers import insertOrUpdateRow, selectRows, selectRowsIn, selectField, selectFieldIn, copyTable, cmd
from migrate.migrateUser import MigrateUser

logger = logging.getLogger(__name__)

CONNECTION_SOURCE = 'edxapp_readonly'
CONNECTION_ID = 'edxapp_id'
CONNECTION_DESTINATION = 'edxapp_university'

S3_SOURCE_BUCKET = 'staging-usercontent'
S3_SOURCE_PREFIX = 'submissions_attachments'
S3_DESTINATION_BUCKET = 'file-upload-university'
S3_DESTINATION_PREFIX = 'submissions-attachments'


class migrateCourseException(BaseException):
    pass

class MigrateCourse:
    def __init__(self, destination, course_id, overwrite, debug):
        self.destination = destination
        self.course_id = course_id
        self.overwrite = overwrite
        self.debug = debug
        self.course_map = {
            'edxapp_university': {
                'CSM': 'EPFL',
            }
        }

        self.user_id_map = {}
        self.anonymous_user_id_map = {}
        self.course_id_map = {
            self.course_id: self.course_id_substitute()
        }
        self.export_dir = '/tmp/course_export'
        self.import_dir = '/home/ubuntu/stacks/openedx-university/logs/course_export'
        self.import_dir_docker = '/openedx/data/logs/course_export'

    def run(self):
        users =  self.selectRows('student_courseenrollment', {'course_id': self.course_id})
        if not users:
            logger.info("There isn't users in the course with id={}, are you sure you want to migrate this course?".format(self.course_id))
            exit(0)

        try:
            self.migrateUsers(users)
            #self.migrateCourse()
            self.migrateCourseActivityStudent() # fillup anonymous_id_map
            #self.migrateCourseActivityCourseware()
            #self.migrateCourseActivityAssessment()
            #self.migrateCourseActivityWorkflow()
            #self.migrateCourseActivitySubmission()
            self.migrateCourseActivitySubmissionFiles()
        except Exception as e:
            logger.error(e)
            raise e

    def migrateUsers(self, users):
        for user in users:
            Migrate = MigrateUser(self.destination, user['user_id'], self.overwrite, self.debug)
            Migrate.run()
            self.user_id_map[user['user_id']] = Migrate.pk

    def migrateCourse(self):
        # do not migrate the course if not overwrite
        if not self.overwrite and self.courseExists(): return True
        self.exportCourse()
        self.importCourse()
        

    def migrateCourseActivityStudent(self):
        # enroll
        self.copyData(
            'student_courseenrollment',
            {'course_id': self.course_id},
            ['id', 'course_id', 'created', 'is_active', 'mode', 'user_id'],
            ['id', 'course_id', 'user_id']
        )

        #self.copyData(
        #    'student_anonymoususerid',
        #    {'course_id': self.course_id},
        #    ['id', 'anonymous_user_id', 'course_id', 'user_id'],
        #    ['id', 'anonymous_user_id']
        #)
        # anonymous_user_id will be changed due to the fact that
        # SECRET_KEY was changed, so we have to generate new one,
        # remove old one and replace every entry in each tables using
        # it
        student_anonymoususerid_rows = self.selectRows(
            'student_anonymoususerid',
            {'course_id': self.course_id},
        )
        for student_anonymoususerid_row in student_anonymoususerid_rows:
            # this will create new row = no need to copy
            anonymous_user_id = self.generate_anonymous_user_id(student_anonymoususerid_row['user_id'])
            self.anonymous_user_id_map[student_anonymoususerid_row['anonymous_user_id']] = anonymous_user_id

        for user_id in self.user_id_map:
            self.copyData(
                'experiments_experimentdata',
                {'user_id': user_id},
                ['id', 'created', 'modified', 'experiment_id', 'key', 'value', 'user_id'],
                ['id', 'user_id', 'experiment_id', 'key']
            )

    def migrateCourseActivityCourseware(self):
        # courseware_studentmodule
        courseware_studentmodule_ids = self.copyData(
            'courseware_studentmodule',
            {'course_id': self.course_id},
            ['id', 'module_type', 'module_id', 'course_id', 'state', 'grade', 'max_grade', 'done', 'created', 'modified', 'student_id'],
            ['id', 'student_id', 'module_id', 'course_id']
        )
        # courseware_studentmodulehistory
        self.copyDataIn(
            'courseware_studentmodulehistory',
            'student_module_id',
            courseware_studentmodule_ids,
            ['id', 'version', 'created', 'state', 'grade', 'max_grade', 'student_module_id'],
            ['id', 'student_module_id']
        )


    def migrateCourseActivitySubmission(self):
        # submissions_studentitem
        submissions_studentitem_ids = self.copyData(
            'submissions_studentitem',
            {'course_id': self.course_id},
            ['id', 'student_id', 'course_id', 'item_id', 'item_type'],
            ['id']
        )

        # submissions_submission
        submissions_submission_ids = self.copyDataIn(
            'submissions_submission',
            'student_item_id',
            submissions_studentitem_ids,
            ['id', 'uuid', 'attempt_number', 'submitted_at', 'created_at', 'raw_answer', 'student_item_id', 'status'],
            ['id']
        )

        # submissions_score
        submissions_score_ids_1 = self.copyDataIn(
            'submissions_score',
            'student_item_id',
            submissions_studentitem_ids,
            ['id', 'points_earned', 'points_possible', 'created_at', 'reset', 'student_item_id', 'submission_id'],
            ['id']
        )
        submissions_score_ids_2 = self.copyDataIn(
            'submissions_score',
            'submission_id',
            submissions_submission_ids,
            ['id', 'points_earned', 'points_possible', 'created_at', 'reset', 'student_item_id', 'submission_id'],
            ['id']
        )

        # submissions_scoresummary
        self.copyDataIn(
            'submissions_scoresummary',
            'id',
            set(submissions_score_ids_1 + submissions_score_ids_2),
            ['id', 'highest_id', 'latest_id', 'student_item_id'],
            ['id']
        )

    def migrateCourseActivitySubmissionFiles(self):
        submissions_studentitem_rows = self.selectRows(
            'submissions_studentitem',
            {'course_id': self.course_id}
        )

        submissions_submission_rows = self.selectRowsIn(
            'submissions_submission',
            'student_item_id',
            [row['id'] for row in submissions_studentitem_rows]
        )
        for submissions_submission_row in submissions_submission_rows:
            raw_answer = json.loads(submissions_submission_row['raw_answer'])
            if 'file_keys' in raw_answer:
                for file_key in raw_answer['file_keys']:
                    self.copyFile(file_key)

    def copyFile(self, file_key):
        # "c40305676d6663094c191ef03c083c28/course-v1:CSM+01+2020/block-v1:CSM+01+2020+type@openassessment+block@80273176cb9b4dca9fe5ac0d52d53568"
        # first hash is the anonymous_user_id, we have to replace it
        s3 = boto3.resource('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
        source_key = "{}/{}".format(S3_SOURCE_PREFIX, file_key)
        anonymous_id = file_key.split('/')[0]
        destination_key = "{}/{}".format(
            S3_DESTINATION_PREFIX,
            file_key.replace(anonymous_id, self.anonymous_user_id_map[anonymous_id])
        )
        copy_source = {
            'Bucket': S3_SOURCE_BUCKET,
            'Key': source_key
        }
        try:
            logger.info(
                "Copy file %s: %s to %s: %s",
                S3_SOURCE_BUCKET,
                source_key,
                S3_DESTINATION_BUCKET,
                destination_key
            )
            s3.meta.client.copy(copy_source, S3_DESTINATION_BUCKET, destination_key)
        except botocore.exceptions.ClientError as e:
            logger.error("Boto3 client error: %s", e)
        
    def migrateCourseActivityWorkflow(self):
        # workflow_assessmentworkflow
        workflow_assessmentworkflow_ids = self.copyData(
            'workflow_assessmentworkflow',
            {'course_id': self.course_id},
            ['id', 'created', 'modified', 'status', 'status_changed', 'submission_uuid', 'uuid', 'course_id', 'item_id'],
            ['id']
        )

        # workflow_assessmentworkflowcancellation
        self.copyDataIn(
            'workflow_assessmentworkflowcancellation',
            'workflow_id',
            workflow_assessmentworkflow_ids,
            ['id', 'comments', 'cancelled_by_id', 'created_at', 'workflow_id'],
            ['id']
        )

        # workflow_assessmentworkflowstep
        self.copyDataIn(
            'workflow_assessmentworkflowstep',
            'workflow_id',
            workflow_assessmentworkflow_ids,
            ['id', 'name', 'submitter_completed_at', 'assessment_completed_at', 'order_num', 'workflow_id'],
            ['id']
        )

        
    def migrateCourseActivityAssessment(self):
        # assessment_peerworkflow
        assessment_peerworkflow_ids = self.copyData(
            'assessment_peerworkflow',
            {'course_id': self.course_id},
            ['id', 'student_id', 'item_id', 'course_id', 'submission_uuid', 'created_at', 'completed_at', 'grading_completed_at', 'cancelled_at'],
            ['id']
        )

        assessment_peerworkflowitem_author_rows = self.selectRowsIn(
            'assessment_peerworkflowitem',
            'author_id',
            assessment_peerworkflow_ids
        )
        assessment_peerworkflowitem_scorer_rows = self.selectRowsIn(
            'assessment_peerworkflowitem',
            'scorer_id',
            assessment_peerworkflow_ids
        )
        assessment_peerworkflowitem_ids = set([row['id'] for row in assessment_peerworkflowitem_author_rows] + [row['id'] for row in assessment_peerworkflowitem_scorer_rows])
        assessment_assessment_ids = set([row['assessment_id'] for row in assessment_peerworkflowitem_author_rows] + [row['assessment_id'] for row in assessment_peerworkflowitem_scorer_rows])
        assessment_assessment_rows = self.selectRowsIn(
            'assessment_assessment',
            'id',
            assessment_assessment_ids
        )
        assessment_rubric_ids = set([row['rubric_id'] for row in assessment_assessment_rows])
        assessment_rubric_rows = self.selectRowsIn(
            'assessment_rubric',
            'id',
            assessment_rubric_ids
        )
        # assessment_rubric
        for assessment_rubric_row in assessment_rubric_rows:
            insertOrUpdateRow(
                assessment_rubric_row,
                'assessment_rubric',
                ['id', 'content_hash', 'structure_hash'],
                ['id'],
                self.destination,
                self.debug
            )
        # assessment_assessment
        for assessment_assessment_row in assessment_assessment_rows:
            print(assessment_assessment_row)
            assessment_assessment_row['scorer_id'] = self.anonymous_user_id_map[assessment_assessment_row['scorer_id']]
            print(assessment_assessment_row)
            insertOrUpdateRow(
                assessment_assessment_row,
                'assessment_assessment',
                ['id', 'submission_uuid', 'scored_at', 'scorer_id', 'score_type', 'feedback', 'rubric_id'],
                ['id'],
                self.destination,
                self.debug
            )
        # assessment_peerworkflowitem
        for assessment_peerworkflowitem_row in assessment_peerworkflowitem_author_rows + assessment_peerworkflowitem_scorer_rows:
            insertOrUpdateRow(
                assessment_peerworkflowitem_row,
                'assessment_peerworkflowitem',
                ['id', 'submission_uuid', 'started_at', 'scored', 'assessment_id', 'author_id', 'scorer_id'],
                ['id'],
                self.destination,
                self.debug
            )

        # assessment_staffworkflow
        self.copyData(
            'assessment_staffworkflow',
            {'course_id': self.course_id},
            ['id', 'scorer_id', 'course_id', 'item_id', 'submission_uuid', 'created_at', 'grading_completed_at', 'grading_started_at', 'cancelled_at', 'assessment'],
            ['id']
        )

        # assessment_criterion
        assessment_criterion_ids = self.copyDataIn(
            'assessment_criterion',
            'rubric_id',
            assessment_rubric_ids,
            ['id', 'name', 'label', 'order_num', 'prompt', 'rubric_id'],
            ['id']
        )
        
        # assessment_criterionoption
        assessment_criterionoption_ids = self.copyDataIn(
            'assessment_criterionoption',
            'criterion_id',
            assessment_criterion_ids,
            ['id', 'order_num', 'points', 'name', 'label', 'explanation', 'criterion_id'],
            ['id']
        )

        # assessment_assessmentpart
        assessment_assessmentpart_ids = set()
        assessment_assessment_ids_parts = set()
        rows = self.selectRowsIn(
            'assessment_assessmentpart',
            'assessment_id',
            assessment_assessment_ids
        )
        assessment_assessmentpart_ids.update([row['id'] for row in rows])
        assessment_assessment_ids_parts.update([row['assessment_id'] for row in rows])
        rows = self.selectRowsIn(
            'assessment_assessmentpart',
            'criterion_id',
            assessment_criterion_ids
        )
        assessment_assessmentpart_ids.update([row['id'] for row in rows])
        assessment_assessment_ids_parts.update([row['assessment_id'] for row in rows])
        rows = self.selectRowsIn(
            'assessment_assessmentpart',
            'option_id',
            assessment_criterionoption_ids
        )
        assessment_assessmentpart_ids.update([row['id'] for row in rows])
        assessment_assessment_ids_parts.update([row['assessment_id'] for row in rows])
        
        self.copyDataIn(
            'assessment_assessment',
            'id',
            assessment_assessment_ids_parts,
            ['id', 'submission_uuid', 'scored_at', 'scorer_id', 'score_type', 'feedback', 'rubric_id'],
            ['id']
        )
        self.copyDataIn(
            'assessment_assessmentpart',
            'id',
            assessment_assessmentpart_ids,
            ['id', 'feedback', 'assessment_id', 'criterion_id', 'option_id'],
            ['id']
        )

        self.fill_assessment_trainingexample()

        self.fill_assessment_assessmentfeedback(assessment_assessment_ids)

    def fill_assessment_assessmentfeedback(self, assessment_assessment_ids):
        assessmentfeedback_id_ids = self.selectFieldIn(
            'assessment_assessmentfeedback_assessments',
            'assessmentfeedback_id',
            'assessment_id',
            assessment_assessment_ids
        )

        # assessment_assessmentfeedback
        # id, submission_uuid, feedback_text
        assessment_assessmentfeedback_ids = self.copyDataIn(
            'assessment_assessmentfeedback',
            'id',
            assessmentfeedback_id_ids,
            ['id', 'submission_uuid', 'feedback_text'],
            ['id']
        )
        # assessment_assessmentfeedback_assessments
        # id, assessmentfeedback_id, assessment_id
        assessment_assessmentfeedback_assessments_ids = self.copyDataIn(
            'assessment_assessmentfeedback_assessments',
            'assessmentfeedback_id',
            assessment_assessmentfeedback_ids,
            ['id', 'assessmentfeedback_id', 'assessment_id'],
            ['id']
        )

        assessment_assessmentfeedback_option_assessmentfeedbackoption_ids = self.selectFieldIn(
            'assessment_assessmentfeedback_options',
            'assessmentfeedbackoption_id',
            'assessmentfeedback_id',
            assessmentfeedback_id_ids
        )

        # assessment_assessmentfeedbackoption
        # id, tex
        assessment_assessmentfeedbackoption_ids = self.copyDataIn(
            'assessment_assessmentfeedbackoption',
            'id',
            assessment_assessmentfeedback_option_assessmentfeedbackoption_ids,
            ['id', 'text'],
            ['id']
        )

        # assessment_assessmentfeedback_options
        # id, assessmentfeedback_id, assessmentfeedbackoption_id
        self.copyDataIn(
            'assessment_assessmentfeedback_options',
            'assessmentfeedback_id',
            assessmentfeedback_id_ids,
            ['id', 'assessmentfeedback_id', 'assessmentfeedbackoption_id'],
            ['id']
        )


    def fill_assessment_trainingexample(self):
        assessment_studenttrainingworkflow_ids = self.copyData(
            'assessment_studenttrainingworkflow',
            {'course_id': self.course_id},
            ['id', 'submission_uuid', 'student_id', 'item_id', 'course_id'],
            ['id']
        )
        
        assessment_studenttrainingworkflowitem_training_example_ids = self.selectFieldIn(
            'assessment_studenttrainingworkflowitem',
            'training_example_id',
            'workflow_id',
            assessment_studenttrainingworkflow_ids
        )

        assessment_trainingexample_rubric_ids = self.selectFieldIn(
            'assessment_trainingexample',
            'rubric_id',
            'id',
            assessment_studenttrainingworkflowitem_training_example_ids
        )

        assessment_rubric_ids = self.copyDataIn(
            'assessment_rubric',
            'id',
            assessment_trainingexample_rubric_ids,
            ['id', 'content_hash', 'structure_hash'],
            ['id']
        )
        assessment_trainingexample_ids = self.copyDataIn(
            'assessment_trainingexample',
            'rubric_id',
            assessment_trainingexample_rubric_ids,
            ['id', 'raw_answer', 'content_hash', 'rubric_id'],
            ['id']
        )
        assessment_studenttrainingworkflowitem_ids = self.copyDataIn(
            'assessment_studenttrainingworkflowitem',
            'workflow_id',
            assessment_studenttrainingworkflow_ids,
            ['id', 'order_num', 'started_at', 'completed_at', 'training_example_id', 'workflow_id'],
            ['id']
        )
        self.copyDataIn(
            'assessment_studenttrainingworkflowitem',
            'training_example_id',
            assessment_trainingexample_ids,
            ['id', 'order_num', 'started_at', 'completed_at', 'training_example_id', 'workflow_id'],
            ['id']
        )
        
    def copyDataIn(self, table_name, select, values, fields, keys):
        rows = self.selectRowsIn(
            table_name,
            select,
            values
        )
        pks = []
        for row in rows:
            pks.append(insertOrUpdateRow(
                self.substitute(table_name, row.copy()),
                table_name,
                fields,
                keys,
                self.destination,
                self.debug
            ))
        return pks
        
    def copyData(self, table_name, select, fields, keys):
        rows =  self.selectRows(
            table_name,
            select
        )
        pks = []
        for row in rows:
            pks.append(
                insertOrUpdateRow(
                    self.substitute(table_name, row.copy()),
                    table_name,
                    fields,
                    keys,
                    self.destination,
                    self.debug
                )
            )
        return pks

    def selectRows(self, table_name, select):
        return selectRows(
            table_name,
            select,
            CONNECTION_SOURCE,
            self.debug
        )

    def selectRowsIn(self, table_name, param, values):
        return selectRowsIn(
            table_name,
            param,
            values,
            CONNECTION_SOURCE,
            self.debug
        )

    def substitute(self, table_name, row):
        if 'user_id' in row:
            row['user_id'] = self.user_id_map[row['user_id']]
            
        #if 'course_id' in row:
        #    row['course_id'] = self.course_id_map[row['course_id']]

        # experiments_experimentdata has key field as course_id
        #if table_name == 'experiments_experimentdata' and 'key' in row:
        #    row['key'] = self.course_id_map[row['key']]

        # courseware_studentmodule has student_id field as user_id
        if table_name == 'courseware_studentmodule' and 'student_id' in row:
            row['student_id'] = self.user_id_map[row['student_id']]

        if table_name == 'assessment_peerworkflow' and 'student_id' in row:
            row['student_id'] = self.anonymous_user_id_map[row['student_id']]

        if table_name == 'assessment_studenttrainingworkflow' and 'student_id' in row:
            row['student_id'] = self.anonymous_user_id_map[row['student_id']]

        if table_name == 'submissions_studentitem' and 'student_id' in row:
            row['student_id'] = self.anonymous_user_id_map[row['student_id']]

        if table_name == 'workflow_assessmentworkflowcancellation' and 'cancelled_by_id' in row:
            row['cancelled_by_id'] = self.anonymous_user_id_map[row['cancelled_by_id']]

        if table_name == 'assessment_assessment' and 'scorer_id' in row:
            row['scorer_id'] = self.anonymous_user_id_map[row['scorer_id']]

        return row

    def course_id_substitute(self):
        result = self.course_id
        for i in self.course_map[self.destination]:
            result = re.sub(
                r'course-v1:{}'.format(i),
                'course-v1:{}'.format(self.course_map[self.destination][i]),
                result
            )
        return result

    def mkdir(self, vm):
        return_code, stdout, stderr = cmd([
            'ssh', 'ubuntu@{}'.format(vm),
            'sudo', 'rm', '-rf', self.export_dir
        ], self.debug)
        if return_code != 0: raise migrateCourseException("CMD error <{}>".format(stderr))

        return_code, stdout, stderr = cmd([
            'ssh', 'ubuntu@{}'.format(vm),
            'sudo', 'mkdir', '--mode', '0777', self.export_dir
        ], self.debug)
        if return_code != 0: raise migrateCourseException("CMD error <{}>".format(stderr))

    def courseExists(self):
        return_code, stdout, stderr = cmd([
            'ssh', 'ubuntu@zh-staging-swarm-1',
            '/home/ubuntu/.local/bin/docker-run-command', 'openedx-university_cms',
            "'python manage.py cms --settings=tutor.production dump_course_ids'"
        ], self.debug)
        if return_code == 0:
            for line in stdout.decode('utf-8').split('\n'):
                if line == self.course_id:
                    logger.info("Course exists, specify --overwrite to recreate the course")
                    return True
            return False
        else:
            raise migrateCourseException("CMD error <{}>".format(stdout))

    def exportCourse(self):
        self.mkdir('zh-staging-app-205')

        return_code, stdout, stderr = cmd([
            'ssh', 'ubuntu@zh-staging-app-205',
            'sudo', '-u', 'www-data',
            '/edx/bin/python.edxapp', '/edx/bin/manage.edxapp',
            'cms', 'export', self.course_id, self.export_dir,
            '--settings', 'openstack'
        ], self.debug)
        if return_code != 0: raise migrateCourseException("CMD error")

    def importCourse(self):
        self.mkdir('zh-staging-swarm-1')

        return_code, stdout, stderr = cmd([
            'ssh', 'ubuntu@zh-staging-swarm-1',
            'scp', '-r', 'ubuntu@zh-staging-app-205:{}'.format(self.export_dir),
            '/'.join(self.import_dir.split('/')[0:-1])
        ], self.debug)
        if return_code != 0: raise migrateCourseException("CMD error")

        # docker-run-command openedx-university_lms 'python manage.py cms --settings=tutor.production bla bla bla '
        return_code, stdout, stderr = cmd([
            'ssh', 'ubuntu@zh-staging-swarm-1',
            '/home/ubuntu/.local/bin/docker-run-command', 'openedx-university_cms',
            "'python manage.py lms --settings=tutor.production import {} {}'".format(self.course_id, self.import_dir_docker)
        ], self.debug)
        if return_code != 0: raise migrateCourseException("CMD error")

    def selectField(self, table_name, field, params):
        return selectField(
            table_name,
            field,
            params,
            CONNECTION_SOURCE,
            self.debug
        )

    def selectFieldIn(self, table_name, field, param, values):
        return selectFieldIn(
            table_name,
            field,
            param,
            values,
            CONNECTION_SOURCE,
            self.debug
        )

    def generate_anonymous_user_id(self, source_user_id):
        user_id = self.user_id_map[source_user_id]
        return_code, stdout, stderr = cmd([
            'ssh', 'ubuntu@zh-staging-swarm-1',
            '~/.local/bin/docker-run-command',
            'openedx-university_lms',
            './manage.py', 'cms',
            '--settings=tutor.production',
            'shell', '-c',
            '"from django.contrib.auth.models import User; from common.djangoapps.student.models import anonymous_id_for_user; a=anonymous_id_for_user(User.objects.get(pk={}), \'course-v1:CSM+01+2020\');print(\'anonymous_user_id=\'+a)"'.format(user_id)
        ], self.debug)
        if return_code == 0:
            for line in stdout.decode('utf-8').split('\n'):
                if line.find('anonymous_user_id=') == 0:
                    return line[18:]
            return None
        else:
            raise migrateCourseException("CMD error <{}>".format(stderr))