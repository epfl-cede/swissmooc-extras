import re
import os
import logging
import json
import pprint
from datetime import datetime

from django.db import connections
from django.core.exceptions import ObjectDoesNotExist

from migrate.helpers import insertOrUpdateRow, deleteRows, deleteRowsIn, selectRows, selectRowsIn
from migrate.helpers import CONNECTION_SOURCE, CONNECTION_ID

logger = logging.getLogger(__name__)

class deleteCourseException(BaseException):
    pass

class DeleteCourse:
    def __init__(self, APP_ENV, destination, course_id, debug):
        self.APP_ENV = APP_ENV
        self.destination = destination
        self.course_id = course_id
        self.debug = debug

    def run(self):
        try:
            self.deleteCourseActivitySubmission()
            self.deleteCourseActivityWorkflow()
            self.deleteCourseActivityAssessment()
            self.deleteCourseActivityCourseware()
            self.deleteCourseActivityStudent()
            #self.deleteCourse()
        except Exception as e:
            logger.error(e)
            raise e


    def deleteCourseActivitySubmission(self):
        submissions_studentitem_rows = self.selectRows(
            'submissions_studentitem',
            {'course_id': self.course_id}
        )
        submissions_studentitem_ids = [row['id'] for row in submissions_studentitem_rows]

        submissions_submission_rows = self.selectRowsIn(
            'submissions_submission',
            'student_item_id',
            submissions_studentitem_ids
        )
        submissions_score_rows = self.selectRowsIn(
            'submissions_score',
            'student_item_id',
            submissions_studentitem_ids
        )
        
        self.deleteRowsIn(
            'submissions_teamsubmission',
            'id',
            [row['team_submission_id'] for row in submissions_submission_rows]
        )
        self.deleteRowsIn(
            'submissions_scoresummary',
            'highest_id',
            [row['id'] for row in submissions_score_rows]
        )
        self.deleteRowsIn(
            'submissions_scoresummary',
            'latest_id',
            [row['id'] for row in submissions_score_rows]
        )
        self.deleteRowsIn(
            'submissions_scoresummary',
            'student_item_id',
            submissions_studentitem_ids
        )

        self.deleteRowsIn(
            'submissions_score',
            'submission_id',
            [row['id'] for row in submissions_submission_rows]
        )
        self.deleteRowsIn(
            'submissions_score',
            'student_item_id',
            submissions_studentitem_ids
        )
        self.deleteRowsIn(
            'submissions_submission',
            'student_item_id',
            submissions_studentitem_ids
        )
        self.deleteRows(
            'submissions_studentitem',
            {'course_id': self.course_id}
        )

    def deleteCourseActivityWorkflow(self):
        # workflow_assessmentworkflow
        workflow_assessmentworkflow_rows = self.selectRows(
            'workflow_assessmentworkflow',
            {'course_id': self.course_id},
        )
        workflow_assessmentworkflow_ids = [row['id'] for row in workflow_assessmentworkflow_rows]

        # workflow_assessmentworkflowcancellation
        self.deleteRowsIn(
            'workflow_assessmentworkflowcancellation',
            'workflow_id',
            workflow_assessmentworkflow_ids,
        )

        # workflow_assessmentworkflowstep
        self.deleteRowsIn(
            'workflow_assessmentworkflowstep',
            'workflow_id',
            workflow_assessmentworkflow_ids,
        )
        self.deleteRows(
            'workflow_assessmentworkflow',
            {'course_id': self.course_id},
        )

    def deleteCourseActivityAssessment(self):
        assessment_peerworkflow_rows = self.selectRows(
            'assessment_peerworkflow',
            {'course_id': self.course_id},
        )
        assessment_peerworkflow_ids = [row['id'] for row in assessment_peerworkflow_rows]

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
        self.deleteRowsIn(
            'assessment_rubric',
            'id',
            assessment_rubric_ids
        )
        self.deleteRowsIn(
            'assessment_assessment',
            'id',
            assessment_assessment_ids
        )
        self.deleteRowsIn(
            'assessment_peerworkflowitem',
            'author_id',
            assessment_peerworkflow_ids
        )
        self.deleteRowsIn(
            'assessment_peerworkflowitem',
            'scorer_id',
            assessment_peerworkflow_ids
        )
        self.deleteRows(
            'assessment_peerworkflow',
            {'course_id': self.course_id},
        )

    def deleteCourseActivityCourseware(self):
        courseware_studentmodule_rows = self.selectRows(
            'courseware_studentmodule',
            {'course_id': self.course_id},
        )
        courseware_studentmodule_ids = [row['id'] for row in courseware_studentmodule_rows]
        self.deleteRowsIn(
            'courseware_studentmodulehistory',
            'student_module_id',
            courseware_studentmodule_ids,
        )
        self.deleteRows(
            'courseware_studentmodule',
            {'course_id': self.course_id},
        )
        

    def deleteCourseActivityStudent(self):
        student_courseenrollment_rows = self.selectRows(
            'student_courseenrollment',
            {'course_id': self.course_id},
        )
        student_anonymoususerid_rows = self.selectRows(
            'student_anonymoususerid',
            {'course_id': self.course_id},
        )

        self.deleteRowsIn(
            'experiments_experimentdata',
            'user_id',
            [row['user_id'] for row in student_anonymoususerid_rows]
        )

        # I dont want to regenerate it each time
        #self.deleteRows(
        #    'student_anonymoususerid',
        #    {'course_id': self.course_id},
        #)
        self.deleteRows(
            'student_courseenrollment',
            {'course_id': self.course_id},
        )

    def deleteRows(self, table_name, select):
        return deleteRows(
            table_name,
            select,
            "edxapp_%s" % self.destination,
            self.debug
        )

    def deleteRowsIn(self, table_name, param, values):
        return deleteRowsIn(
            table_name,
            param,
            values,
            "edxapp_%s" % self.destination,
            self.debug
        )

    def selectRows(self, table_name, select):
        return selectRows(
            table_name,
            select,
            "edxapp_%s" % self.destination,
            self.debug
        )

    def selectRowsIn(self, table_name, param, values):
        return selectRowsIn(
            table_name,
            param,
            values,
            "edxapp_%s" % self.destination,
            self.debug
        )
