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
            self.deleteCourseActivitySubmissionFiles()
            #self.deleteCourseActivitySubmission()
            #self.deleteCourseActivityWorkflow()
            #self.deleteCourseActivityAssessment()
            #self.deleteCourseActivityCourseware()
            #self.deleteCourseActivityStudent()
            #self.deleteCourse()
        except Exception as e:
            logger.error(e)
            raise e


    def deleteCourseActivitySubmissionFiles(self):
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
