# -*- coding: utf-8 -*-
# Execute python manage.py lms --settings=tutor.production inspectdb on service openedx-university_lms
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnnouncementsAnnouncement(models.Model):
    content = models.CharField(max_length=1000)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'announcements_announcement'


class ApiAdminApiaccessconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_admin_apiaccessconfig'


class ApiAdminApiaccessrequest(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=255)
    website = models.CharField(max_length=200)
    reason = models.TextField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, unique=True)
    company_address = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    contacted = models.IntegerField()
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_admin_apiaccessrequest'


class AssessmentAssessment(models.Model):
    submission_uuid = models.CharField(max_length=128)
    scored_at = models.DateTimeField()
    scorer_id = models.CharField(max_length=40)
    score_type = models.CharField(max_length=2)
    feedback = models.TextField()
    rubric = models.ForeignKey('AssessmentRubric', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_assessment'


class AssessmentAssessmentfeedback(models.Model):
    submission_uuid = models.CharField(unique=True, max_length=128)
    feedback_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedback'


class AssessmentAssessmentfeedbackAssessments(models.Model):
    assessmentfeedback = models.ForeignKey(AssessmentAssessmentfeedback, models.DO_NOTHING)
    assessment = models.ForeignKey(AssessmentAssessment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedback_assessments'
        unique_together = (('assessmentfeedback', 'assessment'),)


class AssessmentAssessmentfeedbackOptions(models.Model):
    assessmentfeedback = models.ForeignKey(AssessmentAssessmentfeedback, models.DO_NOTHING)
    assessmentfeedbackoption = models.ForeignKey('AssessmentAssessmentfeedbackoption', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedback_options'
        unique_together = (('assessmentfeedback', 'assessmentfeedbackoption'),)


class AssessmentAssessmentfeedbackoption(models.Model):
    text = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedbackoption'


class AssessmentAssessmentpart(models.Model):
    feedback = models.TextField()
    assessment = models.ForeignKey(AssessmentAssessment, models.DO_NOTHING)
    criterion = models.ForeignKey('AssessmentCriterion', models.DO_NOTHING)
    option = models.ForeignKey('AssessmentCriterionoption', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assessment_assessmentpart'


class AssessmentCriterion(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    order_num = models.PositiveIntegerField()
    prompt = models.TextField()
    rubric = models.ForeignKey('AssessmentRubric', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_criterion'


class AssessmentCriterionoption(models.Model):
    order_num = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    explanation = models.TextField()
    criterion = models.ForeignKey(AssessmentCriterion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_criterionoption'


class AssessmentHistoricalsharedfileupload(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    team_id = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    owner_id = models.CharField(max_length=255)
    file_key = models.CharField(max_length=255)
    description = models.TextField()
    size = models.BigIntegerField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'assessment_historicalsharedfileupload'


class AssessmentPeerworkflow(models.Model):
    student_id = models.CharField(max_length=40)
    item_id = models.CharField(max_length=128)
    course_id = models.CharField(max_length=255)
    submission_uuid = models.CharField(unique=True, max_length=128)
    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    grading_completed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assessment_peerworkflow'


class AssessmentPeerworkflowitem(models.Model):
    submission_uuid = models.CharField(max_length=128)
    started_at = models.DateTimeField()
    scored = models.IntegerField()
    assessment = models.ForeignKey(AssessmentAssessment, models.DO_NOTHING, blank=True, null=True)
    author = models.ForeignKey(AssessmentPeerworkflow, models.DO_NOTHING)
    scorer = models.ForeignKey(AssessmentPeerworkflow, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_peerworkflowitem'


class AssessmentRubric(models.Model):
    content_hash = models.CharField(unique=True, max_length=40)
    structure_hash = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'assessment_rubric'


class AssessmentSharedfileupload(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    team_id = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    owner_id = models.CharField(max_length=255)
    file_key = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    size = models.BigIntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'assessment_sharedfileupload'


class AssessmentStaffworkflow(models.Model):
    scorer_id = models.CharField(max_length=40)
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=128)
    submission_uuid = models.CharField(unique=True, max_length=128)
    created_at = models.DateTimeField()
    grading_completed_at = models.DateTimeField(blank=True, null=True)
    grading_started_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    assessment = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assessment_staffworkflow'


class AssessmentStudenttrainingworkflow(models.Model):
    submission_uuid = models.CharField(unique=True, max_length=128)
    student_id = models.CharField(max_length=40)
    item_id = models.CharField(max_length=128)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'assessment_studenttrainingworkflow'


class AssessmentStudenttrainingworkflowitem(models.Model):
    order_num = models.PositiveIntegerField()
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    training_example = models.ForeignKey('AssessmentTrainingexample', models.DO_NOTHING)
    workflow = models.ForeignKey(AssessmentStudenttrainingworkflow, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_studenttrainingworkflowitem'
        unique_together = (('workflow', 'order_num'),)


class AssessmentTeamstaffworkflow(models.Model):
    staffworkflow_ptr = models.ForeignKey(AssessmentStaffworkflow, models.DO_NOTHING, primary_key=True)
    team_submission_uuid = models.CharField(unique=True, max_length=128)

    class Meta:
        managed = False
        db_table = 'assessment_teamstaffworkflow'


class AssessmentTrainingexample(models.Model):
    raw_answer = models.TextField()
    content_hash = models.CharField(unique=True, max_length=40)
    rubric = models.ForeignKey(AssessmentRubric, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_trainingexample'


class AssessmentTrainingexampleOptionsSelected(models.Model):
    trainingexample = models.ForeignKey(AssessmentTrainingexample, models.DO_NOTHING)
    criterionoption = models.ForeignKey(AssessmentCriterionoption, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'assessment_trainingexample_options_selected'
        unique_together = (('trainingexample', 'criterionoption'),)


class AuthAccountrecovery(models.Model):
    secondary_email = models.CharField(unique=True, max_length=254)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, unique=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_accountrecovery'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthRegistration(models.Model):
    activation_key = models.CharField(unique=True, max_length=32)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'auth_registration'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthUserprofile(models.Model):
    name = models.CharField(max_length=255)
    meta = models.TextField()
    courseware = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    year_of_birth = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    level_of_education = models.CharField(max_length=6, blank=True, null=True)
    mailing_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    allow_certificate = models.IntegerField()
    bio = models.CharField(max_length=3000, blank=True, null=True)
    profile_image_uploaded_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_userprofile'


class BadgesBadgeassertion(models.Model):
    data = models.TextField()
    backend = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)
    assertion_url = models.CharField(max_length=200)
    modified = models.DateTimeField()
    created = models.DateTimeField()
    badge_class = models.ForeignKey('BadgesBadgeclass', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'badges_badgeassertion'


class BadgesBadgeclass(models.Model):
    slug = models.CharField(max_length=255)
    issuing_component = models.CharField(max_length=50)
    display_name = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    description = models.TextField()
    criteria = models.TextField()
    mode = models.CharField(max_length=100)
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'badges_badgeclass'
        unique_together = (('slug', 'issuing_component', 'course_id'),)


class BadgesCoursecompleteimageconfiguration(models.Model):
    mode = models.CharField(unique=True, max_length=125)
    icon = models.CharField(max_length=100)
    default = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'badges_coursecompleteimageconfiguration'


class BadgesCourseeventbadgesconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    courses_completed = models.TextField()
    courses_enrolled = models.TextField()
    course_groups = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'badges_courseeventbadgesconfiguration'


class BlackboardBlackboardenterprisecustomerconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    blackboard_base_url = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255)
    enterprise_customer = models.ForeignKey('EnterpriseEnterprisecustomer', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'blackboard_blackboardenterprisecustomerconfiguration'


class BlackboardBlackboardlearnerdatatransmissionaudit(models.Model):
    blackboard_user_email = models.CharField(max_length=255)
    completed_timestamp = models.CharField(max_length=10)
    course_id = models.CharField(max_length=255)
    course_completed = models.IntegerField()
    enterprise_course_enrollment_id = models.PositiveIntegerField()
    grade = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    total_hours = models.FloatField(blank=True, null=True)
    created = models.DateTimeField()
    error_message = models.TextField()
    status = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'blackboard_blackboardlearnerdatatransmissionaudit'


class BlackboardHistoricalblackboardenterprisecustomerconfiguration(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    blackboard_base_url = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blackboard_historicalblackboardenterprisecustomerconfiguration'


class BlockStructure(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    data_usage_key = models.CharField(unique=True, max_length=255)
    data_version = models.CharField(max_length=255, blank=True, null=True)
    data_edit_timestamp = models.DateTimeField(blank=True, null=True)
    transformers_schema_version = models.CharField(max_length=255)
    block_structure_schema_version = models.CharField(max_length=255)
    data = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'block_structure'


class BlockStructureConfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    num_versions_to_keep = models.IntegerField(blank=True, null=True)
    cache_timeout_in_seconds = models.IntegerField(blank=True, null=True)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'block_structure_config'


class BookmarksBookmark(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_key = models.CharField(max_length=255)
    usage_key = models.CharField(max_length=255)
    path = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    xblock_cache = models.ForeignKey('BookmarksXblockcache', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bookmarks_bookmark'
        unique_together = (('user', 'usage_key'),)


class BookmarksXblockcache(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_key = models.CharField(max_length=255)
    usage_key = models.CharField(unique=True, max_length=255)
    display_name = models.CharField(max_length=255)
    paths = models.TextField()

    class Meta:
        managed = False
        db_table = 'bookmarks_xblockcache'


class BrandingBrandingapiconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branding_brandingapiconfig'


class BrandingBrandinginfoconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    configuration = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branding_brandinginfoconfig'


class BulkEmailBulkemailflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    require_course_email_auth = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bulk_email_bulkemailflag'


class BulkEmailCohorttarget(models.Model):
    target_ptr = models.ForeignKey('BulkEmailTarget', models.DO_NOTHING, primary_key=True)
    cohort = models.ForeignKey('CourseGroupsCourseusergroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bulk_email_cohorttarget'


class BulkEmailCourseauthorization(models.Model):
    course_id = models.CharField(unique=True, max_length=255)
    email_enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bulk_email_courseauthorization'


class BulkEmailCourseemail(models.Model):
    slug = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    html_message = models.TextField(blank=True, null=True)
    text_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    to_option = models.CharField(max_length=64)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    from_addr = models.CharField(max_length=255, blank=True, null=True)
    sender = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bulk_email_courseemail'


class BulkEmailCourseemailTargets(models.Model):
    courseemail = models.ForeignKey(BulkEmailCourseemail, models.DO_NOTHING)
    target = models.ForeignKey('BulkEmailTarget', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bulk_email_courseemail_targets'
        unique_together = (('courseemail', 'target'),)


class BulkEmailCourseemailtemplate(models.Model):
    html_template = models.TextField(blank=True, null=True)
    plain_template = models.TextField(blank=True, null=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bulk_email_courseemailtemplate'


class BulkEmailCoursemodetarget(models.Model):
    target_ptr = models.ForeignKey('BulkEmailTarget', models.DO_NOTHING, primary_key=True)
    track = models.ForeignKey('CourseModesCoursemode', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bulk_email_coursemodetarget'


class BulkEmailOptout(models.Model):
    course_id = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bulk_email_optout'
        unique_together = (('user', 'course_id'),)


class BulkEmailTarget(models.Model):
    target_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'bulk_email_target'


class BulkGradesScoreoverrider(models.Model):
    modified = models.DateTimeField()
    created = models.DateTimeField()
    module_id = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bulk_grades_scoreoverrider'


class CalendarSyncHistoricalusercalendarsyncconfig(models.Model):
    id = models.IntegerField()
    course_key = models.CharField(max_length=255)
    enabled = models.IntegerField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    ics_sequence = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'calendar_sync_historicalusercalendarsyncconfig'


class CalendarSyncUsercalendarsyncconfig(models.Model):
    course_key = models.CharField(max_length=255)
    enabled = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    ics_sequence = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'calendar_sync_usercalendarsyncconfig'
        unique_together = (('user', 'course_key'),)


class CanvasCanvasenterprisecustomerconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    canvas_account_id = models.IntegerField(blank=True, null=True)
    canvas_base_url = models.CharField(max_length=255, blank=True, null=True)
    enterprise_customer = models.ForeignKey('EnterpriseEnterprisecustomer', models.DO_NOTHING, unique=True)
    refresh_token = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'canvas_canvasenterprisecustomerconfiguration'


class CanvasCanvaslearnerdatatransmissionaudit(models.Model):
    canvas_user_email = models.CharField(max_length=255)
    enterprise_course_enrollment_id = models.PositiveIntegerField()
    course_id = models.CharField(max_length=255)
    course_completed = models.IntegerField()
    completed_timestamp = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    error_message = models.TextField()
    created = models.DateTimeField()
    grade = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'canvas_canvaslearnerdatatransmissionaudit'


class CanvasHistoricalcanvasenterprisecustomerconfiguration(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    canvas_account_id = models.IntegerField(blank=True, null=True)
    canvas_base_url = models.CharField(max_length=255, blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    refresh_token = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'canvas_historicalcanvasenterprisecustomerconfiguration'


class CatalogCatalogintegration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    internal_api_url = models.CharField(max_length=200)
    cache_ttl = models.PositiveIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    service_username = models.CharField(max_length=100)
    page_size = models.PositiveIntegerField()
    long_term_cache_ttl = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'catalog_catalogintegration'


class CeleryTaskmeta(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.IntegerField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'celery_taskmeta'


class CeleryTasksetmeta(models.Model):
    taskset_id = models.CharField(unique=True, max_length=255)
    result = models.TextField()
    date_done = models.DateTimeField()
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'celery_tasksetmeta'


class CeleryUtilsFailedtask(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    task_name = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    args = models.TextField()
    kwargs = models.TextField()
    exc = models.CharField(max_length=255)
    datetime_resolved = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'celery_utils_failedtask'


class CertificatesCertificategenerationconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificates_certificategenerationconfiguration'


class CertificatesCertificategenerationcoursesetting(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_key = models.CharField(max_length=255)
    language_specific_templates_enabled = models.IntegerField()
    self_generation_enabled = models.IntegerField()
    include_hours_of_effort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificates_certificategenerationcoursesetting'


class CertificatesCertificategenerationhistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    is_regeneration = models.IntegerField()
    generated_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    instructor_task = models.ForeignKey('InstructorTaskInstructortask', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'certificates_certificategenerationhistory'


class CertificatesCertificatehtmlviewconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    configuration = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificates_certificatehtmlviewconfiguration'


class CertificatesCertificateinvalidation(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    active = models.IntegerField()
    generated_certificate = models.ForeignKey('CertificatesGeneratedcertificate', models.DO_NOTHING)
    invalidated_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'certificates_certificateinvalidation'


class CertificatesCertificatetemplate(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    template = models.TextField()
    organization_id = models.IntegerField(blank=True, null=True)
    course_key = models.CharField(max_length=255, blank=True, null=True)
    mode = models.CharField(max_length=125, blank=True, null=True)
    is_active = models.IntegerField()
    language = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificates_certificatetemplate'
        unique_together = (('organization_id', 'course_key', 'mode', 'language'),)


class CertificatesCertificatetemplateasset(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True, null=True)
    asset = models.CharField(max_length=255)
    asset_slug = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificates_certificatetemplateasset'


class CertificatesCertificatewhitelist(models.Model):
    course_id = models.CharField(max_length=255)
    whitelist = models.IntegerField()
    created = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'certificates_certificatewhitelist'


class CertificatesExamplecertificate(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    description = models.CharField(max_length=255)
    uuid = models.CharField(unique=True, max_length=255)
    access_key = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    template = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    error_reason = models.TextField(blank=True, null=True)
    download_url = models.CharField(max_length=255, blank=True, null=True)
    example_cert_set = models.ForeignKey('CertificatesExamplecertificateset', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'certificates_examplecertificate'


class CertificatesExamplecertificateset(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'certificates_examplecertificateset'


class CertificatesGeneratedcertificate(models.Model):
    course_id = models.CharField(max_length=255)
    verify_uuid = models.CharField(max_length=32)
    download_uuid = models.CharField(max_length=32)
    download_url = models.CharField(max_length=128)
    grade = models.CharField(max_length=5)
    key = models.CharField(max_length=32)
    distinction = models.IntegerField()
    status = models.CharField(max_length=32)
    mode = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    error_reason = models.CharField(max_length=512)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'certificates_generatedcertificate'
        unique_together = (('user', 'course_id'),)


class CertificatesHistoricalgeneratedcertificate(models.Model):
    id = models.IntegerField()
    course_id = models.CharField(max_length=255)
    verify_uuid = models.CharField(max_length=32)
    download_uuid = models.CharField(max_length=32)
    download_url = models.CharField(max_length=128)
    grade = models.CharField(max_length=5)
    key = models.CharField(max_length=32)
    distinction = models.IntegerField()
    status = models.CharField(max_length=32)
    mode = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    error_reason = models.CharField(max_length=512)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificates_historicalgeneratedcertificate'


class CommerceCommerceconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    checkout_on_ecommerce_service = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    cache_ttl = models.PositiveIntegerField()
    receipt_page = models.CharField(max_length=255)
    enable_automatic_refund_approval = models.IntegerField()
    basket_checkout_page = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'commerce_commerceconfiguration'


class CompletionBlockcompletion(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    course_key = models.CharField(max_length=255)
    block_key = models.CharField(max_length=255)
    block_type = models.CharField(max_length=64)
    completion = models.FloatField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'completion_blockcompletion'
        unique_together = (('course_key', 'block_key', 'user'),)


class ConsentDatasharingconsent(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    username = models.CharField(max_length=255)
    granted = models.IntegerField(blank=True, null=True)
    course_id = models.CharField(max_length=255)
    enterprise_customer = models.ForeignKey('EnterpriseEnterprisecustomer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'consent_datasharingconsent'
        unique_together = (('enterprise_customer', 'username', 'course_id'),)


class ConsentDatasharingconsenttextoverrides(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    page_title = models.CharField(max_length=255)
    left_sidebar_text = models.TextField(blank=True, null=True)
    top_paragraph = models.TextField(blank=True, null=True)
    agreement_text = models.TextField(blank=True, null=True)
    continue_text = models.CharField(max_length=255)
    abort_text = models.CharField(max_length=255)
    policy_dropdown_header = models.CharField(max_length=255, blank=True, null=True)
    policy_paragraph = models.TextField(blank=True, null=True)
    confirmation_modal_header = models.CharField(max_length=255)
    confirmation_modal_text = models.TextField()
    modal_affirm_decline_text = models.CharField(max_length=255)
    modal_abort_decline_text = models.CharField(max_length=255)
    declined_notification_title = models.TextField()
    declined_notification_message = models.TextField()
    published = models.IntegerField()
    enterprise_customer = models.ForeignKey('EnterpriseEnterprisecustomer', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'consent_datasharingconsenttextoverrides'


class ConsentHistoricaldatasharingconsent(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    username = models.CharField(max_length=255)
    granted = models.IntegerField(blank=True, null=True)
    course_id = models.CharField(max_length=255)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consent_historicaldatasharingconsent'


class ContentLibrariesContentlibrary(models.Model):
    slug = models.CharField(max_length=50)
    bundle_uuid = models.CharField(unique=True, max_length=32)
    allow_public_learning = models.IntegerField()
    allow_public_read = models.IntegerField()
    org = models.ForeignKey('OrganizationsOrganization', models.DO_NOTHING)
    type = models.CharField(max_length=25)
    license = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'content_libraries_contentlibrary'
        unique_together = (('org', 'slug'),)


class ContentLibrariesContentlibrarypermission(models.Model):
    access_level = models.CharField(max_length=30)
    library = models.ForeignKey(ContentLibrariesContentlibrary, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_libraries_contentlibrarypermission'
        unique_together = (('library', 'group'), ('library', 'user'),)


class ContentTypeGatingContenttypegatingconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField(blank=True, null=True)
    org = models.CharField(max_length=255, blank=True, null=True)
    enabled_as_of = models.DateTimeField(blank=True, null=True)
    studio_override_enabled = models.IntegerField(blank=True, null=True)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('CourseOverviewsCourseoverview', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING, blank=True, null=True)
    org_course = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_gating_contenttypegatingconfig'


class ContentserverCdnuseragentsconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    cdn_user_agents = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contentserver_cdnuseragentsconfig'


class ContentserverCourseassetcachettlconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    cache_ttl = models.PositiveIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contentserver_courseassetcachettlconfig'


class ContentstoreVideouploadconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    profile_whitelist = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contentstore_videouploadconfig'


class CornerstoneCornerstoneenterprisecustomerconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    cornerstone_base_url = models.CharField(max_length=255)
    enterprise_customer = models.ForeignKey('EnterpriseEnterprisecustomer', models.DO_NOTHING, unique=True)
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cornerstone_cornerstoneenterprisecustomerconfiguration'


class CornerstoneCornerstoneglobalconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    completion_status_api_path = models.CharField(max_length=255)
    oauth_api_path = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subject_mapping = models.TextField()
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    languages = models.TextField()

    class Meta:
        managed = False
        db_table = 'cornerstone_cornerstoneglobalconfiguration'


class CornerstoneCornerstonelearnerdatatransmissionaudit(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_guid = models.CharField(max_length=255)
    enterprise_course_enrollment_id = models.PositiveIntegerField(blank=True, null=True)
    course_id = models.CharField(max_length=255)
    session_token = models.CharField(max_length=255)
    callback_url = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    course_completed = models.IntegerField()
    completed_timestamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    grade = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cornerstone_cornerstonelearnerdatatransmissionaudit'
        unique_together = (('user', 'course_id'),)


class CornerstoneHistoricalcornerstoneenterprisecustomerconfiguration(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    cornerstone_base_url = models.CharField(max_length=255)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cornerstone_historicalcornerstoneenterprisecustomerconfiguration'


class CorsCsrfXdomainproxyconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    whitelist = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cors_csrf_xdomainproxyconfiguration'


class CourseActionStateCoursererunstate(models.Model):
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    course_key = models.CharField(max_length=255)
    action = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    should_display = models.IntegerField()
    message = models.CharField(max_length=1000)
    source_course_key = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    created_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    updated_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_action_state_coursererunstate'
        unique_together = (('course_key', 'action'),)


class CourseCreatorsCoursecreator(models.Model):
    state_changed = models.DateTimeField()
    state = models.CharField(max_length=24)
    note = models.CharField(max_length=512)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'course_creators_coursecreator'


class CourseDateSignalsSelfpacedrelativedatesconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField(blank=True, null=True)
    org = models.CharField(max_length=255, blank=True, null=True)
    org_course = models.CharField(max_length=255, blank=True, null=True)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('CourseOverviewsCourseoverview', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_date_signals_selfpacedrelativedatesconfig'


class CourseDurationLimitsCoursedurationlimitconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField(blank=True, null=True)
    org = models.CharField(max_length=255, blank=True, null=True)
    enabled_as_of = models.DateTimeField(blank=True, null=True)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('CourseOverviewsCourseoverview', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING, blank=True, null=True)
    org_course = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_duration_limits_coursedurationlimitconfig'


class CourseGoalsCoursegoal(models.Model):
    course_key = models.CharField(max_length=255)
    goal_key = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_goals_coursegoal'
        unique_together = (('user', 'course_key'),)


class CourseGroupsCohortmembership(models.Model):
    course_id = models.CharField(max_length=255)
    course_user_group = models.ForeignKey('CourseGroupsCourseusergroup', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_groups_cohortmembership'
        unique_together = (('user', 'course_id'),)


class CourseGroupsCoursecohort(models.Model):
    assignment_type = models.CharField(max_length=20)
    course_user_group = models.ForeignKey('CourseGroupsCourseusergroup', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'course_groups_coursecohort'


class CourseGroupsCoursecohortssettings(models.Model):
    is_cohorted = models.IntegerField()
    course_id = models.CharField(unique=True, max_length=255)
    cohorted_discussions = models.TextField(blank=True, null=True)
    always_cohort_inline_discussions = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course_groups_coursecohortssettings'


class CourseGroupsCourseusergroup(models.Model):
    name = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    group_type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'course_groups_courseusergroup'
        unique_together = (('name', 'course_id'),)


class CourseGroupsCourseusergroupUsers(models.Model):
    courseusergroup = models.ForeignKey(CourseGroupsCourseusergroup, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_groups_courseusergroup_users'
        unique_together = (('courseusergroup', 'user'),)


class CourseGroupsCourseusergrouppartitiongroup(models.Model):
    partition_id = models.IntegerField()
    group_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course_user_group = models.ForeignKey(CourseGroupsCourseusergroup, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'course_groups_courseusergrouppartitiongroup'


class CourseGroupsUnregisteredlearnercohortassignments(models.Model):
    email = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    course_user_group = models.ForeignKey(CourseGroupsCourseusergroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_groups_unregisteredlearnercohortassignments'
        unique_together = (('course_id', 'email'),)


class CourseModesCoursemode(models.Model):
    course_id = models.CharField(max_length=255)
    mode_slug = models.CharField(max_length=100)
    mode_display_name = models.CharField(max_length=255)
    min_price = models.IntegerField()
    currency = models.CharField(max_length=8)
    expiration_datetime = models.DateTimeField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    suggested_prices = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    expiration_datetime_is_explicit = models.IntegerField()
    bulk_sku = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_modes_coursemode'
        unique_together = (('course_id', 'mode_slug', 'currency'),)


class CourseModesCoursemodeexpirationconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    verification_window = models.BigIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_modes_coursemodeexpirationconfig'


class CourseModesCoursemodesarchive(models.Model):
    course_id = models.CharField(max_length=255)
    mode_slug = models.CharField(max_length=100)
    mode_display_name = models.CharField(max_length=255)
    min_price = models.IntegerField()
    suggested_prices = models.CharField(max_length=255)
    currency = models.CharField(max_length=8)
    expiration_date = models.DateField(blank=True, null=True)
    expiration_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_modes_coursemodesarchive'


class CourseModesHistoricalcoursemode(models.Model):
    id = models.IntegerField()
    mode_slug = models.CharField(max_length=100)
    mode_display_name = models.CharField(max_length=255)
    min_price = models.IntegerField()
    currency = models.CharField(max_length=8)
    expiration_datetime = models.DateTimeField(blank=True, null=True)
    expiration_datetime_is_explicit = models.IntegerField()
    expiration_date = models.DateField(blank=True, null=True)
    suggested_prices = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    bulk_sku = models.CharField(max_length=255, blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    course_id = models.CharField(max_length=255, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_modes_historicalcoursemode'


class CourseOverviewsCourseoverview(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    version = models.IntegerField()
    id = models.CharField(primary_key=True, max_length=255)
    field_location = models.CharField(db_column='_location', max_length=255)  # Field renamed because it started with '_'.
    display_name = models.TextField(blank=True, null=True)
    display_number_with_default = models.TextField()
    display_org_with_default = models.TextField()
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    advertised_start = models.TextField(blank=True, null=True)
    course_image_url = models.TextField()
    social_sharing_url = models.TextField(blank=True, null=True)
    end_of_course_survey_url = models.TextField(blank=True, null=True)
    certificates_display_behavior = models.TextField(blank=True, null=True)
    certificates_show_before_end = models.IntegerField()
    cert_html_view_enabled = models.IntegerField()
    has_any_active_web_certificate = models.IntegerField()
    cert_name_short = models.TextField()
    cert_name_long = models.TextField()
    lowest_passing_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    days_early_for_beta = models.FloatField(blank=True, null=True)
    mobile_available = models.IntegerField()
    visible_to_staff_only = models.IntegerField()
    field_pre_requisite_courses_json = models.TextField(db_column='_pre_requisite_courses_json')  # Field renamed because it started with '_'.
    enrollment_start = models.DateTimeField(blank=True, null=True)
    enrollment_end = models.DateTimeField(blank=True, null=True)
    enrollment_domain = models.TextField(blank=True, null=True)
    invitation_only = models.IntegerField()
    max_student_enrollments_allowed = models.IntegerField(blank=True, null=True)
    announcement = models.DateTimeField(blank=True, null=True)
    catalog_visibility = models.TextField(blank=True, null=True)
    course_video_url = models.TextField(blank=True, null=True)
    effort = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    org = models.TextField()
    self_paced = models.IntegerField()
    marketing_url = models.TextField(blank=True, null=True)
    eligible_for_financial_aid = models.IntegerField()
    language = models.TextField(blank=True, null=True)
    certificate_available_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_overviews_courseoverview'


class CourseOverviewsCourseoverviewimageconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    small_width = models.IntegerField()
    small_height = models.IntegerField()
    large_width = models.IntegerField()
    large_height = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_overviews_courseoverviewimageconfig'


class CourseOverviewsCourseoverviewimageset(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    small_url = models.TextField()
    large_url = models.TextField()
    course_overview = models.ForeignKey(CourseOverviewsCourseoverview, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'course_overviews_courseoverviewimageset'


class CourseOverviewsCourseoverviewtab(models.Model):
    tab_id = models.CharField(max_length=50)
    course_overview = models.ForeignKey(CourseOverviewsCourseoverview, models.DO_NOTHING)
    course_staff_only = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    url_slug = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    is_hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course_overviews_courseoverviewtab'


class CourseOverviewsHistoricalcourseoverview(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    version = models.IntegerField()
    id = models.CharField(max_length=255)
    field_location = models.CharField(db_column='_location', max_length=255)  # Field renamed because it started with '_'.
    org = models.TextField()
    display_name = models.TextField(blank=True, null=True)
    display_number_with_default = models.TextField()
    display_org_with_default = models.TextField()
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    advertised_start = models.TextField(blank=True, null=True)
    announcement = models.DateTimeField(blank=True, null=True)
    course_image_url = models.TextField()
    social_sharing_url = models.TextField(blank=True, null=True)
    end_of_course_survey_url = models.TextField(blank=True, null=True)
    certificates_display_behavior = models.TextField(blank=True, null=True)
    certificates_show_before_end = models.IntegerField()
    cert_html_view_enabled = models.IntegerField()
    has_any_active_web_certificate = models.IntegerField()
    cert_name_short = models.TextField()
    cert_name_long = models.TextField()
    certificate_available_date = models.DateTimeField(blank=True, null=True)
    lowest_passing_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    days_early_for_beta = models.FloatField(blank=True, null=True)
    mobile_available = models.IntegerField()
    visible_to_staff_only = models.IntegerField()
    field_pre_requisite_courses_json = models.TextField(db_column='_pre_requisite_courses_json')  # Field renamed because it started with '_'.
    enrollment_start = models.DateTimeField(blank=True, null=True)
    enrollment_end = models.DateTimeField(blank=True, null=True)
    enrollment_domain = models.TextField(blank=True, null=True)
    invitation_only = models.IntegerField()
    max_student_enrollments_allowed = models.IntegerField(blank=True, null=True)
    catalog_visibility = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    course_video_url = models.TextField(blank=True, null=True)
    effort = models.TextField(blank=True, null=True)
    self_paced = models.IntegerField()
    marketing_url = models.TextField(blank=True, null=True)
    eligible_for_financial_aid = models.IntegerField()
    language = models.TextField(blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_overviews_historicalcourseoverview'


class CourseOverviewsSimulatecoursepublishconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    arguments = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_overviews_simulatecoursepublishconfig'


class CoursewareCoursedynamicupgradedeadlineconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    course_id = models.CharField(max_length=255)
    deadline_days = models.PositiveSmallIntegerField()
    opt_out = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courseware_coursedynamicupgradedeadlineconfiguration'


class CoursewareDynamicupgradedeadlineconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    deadline_days = models.PositiveSmallIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courseware_dynamicupgradedeadlineconfiguration'


class CoursewareOfflinecomputedgrade(models.Model):
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField()
    gradeset = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'courseware_offlinecomputedgrade'
        unique_together = (('user', 'course_id'),)


class CoursewareOfflinecomputedgradelog(models.Model):
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    seconds = models.IntegerField()
    nstudents = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'courseware_offlinecomputedgradelog'


class CoursewareOrgdynamicupgradedeadlineconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    org_id = models.CharField(max_length=255)
    deadline_days = models.PositiveSmallIntegerField()
    opt_out = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courseware_orgdynamicupgradedeadlineconfiguration'


class CoursewareStudentfieldoverride(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    value = models.TextField()
    student = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'courseware_studentfieldoverride'
        unique_together = (('course_id', 'field', 'location', 'student'),)


class CoursewareStudentmodule(models.Model):
    id = models.BigAutoField(primary_key=True)
    module_type = models.CharField(max_length=32)
    module_id = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    state = models.TextField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    max_grade = models.FloatField(blank=True, null=True)
    done = models.CharField(max_length=8)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    student_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'courseware_studentmodule'
        unique_together = (('student_id', 'module_id', 'course_id'),)


class CoursewareStudentmodulehistory(models.Model):
    version = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    state = models.TextField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    max_grade = models.FloatField(blank=True, null=True)
    student_module_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'courseware_studentmodulehistory'


class CoursewareXmodulestudentinfofield(models.Model):
    field_name = models.CharField(max_length=64)
    value = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    student = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'courseware_xmodulestudentinfofield'
        unique_together = (('student', 'field_name'),)


class CoursewareXmodulestudentprefsfield(models.Model):
    field_name = models.CharField(max_length=64)
    value = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    module_type = models.CharField(max_length=64)
    student = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'courseware_xmodulestudentprefsfield'
        unique_together = (('student', 'module_type', 'field_name'),)


class CoursewareXmoduleuserstatesummaryfield(models.Model):
    field_name = models.CharField(max_length=64)
    value = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    usage_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'courseware_xmoduleuserstatesummaryfield'
        unique_together = (('usage_id', 'field_name'),)


class CrawlersCrawlersconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    known_user_agents = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawlers_crawlersconfig'


class CredentialsCredentialsapiconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    internal_service_url = models.CharField(max_length=200)
    public_service_url = models.CharField(max_length=200)
    enable_learner_issuance = models.IntegerField()
    enable_studio_authoring = models.IntegerField()
    cache_ttl = models.PositiveIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credentials_credentialsapiconfig'


class CredentialsNotifycredentialsconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    arguments = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credentials_notifycredentialsconfig'


class CreditCreditconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    cache_ttl = models.PositiveIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credit_creditconfig'


class CreditCreditcourse(models.Model):
    course_key = models.CharField(unique=True, max_length=255)
    enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'credit_creditcourse'


class CreditCrediteligibility(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    username = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    course = models.ForeignKey(CreditCreditcourse, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'credit_crediteligibility'
        unique_together = (('username', 'course'),)


class CreditCreditprovider(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    provider_id = models.CharField(unique=True, max_length=255)
    active = models.IntegerField()
    display_name = models.CharField(max_length=255)
    enable_integration = models.IntegerField()
    provider_url = models.CharField(max_length=200)
    provider_status_url = models.CharField(max_length=200)
    provider_description = models.TextField()
    fulfillment_instructions = models.TextField(blank=True, null=True)
    eligibility_email_message = models.TextField()
    receipt_email_message = models.TextField()
    thumbnail_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'credit_creditprovider'


class CreditCreditrequest(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(unique=True, max_length=32)
    username = models.CharField(max_length=255)
    parameters = models.TextField()
    status = models.CharField(max_length=255)
    course = models.ForeignKey(CreditCreditcourse, models.DO_NOTHING)
    provider = models.ForeignKey(CreditCreditprovider, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'credit_creditrequest'
        unique_together = (('username', 'course', 'provider'),)


class CreditCreditrequirement(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    namespace = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    criteria = models.TextField()
    active = models.IntegerField()
    course = models.ForeignKey(CreditCreditcourse, models.DO_NOTHING)
    sort_value = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'credit_creditrequirement'
        unique_together = (('namespace', 'name', 'course'),)


class CreditCreditrequirementstatus(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    username = models.CharField(max_length=255)
    status = models.CharField(max_length=32)
    reason = models.TextField()
    requirement = models.ForeignKey(CreditCreditrequirement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'credit_creditrequirementstatus'
        unique_together = (('username', 'requirement'),)


class DarkLangDarklangconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    released_languages = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    beta_languages = models.TextField()
    enable_beta_languages = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dark_lang_darklangconfig'


class DegreedDegreedenterprisecustomerconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    degreed_company_id = models.CharField(max_length=255)
    enterprise_customer = models.ForeignKey('EnterpriseEnterprisecustomer', models.DO_NOTHING, unique=True)
    transmission_chunk_size = models.IntegerField()
    degreed_base_url = models.CharField(max_length=255)
    degreed_user_id = models.CharField(max_length=255)
    degreed_user_password = models.CharField(max_length=255)
    provider_id = models.CharField(max_length=100)
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'degreed_degreedenterprisecustomerconfiguration'


class DegreedDegreedglobalconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    completion_status_api_path = models.CharField(max_length=255)
    course_api_path = models.CharField(max_length=255)
    oauth_api_path = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'degreed_degreedglobalconfiguration'


class DegreedDegreedlearnerdatatransmissionaudit(models.Model):
    degreed_user_email = models.CharField(max_length=255)
    enterprise_course_enrollment_id = models.PositiveIntegerField()
    course_id = models.CharField(max_length=255)
    course_completed = models.IntegerField()
    completed_timestamp = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    error_message = models.TextField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'degreed_degreedlearnerdatatransmissionaudit'


class DegreedHistoricaldegreedenterprisecustomerconfiguration(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    degreed_company_id = models.CharField(max_length=255)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    transmission_chunk_size = models.IntegerField()
    degreed_base_url = models.CharField(max_length=255)
    degreed_user_id = models.CharField(max_length=255)
    degreed_user_password = models.CharField(max_length=255)
    provider_id = models.CharField(max_length=100)
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'degreed_historicaldegreedenterprisecustomerconfiguration'


class DemographicsHistoricaluserdemographics(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    show_call_to_action = models.IntegerField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demographics_historicaluserdemographics'


class DemographicsUserdemographics(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    show_call_to_action = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'demographics_userdemographics'


class DiscountsDiscountpercentageconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField(blank=True, null=True)
    org = models.CharField(max_length=255, blank=True, null=True)
    org_course = models.CharField(max_length=255, blank=True, null=True)
    percentage = models.PositiveIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(CourseOverviewsCourseoverview, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discounts_discountpercentageconfig'


class DiscountsDiscountrestrictionconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField(blank=True, null=True)
    org = models.CharField(max_length=255, blank=True, null=True)
    org_course = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.IntegerField(blank=True, null=True)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(CourseOverviewsCourseoverview, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discounts_discountrestrictionconfig'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    worker = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoCommentClientPermission(models.Model):
    name = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'django_comment_client_permission'


class DjangoCommentClientPermissionRoles(models.Model):
    permission = models.ForeignKey(DjangoCommentClientPermission, models.DO_NOTHING)
    role = models.ForeignKey('DjangoCommentClientRole', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_comment_client_permission_roles'
        unique_together = (('permission', 'role'),)


class DjangoCommentClientRole(models.Model):
    name = models.CharField(max_length=30)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'django_comment_client_role'


class DjangoCommentClientRoleUsers(models.Model):
    role = models.ForeignKey(DjangoCommentClientRole, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_comment_client_role_users'
        unique_together = (('role', 'user'),)


class DjangoCommentCommonCoursediscussionsettings(models.Model):
    course_id = models.CharField(unique=True, max_length=255)
    always_divide_inline_discussions = models.IntegerField()
    divided_discussions = models.TextField(blank=True, null=True)
    division_scheme = models.CharField(max_length=20)
    discussions_id_map = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_comment_common_coursediscussionsettings'


class DjangoCommentCommonDiscussionsidmapping(models.Model):
    course_id = models.CharField(primary_key=True, max_length=255)
    mapping = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_comment_common_discussionsidmapping'


class DjangoCommentCommonForumsconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    connection_timeout = models.FloatField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_comment_common_forumsconfig'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoRedirect(models.Model):
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING)
    old_path = models.CharField(max_length=200)
    new_path = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'django_redirect'
        unique_together = (('site', 'old_path'),)


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class DjceleryCrontabschedule(models.Model):
    minute = models.CharField(max_length=64)
    hour = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=64)
    month_of_year = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'djcelery_crontabschedule'


class DjceleryIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'djcelery_intervalschedule'


class DjceleryPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.PositiveIntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjceleryCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjceleryIntervalschedule, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_periodictask'


class DjceleryPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'djcelery_periodictasks'


class DjceleryTaskstate(models.Model):
    state = models.CharField(max_length=64)
    task_id = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=200, blank=True, null=True)
    tstamp = models.DateTimeField()
    args = models.TextField(blank=True, null=True)
    kwargs = models.TextField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    retries = models.IntegerField()
    hidden = models.IntegerField()
    worker = models.ForeignKey('DjceleryWorkerstate', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_taskstate'


class DjceleryWorkerstate(models.Model):
    hostname = models.CharField(unique=True, max_length=255)
    last_heartbeat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_workerstate'


class EdxWhenContentdate(models.Model):
    course_id = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    policy = models.ForeignKey('EdxWhenDatepolicy', models.DO_NOTHING)
    active = models.IntegerField()
    field = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'edx_when_contentdate'
        unique_together = (('policy', 'location', 'field'),)


class EdxWhenDatepolicy(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    abs_date = models.DateTimeField(blank=True, null=True)
    rel_date = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edx_when_datepolicy'


class EdxWhenUserdate(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    abs_date = models.DateTimeField(blank=True, null=True)
    rel_date = models.BigIntegerField(blank=True, null=True)
    reason = models.TextField()
    actor = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    content_date = models.ForeignKey(EdxWhenContentdate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'edx_when_userdate'


class EdxvalCoursevideo(models.Model):
    course_id = models.CharField(max_length=255)
    video = models.ForeignKey('EdxvalVideo', models.DO_NOTHING)
    is_hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'edxval_coursevideo'
        unique_together = (('course_id', 'video'),)


class EdxvalEncodedvideo(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    url = models.CharField(max_length=200)
    file_size = models.PositiveIntegerField()
    bitrate = models.PositiveIntegerField()
    profile = models.ForeignKey('EdxvalProfile', models.DO_NOTHING)
    video = models.ForeignKey('EdxvalVideo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'edxval_encodedvideo'


class EdxvalProfile(models.Model):
    profile_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'edxval_profile'


class EdxvalThirdpartytranscriptcredentialsstate(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    org = models.CharField(max_length=32)
    provider = models.CharField(max_length=20)
    has_creds = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'edxval_thirdpartytranscriptcredentialsstate'
        unique_together = (('org', 'provider'),)


class EdxvalTranscriptpreference(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(unique=True, max_length=255)
    provider = models.CharField(max_length=20)
    cielo24_fidelity = models.CharField(max_length=20, blank=True, null=True)
    cielo24_turnaround = models.CharField(max_length=20, blank=True, null=True)
    three_play_turnaround = models.CharField(max_length=20, blank=True, null=True)
    preferred_languages = models.TextField()
    video_source_language = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edxval_transcriptpreference'


class EdxvalVideo(models.Model):
    created = models.DateTimeField()
    edx_video_id = models.CharField(unique=True, max_length=100)
    client_video_id = models.CharField(max_length=255)
    duration = models.FloatField()
    status = models.CharField(max_length=255)
    error_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edxval_video'


class EdxvalVideoimage(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    image = models.CharField(max_length=500, blank=True, null=True)
    generated_images = models.TextField()
    course_video = models.ForeignKey(EdxvalCoursevideo, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'edxval_videoimage'


class EdxvalVideotranscript(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    transcript = models.CharField(max_length=255, blank=True, null=True)
    language_code = models.CharField(max_length=50)
    provider = models.CharField(max_length=30)
    file_format = models.CharField(max_length=20)
    video = models.ForeignKey(EdxvalVideo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edxval_videotranscript'
        unique_together = (('video', 'language_code'),)


class EmailMarketingEmailmarketingconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    sailthru_key = models.CharField(max_length=32)
    sailthru_secret = models.CharField(max_length=32)
    sailthru_new_user_list = models.CharField(max_length=48)
    sailthru_retry_interval = models.IntegerField()
    sailthru_max_retries = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    sailthru_abandoned_cart_delay = models.IntegerField()
    sailthru_abandoned_cart_template = models.CharField(max_length=20)
    sailthru_content_cache_age = models.IntegerField()
    sailthru_enroll_cost = models.IntegerField()
    sailthru_enroll_template = models.CharField(max_length=20)
    sailthru_get_tags_from_sailthru = models.IntegerField()
    sailthru_purchase_template = models.CharField(max_length=20)
    sailthru_upgrade_template = models.CharField(max_length=20)
    sailthru_lms_url_override = models.CharField(max_length=80)
    welcome_email_send_delay = models.IntegerField()
    user_registration_cookie_timeout_delay = models.FloatField()
    sailthru_welcome_template = models.CharField(max_length=20)
    sailthru_verification_failed_template = models.CharField(max_length=20)
    sailthru_verification_passed_template = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'email_marketing_emailmarketingconfiguration'


class EmbargoCountry(models.Model):
    country = models.CharField(unique=True, max_length=2)

    class Meta:
        managed = False
        db_table = 'embargo_country'


class EmbargoCountryaccessrule(models.Model):
    rule_type = models.CharField(max_length=255)
    country = models.ForeignKey(EmbargoCountry, models.DO_NOTHING)
    restricted_course = models.ForeignKey('EmbargoRestrictedcourse', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'embargo_countryaccessrule'
        unique_together = (('restricted_course', 'country'),)


class EmbargoCourseaccessrulehistory(models.Model):
    timestamp = models.DateTimeField()
    course_key = models.CharField(max_length=255)
    snapshot = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'embargo_courseaccessrulehistory'


class EmbargoEmbargoedcourse(models.Model):
    course_id = models.CharField(unique=True, max_length=255)
    embargoed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'embargo_embargoedcourse'


class EmbargoEmbargoedstate(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    embargoed_countries = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'embargo_embargoedstate'


class EmbargoIpfilter(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    whitelist = models.TextField()
    blacklist = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'embargo_ipfilter'


class EmbargoRestrictedcourse(models.Model):
    course_key = models.CharField(unique=True, max_length=255)
    enroll_msg_key = models.CharField(max_length=255)
    access_msg_key = models.CharField(max_length=255)
    disable_access_check = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'embargo_restrictedcourse'


class EnterpriseEnrollmentnotificationemailtemplate(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    plaintext_template = models.TextField()
    html_template = models.TextField()
    subject_line = models.CharField(max_length=100)
    enterprise_customer = models.ForeignKey('EnterpriseEnterprisecustomer', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'enterprise_enrollmentnotificationemailtemplate'


class EnterpriseEnterpriseanalyticsuser(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    analytics_user_id = models.CharField(max_length=255)
    enterprise_customer_user = models.ForeignKey('EnterpriseEnterprisecustomeruser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_enterpriseanalyticsuser'
        unique_together = (('enterprise_customer_user', 'analytics_user_id'),)


class EnterpriseEnterprisecatalogquery(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    content_filter = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecatalogquery'


class EnterpriseEnterprisecourseenrollment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    enterprise_customer_user = models.ForeignKey('EnterpriseEnterprisecustomeruser', models.DO_NOTHING)
    source = models.ForeignKey('EnterpriseEnterpriseenrollmentsource', models.DO_NOTHING, blank=True, null=True)
    saved_for_later = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecourseenrollment'
        unique_together = (('enterprise_customer_user', 'course_id'),)


class EnterpriseEnterprisecustomer(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=30)
    active = models.IntegerField()
    country = models.CharField(max_length=2, blank=True, null=True)
    hide_course_original_price = models.IntegerField()
    enable_data_sharing_consent = models.IntegerField()
    enforce_data_sharing_consent = models.CharField(max_length=25)
    enable_audit_enrollment = models.IntegerField()
    enable_audit_data_reporting = models.IntegerField()
    replace_sensitive_sso_username = models.IntegerField()
    enable_autocohorting = models.IntegerField()
    enable_portal_code_management_screen = models.IntegerField()
    enable_portal_reporting_config_screen = models.IntegerField()
    enable_portal_subscription_management_screen = models.IntegerField()
    enable_learner_portal = models.IntegerField()
    contact_email = models.CharField(max_length=254, blank=True, null=True)
    customer_type = models.ForeignKey('EnterpriseEnterprisecustomertype', models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)
    enable_slug_login = models.IntegerField()
    enable_portal_saml_configuration_screen = models.IntegerField()
    default_contract_discount = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    enable_analytics_screen = models.IntegerField()
    enable_integrated_customer_learner_portal_search = models.IntegerField()
    default_language = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomer'


class EnterpriseEnterprisecustomerbrandingconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    logo = models.CharField(max_length=255, blank=True, null=True)
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING, unique=True)
    primary_color = models.CharField(max_length=7, blank=True, null=True)
    secondary_color = models.CharField(max_length=7, blank=True, null=True)
    tertiary_color = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomerbrandingconfiguration'


class EnterpriseEnterprisecustomercatalog(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=255)
    content_filter = models.TextField(blank=True, null=True)
    enabled_course_modes = models.TextField()
    publish_audit_enrollment_urls = models.IntegerField()
    enterprise_catalog_query = models.ForeignKey(EnterpriseEnterprisecatalogquery, models.DO_NOTHING, blank=True, null=True)
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING)
    sync_enterprise_catalog_query = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomercatalog'


class EnterpriseEnterprisecustomeridentityprovider(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    provider_id = models.CharField(unique=True, max_length=50)
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomeridentityprovider'


class EnterpriseEnterprisecustomerreportingconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(unique=True, max_length=32)
    active = models.IntegerField()
    include_date = models.IntegerField()
    delivery_method = models.CharField(max_length=20)
    pgp_encryption_key = models.TextField(blank=True, null=True)
    data_type = models.CharField(max_length=20)
    report_type = models.CharField(max_length=20)
    email = models.TextField()
    frequency = models.CharField(max_length=20)
    day_of_month = models.SmallIntegerField(blank=True, null=True)
    day_of_week = models.SmallIntegerField(blank=True, null=True)
    hour_of_day = models.SmallIntegerField()
    decrypted_password = models.TextField(blank=True, null=True)
    sftp_hostname = models.CharField(max_length=256, blank=True, null=True)
    sftp_port = models.PositiveIntegerField(blank=True, null=True)
    sftp_username = models.CharField(max_length=256, blank=True, null=True)
    decrypted_sftp_password = models.TextField(blank=True, null=True)
    sftp_file_path = models.CharField(max_length=256, blank=True, null=True)
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomerreportingconfiguration'


class EnterpriseEnterprisecustomerreportingconfigurationEnterpricf00(models.Model):
    enterprisecustomerreportingconfiguration = models.ForeignKey(EnterpriseEnterprisecustomerreportingconfiguration, models.DO_NOTHING)
    enterprisecustomercatalog = models.ForeignKey(EnterpriseEnterprisecustomercatalog, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomerreportingconfiguration_enterpricf00'
        unique_together = (('enterprisecustomerreportingconfiguration', 'enterprisecustomercatalog'),)


class EnterpriseEnterprisecustomertype(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomertype'


class EnterpriseEnterprisecustomeruser(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_id = models.PositiveIntegerField()
    active = models.IntegerField()
    linked = models.IntegerField()
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisecustomeruser'
        unique_together = (('enterprise_customer', 'user_id'),)


class EnterpriseEnterpriseenrollmentsource(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=64)
    slug = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'enterprise_enterpriseenrollmentsource'


class EnterpriseEnterprisefeaturerole(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisefeaturerole'


class EnterpriseEnterprisefeatureuserroleassignment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    role = models.ForeignKey(EnterpriseEnterprisefeaturerole, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_enterprisefeatureuserroleassignment'


class EnterpriseHistoricalenrollmentnotificationemailtemplate(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    plaintext_template = models.TextField()
    html_template = models.TextField()
    subject_line = models.CharField(max_length=100)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_historicalenrollmentnotificationemailtemplate'


class EnterpriseHistoricalenterpriseanalyticsuser(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    analytics_user_id = models.CharField(max_length=255)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_user_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_historicalenterpriseanalyticsuser'


class EnterpriseHistoricalenterprisecourseenrollment(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_user_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    saved_for_later = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enterprise_historicalenterprisecourseenrollment'


class EnterpriseHistoricalenterprisecustomer(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=30)
    active = models.IntegerField()
    country = models.CharField(max_length=2, blank=True, null=True)
    hide_course_original_price = models.IntegerField()
    enable_data_sharing_consent = models.IntegerField()
    enforce_data_sharing_consent = models.CharField(max_length=25)
    enable_audit_enrollment = models.IntegerField()
    enable_audit_data_reporting = models.IntegerField()
    replace_sensitive_sso_username = models.IntegerField()
    enable_autocohorting = models.IntegerField()
    enable_portal_code_management_screen = models.IntegerField()
    enable_portal_reporting_config_screen = models.IntegerField()
    enable_portal_subscription_management_screen = models.IntegerField()
    enable_learner_portal = models.IntegerField()
    contact_email = models.CharField(max_length=254, blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    customer_type_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    site_id = models.IntegerField(blank=True, null=True)
    enable_slug_login = models.IntegerField()
    enable_portal_saml_configuration_screen = models.IntegerField()
    default_contract_discount = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    enable_analytics_screen = models.IntegerField()
    enable_integrated_customer_learner_portal_search = models.IntegerField()
    default_language = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_historicalenterprisecustomer'


class EnterpriseHistoricalenterprisecustomercatalog(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(max_length=32)
    title = models.CharField(max_length=255)
    content_filter = models.TextField(blank=True, null=True)
    enabled_course_modes = models.TextField()
    publish_audit_enrollment_urls = models.IntegerField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_catalog_query_id = models.IntegerField(blank=True, null=True)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    sync_enterprise_catalog_query = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enterprise_historicalenterprisecustomercatalog'


class EnterpriseHistoricallicensedenterprisecourseenrollment(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    license_uuid = models.CharField(max_length=32)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_course_enrollment_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    is_revoked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enterprise_historicallicensedenterprisecourseenrollment'


class EnterpriseHistoricalpendingenrollment(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    course_mode = models.CharField(max_length=25)
    cohort_name = models.CharField(max_length=255, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=8, decimal_places=5)
    sales_force_id = models.CharField(max_length=255, blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_historicalpendingenrollment'


class EnterpriseHistoricalpendingenterprisecustomeradminuser(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_email = models.CharField(max_length=254)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_historicalpendingenterprisecustomeradminuser'


class EnterpriseHistoricalpendingenterprisecustomeruser(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_email = models.CharField(max_length=254)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_historicalpendingenterprisecustomeruser'


class EnterpriseLicensedenterprisecourseenrollment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    license_uuid = models.CharField(max_length=32)
    enterprise_course_enrollment = models.ForeignKey(EnterpriseEnterprisecourseenrollment, models.DO_NOTHING, unique=True)
    is_revoked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enterprise_licensedenterprisecourseenrollment'


class EnterprisePendingenrollment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    course_mode = models.CharField(max_length=25)
    cohort_name = models.CharField(max_length=255, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=8, decimal_places=5)
    sales_force_id = models.CharField(max_length=255, blank=True, null=True)
    source = models.ForeignKey(EnterpriseEnterpriseenrollmentsource, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('EnterprisePendingenterprisecustomeruser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_pendingenrollment'
        unique_together = (('user', 'course_id'),)


class EnterprisePendingenterprisecustomeradminuser(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_email = models.CharField(max_length=254)
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_pendingenterprisecustomeradminuser'
        unique_together = (('enterprise_customer', 'user_email'),)


class EnterprisePendingenterprisecustomeruser(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_email = models.CharField(unique=True, max_length=254)
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_pendingenterprisecustomeruser'


class EnterpriseSystemwideenterpriserole(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enterprise_systemwideenterpriserole'


class EnterpriseSystemwideenterpriseuserroleassignment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    role = models.ForeignKey(EnterpriseSystemwideenterpriserole, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enterprise_systemwideenterpriseuserroleassignment'


class EntitlementsCourseentitlement(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(unique=True, max_length=32)
    course_uuid = models.CharField(max_length=32)
    expired_at = models.DateTimeField(blank=True, null=True)
    mode = models.CharField(max_length=100)
    order_number = models.CharField(max_length=128, blank=True, null=True)
    enrollment_course_run = models.ForeignKey('StudentCourseenrollment', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    field_policy = models.ForeignKey('EntitlementsCourseentitlementpolicy', models.DO_NOTHING, db_column='_policy_id', blank=True, null=True)  # Field renamed because it started with '_'.
    refund_locked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'entitlements_courseentitlement'
        unique_together = (('course_uuid', 'order_number'),)


class EntitlementsCourseentitlementpolicy(models.Model):
    expiration_period = models.BigIntegerField()
    refund_period = models.BigIntegerField()
    regain_period = models.BigIntegerField()
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING, blank=True, null=True)
    mode = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entitlements_courseentitlementpolicy'


class EntitlementsCourseentitlementsupportdetail(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reason = models.CharField(max_length=15)
    comments = models.TextField(blank=True, null=True)
    entitlement = models.ForeignKey(EntitlementsCourseentitlement, models.DO_NOTHING)
    support_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    unenrolled_run_id = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'entitlements_courseentitlementsupportdetail'


class EntitlementsHistoricalcourseentitlement(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(max_length=32)
    course_uuid = models.CharField(max_length=32)
    expired_at = models.DateTimeField(blank=True, null=True)
    mode = models.CharField(max_length=100)
    order_number = models.CharField(max_length=128, blank=True, null=True)
    refund_locked = models.IntegerField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    field_policy_id = models.IntegerField(db_column='_policy_id', blank=True, null=True)  # Field renamed because it started with '_'.
    enrollment_course_run_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entitlements_historicalcourseentitlement'


class EntitlementsHistoricalcourseentitlementsupportdetail(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reason = models.CharField(max_length=15)
    action = models.CharField(max_length=15)
    comments = models.TextField(blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    entitlement_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    support_user_id = models.IntegerField(blank=True, null=True)
    unenrolled_run_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entitlements_historicalcourseentitlementsupportdetail'


class ExperimentsExperimentdata(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    experiment_id = models.PositiveSmallIntegerField()
    key = models.CharField(max_length=255)
    value = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'experiments_experimentdata'
        unique_together = (('user', 'experiment_id', 'key'),)


class ExperimentsExperimentkeyvalue(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    experiment_id = models.PositiveSmallIntegerField()
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'experiments_experimentkeyvalue'
        unique_together = (('experiment_id', 'key'),)


class ExperimentsHistoricalexperimentkeyvalue(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    experiment_id = models.PositiveSmallIntegerField()
    key = models.CharField(max_length=255)
    value = models.TextField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiments_historicalexperimentkeyvalue'


class ExternalUserIdsExternalid(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_user_id = models.CharField(unique=True, max_length=32)
    external_id_type = models.ForeignKey('ExternalUserIdsExternalidtype', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'external_user_ids_externalid'
        unique_together = (('user', 'external_id_type'),)


class ExternalUserIdsExternalidtype(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=32)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'external_user_ids_externalidtype'


class ExternalUserIdsHistoricalexternalid(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_user_id = models.CharField(max_length=32)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    external_id_type_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'external_user_ids_historicalexternalid'


class ExternalUserIdsHistoricalexternalidtype(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=32)
    description = models.TextField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'external_user_ids_historicalexternalidtype'


class GradesComputegradessetting(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    batch_size = models.IntegerField()
    course_ids = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades_computegradessetting'


class GradesCoursepersistentgradesflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    course_id = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades_coursepersistentgradesflag'


class GradesHistoricalpersistentsubsectiongradeoverride(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    earned_all_override = models.FloatField(blank=True, null=True)
    possible_all_override = models.FloatField(blank=True, null=True)
    earned_graded_override = models.FloatField(blank=True, null=True)
    possible_graded_override = models.FloatField(blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    grade_id = models.BigIntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    override_reason = models.CharField(max_length=300, blank=True, null=True)
    system = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades_historicalpersistentsubsectiongradeoverride'


class GradesPersistentcoursegrade(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    course_id = models.CharField(max_length=255)
    course_edited_timestamp = models.DateTimeField(blank=True, null=True)
    course_version = models.CharField(max_length=255)
    grading_policy_hash = models.CharField(max_length=255)
    percent_grade = models.FloatField()
    letter_grade = models.CharField(max_length=255)
    passed_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades_persistentcoursegrade'
        unique_together = (('course_id', 'user_id'),)


class GradesPersistentgradesenabledflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    enabled_for_all_courses = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades_persistentgradesenabledflag'


class GradesPersistentsubsectiongrade(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    course_id = models.CharField(max_length=255)
    usage_key = models.CharField(max_length=255)
    subtree_edited_timestamp = models.DateTimeField(blank=True, null=True)
    course_version = models.CharField(max_length=255)
    earned_all = models.FloatField()
    possible_all = models.FloatField()
    earned_graded = models.FloatField()
    possible_graded = models.FloatField()
    visible_blocks_hash = models.ForeignKey('GradesVisibleblocks', models.DO_NOTHING, db_column='visible_blocks_hash')
    first_attempted = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades_persistentsubsectiongrade'
        unique_together = (('course_id', 'user_id', 'usage_key'),)


class GradesPersistentsubsectiongradeoverride(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    earned_all_override = models.FloatField(blank=True, null=True)
    possible_all_override = models.FloatField(blank=True, null=True)
    earned_graded_override = models.FloatField(blank=True, null=True)
    possible_graded_override = models.FloatField(blank=True, null=True)
    grade = models.ForeignKey(GradesPersistentsubsectiongrade, models.DO_NOTHING, unique=True)
    override_reason = models.CharField(max_length=300, blank=True, null=True)
    system = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades_persistentsubsectiongradeoverride'


class GradesVisibleblocks(models.Model):
    blocks_json = models.TextField()
    hashed = models.CharField(unique=True, max_length=100)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'grades_visibleblocks'


class InstructorTaskGradereportsetting(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    batch_size = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor_task_gradereportsetting'


class InstructorTaskInstructortask(models.Model):
    task_type = models.CharField(max_length=50)
    course_id = models.CharField(max_length=255)
    task_key = models.CharField(max_length=255)
    task_input = models.TextField()
    task_id = models.CharField(max_length=255)
    task_state = models.CharField(max_length=50, blank=True, null=True)
    task_output = models.CharField(max_length=1024, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField()
    subtasks = models.TextField()
    requester = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instructor_task_instructortask'


class IntegratedChannelContentmetadataitemtransmission(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    integrated_channel_code = models.CharField(max_length=30)
    content_id = models.CharField(max_length=255)
    channel_metadata = models.TextField()
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'integrated_channel_contentmetadataitemtransmission'
        unique_together = (('enterprise_customer', 'integrated_channel_code', 'content_id'),)


class IntegratedChannelLearnerdatatransmissionaudit(models.Model):
    enterprise_course_enrollment_id = models.PositiveIntegerField()
    course_id = models.CharField(max_length=255)
    course_completed = models.IntegerField()
    completed_timestamp = models.BigIntegerField()
    instructor_name = models.CharField(max_length=255)
    grade = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    error_message = models.TextField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'integrated_channel_learnerdatatransmissionaudit'


class LearningSequencesCoursecontext(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    learning_context = models.ForeignKey('LearningSequencesLearningcontext', models.DO_NOTHING, primary_key=True)
    course_visibility = models.CharField(max_length=32)
    self_paced = models.IntegerField()
    days_early_for_beta = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'learning_sequences_coursecontext'


class LearningSequencesCoursesection(models.Model):
    id = models.BigAutoField(primary_key=True)
    ordering = models.PositiveIntegerField()
    usage_key = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=1000)
    hide_from_toc = models.IntegerField()
    visible_to_staff_only = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_context = models.ForeignKey(LearningSequencesCoursecontext, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'learning_sequences_coursesection'
        unique_together = (('course_context', 'usage_key'),)


class LearningSequencesCoursesectionsequence(models.Model):
    id = models.BigAutoField(primary_key=True)
    ordering = models.PositiveIntegerField()
    hide_from_toc = models.IntegerField()
    visible_to_staff_only = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    section = models.ForeignKey(LearningSequencesCoursesection, models.DO_NOTHING)
    sequence = models.ForeignKey('LearningSequencesLearningsequence', models.DO_NOTHING)
    inaccessible_after_due = models.IntegerField()
    course_context = models.ForeignKey(LearningSequencesCoursecontext, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'learning_sequences_coursesectionsequence'
        unique_together = (('course_context', 'ordering'),)


class LearningSequencesLearningcontext(models.Model):
    id = models.BigAutoField(primary_key=True)
    context_key = models.CharField(unique=True, max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    published_version = models.CharField(max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'learning_sequences_learningcontext'


class LearningSequencesLearningsequence(models.Model):
    id = models.BigAutoField(primary_key=True)
    learning_context = models.ForeignKey(LearningSequencesLearningcontext, models.DO_NOTHING)
    usage_key = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=1000)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'learning_sequences_learningsequence'
        unique_together = (('learning_context', 'usage_key'),)


class LmsXblockXblockasidesconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    disabled_blocks = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lms_xblock_xblockasidesconfig'


class LtiConsumerLtiagslineitem(models.Model):
    resource_id = models.CharField(max_length=100)
    resource_link_id = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=100)
    score_maximum = models.IntegerField()
    tag = models.CharField(max_length=50)
    start_date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    lti_configuration = models.ForeignKey('LtiConsumerLticonfiguration', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lti_consumer_ltiagslineitem'


class LtiConsumerLtiagsscore(models.Model):
    timestamp = models.DateTimeField()
    score_given = models.FloatField(blank=True, null=True)
    score_maximum = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    activity_progress = models.CharField(max_length=20)
    grading_progress = models.CharField(max_length=20)
    user_id = models.CharField(max_length=255)
    line_item = models.ForeignKey(LtiConsumerLtiagslineitem, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lti_consumer_ltiagsscore'
        unique_together = (('line_item', 'user_id'),)


class LtiConsumerLticonfiguration(models.Model):
    version = models.CharField(max_length=10)
    config_store = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    lti_1p3_internal_private_key = models.TextField()
    lti_1p3_internal_private_key_id = models.CharField(max_length=255)
    lti_1p3_internal_public_jwk = models.TextField()
    lti_1p3_client_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'lti_consumer_lticonfiguration'


class MilestonesCoursecontentmilestone(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    content_id = models.CharField(max_length=255)
    active = models.IntegerField()
    milestone = models.ForeignKey('MilestonesMilestone', models.DO_NOTHING)
    milestone_relationship_type = models.ForeignKey('MilestonesMilestonerelationshiptype', models.DO_NOTHING)
    requirements = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'milestones_coursecontentmilestone'
        unique_together = (('course_id', 'content_id', 'milestone'),)


class MilestonesCoursemilestone(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    active = models.IntegerField()
    milestone = models.ForeignKey('MilestonesMilestone', models.DO_NOTHING)
    milestone_relationship_type = models.ForeignKey('MilestonesMilestonerelationshiptype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'milestones_coursemilestone'
        unique_together = (('course_id', 'milestone'),)


class MilestonesMilestone(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    namespace = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    description = models.TextField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'milestones_milestone'
        unique_together = (('namespace', 'name'),)


class MilestonesMilestonerelationshiptype(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=25)
    description = models.TextField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'milestones_milestonerelationshiptype'


class MilestonesUsermilestone(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_id = models.IntegerField()
    source = models.TextField()
    collected = models.DateTimeField(blank=True, null=True)
    active = models.IntegerField()
    milestone = models.ForeignKey(MilestonesMilestone, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'milestones_usermilestone'
        unique_together = (('user_id', 'milestone'),)


class MobileApiAppversionconfig(models.Model):
    platform = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    major_version = models.IntegerField()
    minor_version = models.IntegerField()
    patch_version = models.IntegerField()
    expire_at = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mobile_api_appversionconfig'
        unique_together = (('platform', 'version'),)


class MobileApiIgnoremobileavailableflagconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mobile_api_ignoremobileavailableflagconfig'


class MobileApiMobileapiconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    video_profiles = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mobile_api_mobileapiconfig'


class MoodleHistoricalmoodleenterprisecustomerconfiguration(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)
    moodle_base_url = models.CharField(max_length=255)
    service_short_name = models.CharField(max_length=255)
    category_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enterprise_customer_id = models.CharField(max_length=32, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moodle_historicalmoodleenterprisecustomerconfiguration'


class MoodleMoodleenterprisecustomerconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)
    moodle_base_url = models.CharField(max_length=255)
    service_short_name = models.CharField(max_length=255)
    category_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'moodle_moodleenterprisecustomerconfiguration'


class MoodleMoodlelearnerdatatransmissionaudit(models.Model):
    moodle_user_email = models.CharField(max_length=255)
    enterprise_course_enrollment_id = models.PositiveIntegerField()
    course_id = models.CharField(max_length=255)
    grade = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    total_hours = models.FloatField(blank=True, null=True)
    course_completed = models.IntegerField()
    completed_timestamp = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    error_message = models.TextField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'moodle_moodlelearnerdatatransmissionaudit'


class NotifyNotification(models.Model):
    message = models.TextField()
    url = models.CharField(max_length=200, blank=True, null=True)
    is_viewed = models.IntegerField()
    is_emailed = models.IntegerField()
    created = models.DateTimeField()
    subscription = models.ForeignKey('NotifySubscription', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notify_notification'


class NotifyNotificationtype(models.Model):
    key = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, blank=True, null=True)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notify_notificationtype'


class NotifySettings(models.Model):
    interval = models.SmallIntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notify_settings'


class NotifySubscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    object_id = models.CharField(max_length=64, blank=True, null=True)
    send_emails = models.IntegerField()
    notification_type = models.ForeignKey(NotifyNotificationtype, models.DO_NOTHING)
    settings = models.ForeignKey(NotifySettings, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notify_subscription'


class Oauth2ProviderAccesstoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    scope = models.TextField()
    application = models.ForeignKey('Oauth2ProviderApplication', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    source_refresh_token = models.ForeignKey('Oauth2ProviderRefreshtoken', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_accesstoken'


class Oauth2ProviderApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(unique=True, max_length=100)
    redirect_uris = models.TextField()
    client_type = models.CharField(max_length=32)
    authorization_grant_type = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    skip_authorization = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_application'


class Oauth2ProviderGrant(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.CharField(max_length=255)
    scope = models.TextField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    code_challenge = models.CharField(max_length=128)
    code_challenge_method = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_grant'


class Oauth2ProviderRefreshtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=255)
    access_token = models.ForeignKey(Oauth2ProviderAccesstoken, models.DO_NOTHING, unique=True, blank=True, null=True)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    revoked = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_refreshtoken'
        unique_together = (('token', 'revoked'),)


class OauthDispatchApplicationaccess(models.Model):
    scopes = models.CharField(max_length=825)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING, unique=True)
    filters = models.CharField(max_length=825, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_dispatch_applicationaccess'


class OauthDispatchApplicationorganization(models.Model):
    relation_type = models.CharField(max_length=32)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    organization = models.ForeignKey('OrganizationsOrganization', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'oauth_dispatch_applicationorganization'
        unique_together = (('application', 'relation_type', 'organization'),)


class OauthDispatchRestrictedapplication(models.Model):
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'oauth_dispatch_restrictedapplication'


class OrganizationsHistoricalorganization(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    active = models.IntegerField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organizations_historicalorganization'


class OrganizationsOrganization(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'organizations_organization'


class OrganizationsOrganizationcourse(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    active = models.IntegerField()
    organization = models.ForeignKey(OrganizationsOrganization, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organizations_organizationcourse'
        unique_together = (('course_id', 'organization'),)


class ProctoringProctoredexam(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    content_id = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    exam_name = models.TextField()
    time_limit_mins = models.IntegerField()
    due_date = models.DateTimeField(blank=True, null=True)
    is_proctored = models.IntegerField()
    is_practice_exam = models.IntegerField()
    is_active = models.IntegerField()
    hide_after_due = models.IntegerField()
    backend = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexam'
        unique_together = (('course_id', 'content_id'),)


class ProctoringProctoredexamreviewpolicy(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    review_policy = models.TextField()
    proctored_exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING)
    set_by_user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamreviewpolicy'


class ProctoringProctoredexamreviewpolicyhistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    original_id = models.IntegerField()
    review_policy = models.TextField()
    proctored_exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING)
    set_by_user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamreviewpolicyhistory'


class ProctoringProctoredexamsoftwaresecurereview(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    attempt_code = models.CharField(unique=True, max_length=255)
    review_status = models.CharField(max_length=255)
    raw_data = models.TextField()
    video_url = models.TextField()
    exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING, blank=True, null=True)
    reviewed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamsoftwaresecurereview'


class ProctoringProctoredexamsoftwaresecurereviewhistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    attempt_code = models.CharField(max_length=255)
    review_status = models.CharField(max_length=255)
    raw_data = models.TextField()
    video_url = models.TextField()
    exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING, blank=True, null=True)
    reviewed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamsoftwaresecurereviewhistory'


class ProctoringProctoredexamstudentallowance(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    proctored_exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamstudentallowance'
        unique_together = (('user', 'proctored_exam', 'key'),)


class ProctoringProctoredexamstudentallowancehistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    allowance_id = models.IntegerField()
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    proctored_exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamstudentallowancehistory'


class ProctoringProctoredexamstudentattempt(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_poll_timestamp = models.DateTimeField(blank=True, null=True)
    last_poll_ipaddr = models.CharField(max_length=32, blank=True, null=True)
    attempt_code = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    allowed_time_limit_mins = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=64)
    taking_as_proctored = models.IntegerField()
    is_sample_attempt = models.IntegerField()
    student_name = models.CharField(max_length=255)
    review_policy_id = models.IntegerField(blank=True, null=True)
    proctored_exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    is_status_acknowledged = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamstudentattempt'
        unique_together = (('user', 'proctored_exam'),)


class ProctoringProctoredexamstudentattemptcomment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_time = models.IntegerField()
    stop_time = models.IntegerField()
    duration = models.IntegerField()
    comment = models.TextField()
    status = models.CharField(max_length=255)
    review = models.ForeignKey(ProctoringProctoredexamsoftwaresecurereview, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamstudentattemptcomment'


class ProctoringProctoredexamstudentattempthistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    attempt_id = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    attempt_code = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    allowed_time_limit_mins = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=64)
    taking_as_proctored = models.IntegerField()
    is_sample_attempt = models.IntegerField()
    student_name = models.CharField(max_length=255)
    review_policy_id = models.IntegerField(blank=True, null=True)
    last_poll_timestamp = models.DateTimeField(blank=True, null=True)
    last_poll_ipaddr = models.CharField(max_length=32, blank=True, null=True)
    proctored_exam = models.ForeignKey(ProctoringProctoredexam, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proctoring_proctoredexamstudentattempthistory'


class ProgramEnrollmentsCourseaccessroleassignment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    role = models.CharField(max_length=64)
    enrollment = models.ForeignKey('ProgramEnrollmentsProgramcourseenrollment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'program_enrollments_courseaccessroleassignment'
        unique_together = (('role', 'enrollment'),)


class ProgramEnrollmentsHistoricalprogramcourseenrollment(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_key = models.CharField(max_length=255)
    status = models.CharField(max_length=9)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    course_enrollment_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    program_enrollment_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'program_enrollments_historicalprogramcourseenrollment'


class ProgramEnrollmentsHistoricalprogramenrollment(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_user_key = models.CharField(max_length=255, blank=True, null=True)
    program_uuid = models.CharField(max_length=32)
    curriculum_uuid = models.CharField(max_length=32)
    status = models.CharField(max_length=9)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'program_enrollments_historicalprogramenrollment'


class ProgramEnrollmentsProgramcourseenrollment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_key = models.CharField(max_length=255)
    status = models.CharField(max_length=9)
    course_enrollment = models.ForeignKey('StudentCourseenrollment', models.DO_NOTHING, blank=True, null=True)
    program_enrollment = models.ForeignKey('ProgramEnrollmentsProgramenrollment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'program_enrollments_programcourseenrollment'
        unique_together = (('program_enrollment', 'course_key'),)


class ProgramEnrollmentsProgramenrollment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_user_key = models.CharField(max_length=255, blank=True, null=True)
    program_uuid = models.CharField(max_length=32)
    curriculum_uuid = models.CharField(max_length=32)
    status = models.CharField(max_length=9)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'program_enrollments_programenrollment'
        unique_together = (('external_user_key', 'program_uuid', 'curriculum_uuid'), ('user', 'program_uuid', 'curriculum_uuid'),)


class ProgramsCustomprogramsconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    arguments = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programs_customprogramsconfig'


class ProgramsProgramsapiconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    marketing_path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'programs_programsapiconfig'


class RssProxyWhitelistedrssurl(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    url = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'rss_proxy_whitelistedrssurl'


class SapSuccessFactorsSapsuccessfactorsenterprisecustomerconfidb8A(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    transmission_chunk_size = models.IntegerField()
    channel_worker_username = models.CharField(max_length=255, blank=True, null=True)
    catalogs_to_transmit = models.TextField(blank=True, null=True)
    key = models.CharField(max_length=255)
    sapsf_base_url = models.CharField(max_length=255)
    sapsf_company_id = models.CharField(max_length=255)
    sapsf_user_id = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20)
    additional_locales = models.TextField()
    show_course_price = models.IntegerField()
    transmit_total_hours = models.IntegerField()
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'sap_success_factors_sapsuccessfactorsenterprisecustomerconfidb8a'


class SapSuccessFactorsSapsuccessfactorsglobalconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    completion_status_api_path = models.CharField(max_length=255)
    course_api_path = models.CharField(max_length=255)
    oauth_api_path = models.CharField(max_length=255)
    search_student_api_path = models.CharField(max_length=255)
    provider_id = models.CharField(max_length=100)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sap_success_factors_sapsuccessfactorsglobalconfiguration'


class SapSuccessFactorsSapsuccessfactorslearnerdatatransmission3Ce5(models.Model):
    sapsf_user_id = models.CharField(max_length=255)
    enterprise_course_enrollment_id = models.PositiveIntegerField()
    course_id = models.CharField(max_length=255)
    course_completed = models.IntegerField()
    instructor_name = models.CharField(max_length=255)
    grade = models.CharField(max_length=100)
    total_hours = models.FloatField(blank=True, null=True)
    completed_timestamp = models.BigIntegerField()
    status = models.CharField(max_length=100)
    error_message = models.TextField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sap_success_factors_sapsuccessfactorslearnerdatatransmission3ce5'


class SchedulesHistoricalschedule(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    upgrade_deadline = models.DateTimeField(blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enrollment_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedules_historicalschedule'


class SchedulesSchedule(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    upgrade_deadline = models.DateTimeField(blank=True, null=True)
    enrollment = models.ForeignKey('StudentCourseenrollment', models.DO_NOTHING, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedules_schedule'


class SchedulesScheduleconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    create_schedules = models.IntegerField()
    enqueue_recurring_nudge = models.IntegerField()
    deliver_recurring_nudge = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)
    deliver_upgrade_reminder = models.IntegerField()
    enqueue_upgrade_reminder = models.IntegerField()
    deliver_course_update = models.IntegerField()
    enqueue_course_update = models.IntegerField()
    hold_back_ratio = models.FloatField()

    class Meta:
        managed = False
        db_table = 'schedules_scheduleconfig'


class SchedulesScheduleexperience(models.Model):
    experience_type = models.PositiveSmallIntegerField()
    schedule = models.ForeignKey(SchedulesSchedule, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'schedules_scheduleexperience'


class SelfPacedSelfpacedconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    enable_course_home_improvements = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'self_paced_selfpacedconfiguration'


class ShoppingcartCertificateitem(models.Model):
    orderitem_ptr = models.ForeignKey('ShoppingcartOrderitem', models.DO_NOTHING, primary_key=True)
    course_id = models.CharField(max_length=128)
    mode = models.CharField(max_length=50)
    course_enrollment = models.ForeignKey('StudentCourseenrollment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_certificateitem'


class ShoppingcartCoupon(models.Model):
    code = models.CharField(max_length=32)
    description = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.CharField(max_length=255)
    percentage_discount = models.IntegerField()
    created_at = models.DateTimeField()
    is_active = models.IntegerField()
    expiration_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_coupon'


class ShoppingcartCouponredemption(models.Model):
    coupon = models.ForeignKey(ShoppingcartCoupon, models.DO_NOTHING)
    order = models.ForeignKey('ShoppingcartOrder', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_couponredemption'


class ShoppingcartCourseregcodeitem(models.Model):
    orderitem_ptr = models.ForeignKey('ShoppingcartOrderitem', models.DO_NOTHING, primary_key=True)
    course_id = models.CharField(max_length=128)
    mode = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'shoppingcart_courseregcodeitem'


class ShoppingcartCourseregcodeitemannotation(models.Model):
    course_id = models.CharField(unique=True, max_length=128)
    annotation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_courseregcodeitemannotation'


class ShoppingcartCourseregistrationcode(models.Model):
    code = models.CharField(unique=True, max_length=32)
    course_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    mode_slug = models.CharField(max_length=100, blank=True, null=True)
    is_valid = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    invoice = models.ForeignKey('ShoppingcartInvoice', models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey('ShoppingcartOrder', models.DO_NOTHING, blank=True, null=True)
    invoice_item = models.ForeignKey('ShoppingcartCourseregistrationcodeinvoiceitem', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_courseregistrationcode'


class ShoppingcartCourseregistrationcodeinvoiceitem(models.Model):
    invoiceitem_ptr = models.ForeignKey('ShoppingcartInvoiceitem', models.DO_NOTHING, primary_key=True)
    course_id = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'shoppingcart_courseregistrationcodeinvoiceitem'


class ShoppingcartDonation(models.Model):
    orderitem_ptr = models.ForeignKey('ShoppingcartOrderitem', models.DO_NOTHING, primary_key=True)
    donation_type = models.CharField(max_length=32)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'shoppingcart_donation'


class ShoppingcartDonationconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_donationconfiguration'


class ShoppingcartInvoice(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    company_name = models.CharField(max_length=255)
    company_contact_name = models.CharField(max_length=255)
    company_contact_email = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255)
    recipient_email = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    address_line_3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    total_amount = models.FloatField()
    course_id = models.CharField(max_length=255)
    internal_reference = models.CharField(max_length=255, blank=True, null=True)
    customer_reference_number = models.CharField(max_length=63, blank=True, null=True)
    is_valid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shoppingcart_invoice'


class ShoppingcartInvoicehistory(models.Model):
    timestamp = models.DateTimeField()
    snapshot = models.TextField()
    invoice = models.ForeignKey(ShoppingcartInvoice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_invoicehistory'


class ShoppingcartInvoiceitem(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=30, decimal_places=2)
    currency = models.CharField(max_length=8)
    invoice = models.ForeignKey(ShoppingcartInvoice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_invoiceitem'


class ShoppingcartInvoicetransaction(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    currency = models.CharField(max_length=8)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    invoice = models.ForeignKey(ShoppingcartInvoice, models.DO_NOTHING)
    last_modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_invoicetransaction'


class ShoppingcartOrder(models.Model):
    currency = models.CharField(max_length=8)
    status = models.CharField(max_length=32)
    purchase_time = models.DateTimeField(blank=True, null=True)
    refunded_time = models.DateTimeField(blank=True, null=True)
    bill_to_first = models.CharField(max_length=64)
    bill_to_last = models.CharField(max_length=64)
    bill_to_street1 = models.CharField(max_length=128)
    bill_to_street2 = models.CharField(max_length=128)
    bill_to_city = models.CharField(max_length=64)
    bill_to_state = models.CharField(max_length=8)
    bill_to_postalcode = models.CharField(max_length=16)
    bill_to_country = models.CharField(max_length=64)
    bill_to_ccnum = models.CharField(max_length=8)
    bill_to_cardtype = models.CharField(max_length=32)
    processor_reply_dump = models.TextField()
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_contact_name = models.CharField(max_length=255, blank=True, null=True)
    company_contact_email = models.CharField(max_length=255, blank=True, null=True)
    recipient_name = models.CharField(max_length=255, blank=True, null=True)
    recipient_email = models.CharField(max_length=255, blank=True, null=True)
    customer_reference_number = models.CharField(max_length=63, blank=True, null=True)
    order_type = models.CharField(max_length=32)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_order'


class ShoppingcartOrderitem(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=32)
    qty = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=30, decimal_places=2)
    list_price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    line_desc = models.CharField(max_length=1024)
    currency = models.CharField(max_length=8)
    fulfilled_time = models.DateTimeField(blank=True, null=True)
    refund_requested_time = models.DateTimeField(blank=True, null=True)
    service_fee = models.DecimalField(max_digits=30, decimal_places=2)
    report_comments = models.TextField()
    order = models.ForeignKey(ShoppingcartOrder, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_orderitem'


class ShoppingcartPaidcourseregistration(models.Model):
    orderitem_ptr = models.ForeignKey(ShoppingcartOrderitem, models.DO_NOTHING, primary_key=True)
    course_id = models.CharField(max_length=128)
    mode = models.CharField(max_length=50)
    course_enrollment = models.ForeignKey('StudentCourseenrollment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_paidcourseregistration'


class ShoppingcartPaidcourseregistrationannotation(models.Model):
    course_id = models.CharField(unique=True, max_length=128)
    annotation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_paidcourseregistrationannotation'


class ShoppingcartRegistrationcoderedemption(models.Model):
    redeemed_at = models.DateTimeField(blank=True, null=True)
    course_enrollment = models.ForeignKey('StudentCourseenrollment', models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey(ShoppingcartOrder, models.DO_NOTHING, blank=True, null=True)
    redeemed_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    registration_code = models.ForeignKey(ShoppingcartCourseregistrationcode, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoppingcart_registrationcoderedemption'


class SiteConfigurationSiteconfiguration(models.Model):
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING, unique=True)
    enabled = models.IntegerField()
    site_values = models.TextField()

    class Meta:
        managed = False
        db_table = 'site_configuration_siteconfiguration'


class SiteConfigurationSiteconfigurationhistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)
    enabled = models.IntegerField()
    site_values = models.TextField()

    class Meta:
        managed = False
        db_table = 'site_configuration_siteconfigurationhistory'


class SocialAuthAssociation(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class SocialAuthCode(models.Model):
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthPartial(models.Model):
    token = models.CharField(max_length=32)
    next_step = models.PositiveSmallIntegerField()
    backend = models.CharField(max_length=32)
    data = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)


class SplashSplashconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    cookie_name = models.TextField()
    cookie_allowed_values = models.TextField()
    unaffected_usernames = models.TextField()
    unaffected_url_paths = models.TextField()
    redirect_url = models.CharField(max_length=200)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'splash_splashconfig'


class StaticReplaceAssetbaseurlconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    base_url = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'static_replace_assetbaseurlconfig'


class StaticReplaceAssetexcludedextensionsconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    excluded_extensions = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'static_replace_assetexcludedextensionsconfig'


class StatusCoursemessage(models.Model):
    course_key = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    global_message = models.ForeignKey('StatusGlobalstatusmessage', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'status_coursemessage'


class StatusGlobalstatusmessage(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status_globalstatusmessage'


class StudentAccountrecoveryconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    csv_file = models.CharField(max_length=100)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_accountrecoveryconfiguration'


class StudentAllowedauthuser(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_allowedauthuser'


class StudentAnonymoususerid(models.Model):
    anonymous_user_id = models.CharField(unique=True, max_length=32)
    course_id = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_anonymoususerid'


class StudentBulkchangeenrollmentconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    csv_file = models.CharField(max_length=100)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_bulkchangeenrollmentconfiguration'


class StudentBulkunenrollconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    csv_file = models.CharField(max_length=100)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_bulkunenrollconfiguration'


class StudentCourseaccessrole(models.Model):
    org = models.CharField(max_length=64)
    course_id = models.CharField(max_length=255)
    role = models.CharField(max_length=64)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_courseaccessrole'
        unique_together = (('user', 'org', 'course_id', 'role'),)


class StudentCourseenrollment(models.Model):
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()
    mode = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_courseenrollment'
        unique_together = (('user', 'course_id'),)


class StudentCourseenrollmentHistory(models.Model):
    id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()
    mode = models.CharField(max_length=100)
    history_id = models.CharField(primary_key=True, max_length=32)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    course_id = models.CharField(max_length=255, blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_courseenrollment_history'


class StudentCourseenrollmentallowed(models.Model):
    email = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    auto_enroll = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_courseenrollmentallowed'
        unique_together = (('email', 'course_id'),)


class StudentCourseenrollmentattribute(models.Model):
    namespace = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    enrollment = models.ForeignKey(StudentCourseenrollment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_courseenrollmentattribute'


class StudentCourseenrollmentcelebration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    celebrate_first_section = models.IntegerField()
    enrollment = models.ForeignKey(StudentCourseenrollment, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'student_courseenrollmentcelebration'


class StudentDashboardconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    recent_enrollment_time_delta = models.PositiveIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_dashboardconfiguration'


class StudentEnrollmentrefundconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    refund_window_microseconds = models.BigIntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_enrollmentrefundconfiguration'


class StudentEntranceexamconfiguration(models.Model):
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField()
    skip_entrance_exam = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_entranceexamconfiguration'
        unique_together = (('user', 'course_id'),)


class StudentFbeenrollmentexclusion(models.Model):
    enrollment = models.ForeignKey(StudentCourseenrollment, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'student_fbeenrollmentexclusion'


class StudentHistoricalmanualenrollmentaudit(models.Model):
    id = models.IntegerField()
    enrolled_email = models.CharField(max_length=255)
    time_stamp = models.DateTimeField(blank=True, null=True)
    state_transition = models.CharField(max_length=255)
    reason = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=64, blank=True, null=True)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    enrolled_by_id = models.IntegerField(blank=True, null=True)
    enrollment_id = models.IntegerField(blank=True, null=True)
    history_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_historicalmanualenrollmentaudit'


class StudentLanguageproficiency(models.Model):
    code = models.CharField(max_length=16)
    user_profile = models.ForeignKey(AuthUserprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_languageproficiency'
        unique_together = (('code', 'user_profile'),)


class StudentLinkedinaddtoprofileconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    company_identifier = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_linkedinaddtoprofileconfiguration'


class StudentLoginfailures(models.Model):
    failure_count = models.IntegerField()
    lockout_until = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_loginfailures'


class StudentManualenrollmentaudit(models.Model):
    enrolled_email = models.CharField(max_length=255)
    time_stamp = models.DateTimeField(blank=True, null=True)
    state_transition = models.CharField(max_length=255)
    reason = models.TextField(blank=True, null=True)
    enrolled_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    enrollment = models.ForeignKey(StudentCourseenrollment, models.DO_NOTHING, blank=True, null=True)
    role = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_manualenrollmentaudit'


class StudentPendingemailchange(models.Model):
    new_email = models.CharField(max_length=255)
    activation_key = models.CharField(unique=True, max_length=32)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'student_pendingemailchange'


class StudentPendingnamechange(models.Model):
    new_name = models.CharField(max_length=255)
    rationale = models.CharField(max_length=1024)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'student_pendingnamechange'


class StudentPendingsecondaryemailchange(models.Model):
    new_secondary_email = models.CharField(max_length=255)
    activation_key = models.CharField(unique=True, max_length=32)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'student_pendingsecondaryemailchange'


class StudentRegistrationcookieconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    utm_cookie_name = models.CharField(max_length=255)
    affiliate_cookie_name = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_registrationcookieconfiguration'


class StudentSociallink(models.Model):
    platform = models.CharField(max_length=30)
    social_link = models.CharField(max_length=100)
    user_profile = models.ForeignKey(AuthUserprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_sociallink'


class StudentUserattribute(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_userattribute'
        unique_together = (('user', 'name'),)


class StudentUserpasswordtogglehistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.IntegerField()
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_userpasswordtogglehistory'


class StudentUsersignupsource(models.Model):
    site = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_usersignupsource'


class StudentUserstanding(models.Model):
    account_status = models.CharField(max_length=31)
    standing_last_changed_at = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'student_userstanding'


class StudentUsertestgroup(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'student_usertestgroup'


class StudentUsertestgroupUsers(models.Model):
    usertestgroup = models.ForeignKey(StudentUsertestgroup, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_usertestgroup_users'
        unique_together = (('usertestgroup', 'user'),)


class SubmissionsScore(models.Model):
    points_earned = models.PositiveIntegerField()
    points_possible = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    reset = models.IntegerField()
    student_item = models.ForeignKey('SubmissionsStudentitem', models.DO_NOTHING)
    submission = models.ForeignKey('SubmissionsSubmission', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submissions_score'


class SubmissionsScoreannotation(models.Model):
    annotation_type = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    reason = models.TextField()
    score = models.ForeignKey(SubmissionsScore, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'submissions_scoreannotation'


class SubmissionsScoresummary(models.Model):
    highest = models.ForeignKey(SubmissionsScore, models.DO_NOTHING)
    latest = models.ForeignKey(SubmissionsScore, models.DO_NOTHING)
    student_item = models.ForeignKey('SubmissionsStudentitem', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'submissions_scoresummary'


class SubmissionsStudentitem(models.Model):
    student_id = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    item_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'submissions_studentitem'
        unique_together = (('course_id', 'student_id', 'item_id'),)


class SubmissionsSubmission(models.Model):
    uuid = models.CharField(max_length=32)
    attempt_number = models.PositiveIntegerField()
    submitted_at = models.DateTimeField()
    created_at = models.DateTimeField()
    raw_answer = models.TextField()
    student_item = models.ForeignKey(SubmissionsStudentitem, models.DO_NOTHING)
    status = models.CharField(max_length=1)
    team_submission = models.ForeignKey('SubmissionsTeamsubmission', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submissions_submission'


class SubmissionsTeamsubmission(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(max_length=32)
    attempt_number = models.PositiveIntegerField()
    submitted_at = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    team_id = models.CharField(max_length=255)
    status = models.CharField(max_length=1)
    submitted_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submissions_teamsubmission'


class SuperCsvCsvoperation(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    class_name = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255)
    operation = models.CharField(max_length=255)
    data = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    original_filename = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'super_csv_csvoperation'


class SurveySurveyanswer(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    field_name = models.CharField(max_length=255)
    field_value = models.CharField(max_length=1024)
    course_key = models.CharField(max_length=255, blank=True, null=True)
    form = models.ForeignKey('SurveySurveyform', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'survey_surveyanswer'


class SurveySurveyform(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    form = models.TextField()

    class Meta:
        managed = False
        db_table = 'survey_surveyform'


class SystemWideRolesSystemwiderole(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_wide_roles_systemwiderole'


class SystemWideRolesSystemwideroleassignment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    role = models.ForeignKey(SystemWideRolesSystemwiderole, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_wide_roles_systemwideroleassignment'


class TaggingTagavailablevalues(models.Model):
    value = models.CharField(max_length=255)
    category = models.ForeignKey('TaggingTagcategories', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tagging_tagavailablevalues'


class TaggingTagcategories(models.Model):
    name = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tagging_tagcategories'


class TeamsCourseteam(models.Model):
    team_id = models.CharField(unique=True, max_length=255)
    discussion_topic_id = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    topic_id = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    description = models.CharField(max_length=300)
    country = models.CharField(max_length=2)
    language = models.CharField(max_length=16)
    last_activity_at = models.DateTimeField()
    team_size = models.IntegerField()
    organization_protected = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'teams_courseteam'


class TeamsCourseteammembership(models.Model):
    date_joined = models.DateTimeField()
    last_activity_at = models.DateTimeField()
    team = models.ForeignKey(TeamsCourseteam, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teams_courseteammembership'
        unique_together = (('user', 'team'),)


class ThemingSitetheme(models.Model):
    theme_dir_name = models.CharField(max_length=255)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'theming_sitetheme'


class ThirdPartyAuthLtiproviderconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    name = models.CharField(max_length=50)
    skip_registration_form = models.IntegerField()
    skip_email_verification = models.IntegerField()
    lti_consumer_key = models.CharField(max_length=255)
    lti_hostname = models.CharField(max_length=255)
    lti_consumer_secret = models.CharField(max_length=255)
    lti_max_timestamp_age = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)
    max_session_length = models.PositiveIntegerField(blank=True, null=True)
    skip_hinted_login_dialog = models.IntegerField()
    send_to_registration_first = models.IntegerField()
    sync_learner_profile_data = models.IntegerField()
    send_welcome_email = models.IntegerField()
    slug = models.CharField(max_length=30)
    enable_sso_id_verification = models.IntegerField()
    organization = models.ForeignKey(OrganizationsOrganization, models.DO_NOTHING, blank=True, null=True)
    visible = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'third_party_auth_ltiproviderconfig'


class ThirdPartyAuthOauth2Providerconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    icon_class = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    secondary = models.IntegerField()
    skip_registration_form = models.IntegerField()
    skip_email_verification = models.IntegerField()
    backend_name = models.CharField(max_length=50)
    key = models.TextField()
    secret = models.TextField()
    other_settings = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    icon_image = models.CharField(max_length=100)
    visible = models.IntegerField()
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)
    max_session_length = models.PositiveIntegerField(blank=True, null=True)
    skip_hinted_login_dialog = models.IntegerField()
    send_to_registration_first = models.IntegerField()
    sync_learner_profile_data = models.IntegerField()
    send_welcome_email = models.IntegerField()
    slug = models.CharField(max_length=30)
    enable_sso_id_verification = models.IntegerField()
    organization = models.ForeignKey(OrganizationsOrganization, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'third_party_auth_oauth2providerconfig'


class ThirdPartyAuthSamlconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    private_key = models.TextField()
    public_key = models.TextField()
    entity_id = models.CharField(max_length=255)
    org_info_str = models.TextField()
    other_config_str = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)
    slug = models.CharField(max_length=30)
    is_public = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'third_party_auth_samlconfiguration'


class ThirdPartyAuthSamlproviderconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    icon_class = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    secondary = models.IntegerField()
    skip_registration_form = models.IntegerField()
    skip_email_verification = models.IntegerField()
    backend_name = models.CharField(max_length=50)
    entity_id = models.CharField(max_length=255)
    metadata_source = models.CharField(max_length=255)
    attr_user_permanent_id = models.CharField(max_length=128)
    attr_full_name = models.CharField(max_length=128)
    attr_first_name = models.CharField(max_length=128)
    attr_last_name = models.CharField(max_length=128)
    attr_username = models.CharField(max_length=128)
    attr_email = models.CharField(max_length=128)
    other_settings = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    icon_image = models.CharField(max_length=100)
    debug_mode = models.IntegerField()
    visible = models.IntegerField()
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)
    automatic_refresh_enabled = models.IntegerField()
    identity_provider_type = models.CharField(max_length=128)
    max_session_length = models.PositiveIntegerField(blank=True, null=True)
    skip_hinted_login_dialog = models.IntegerField()
    send_to_registration_first = models.IntegerField()
    sync_learner_profile_data = models.IntegerField()
    archived = models.IntegerField()
    saml_configuration = models.ForeignKey(ThirdPartyAuthSamlconfiguration, models.DO_NOTHING, blank=True, null=True)
    send_welcome_email = models.IntegerField()
    slug = models.CharField(max_length=30)
    enable_sso_id_verification = models.IntegerField()
    default_email = models.CharField(max_length=255)
    default_first_name = models.CharField(max_length=255)
    default_full_name = models.CharField(max_length=255)
    default_last_name = models.CharField(max_length=255)
    default_username = models.CharField(max_length=255)
    organization = models.ForeignKey(OrganizationsOrganization, models.DO_NOTHING, blank=True, null=True)
    country = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'third_party_auth_samlproviderconfig'


class ThirdPartyAuthSamlproviderdata(models.Model):
    fetched_at = models.DateTimeField()
    expires_at = models.DateTimeField(blank=True, null=True)
    entity_id = models.CharField(max_length=255)
    sso_url = models.CharField(max_length=200)
    public_key = models.TextField()

    class Meta:
        managed = False
        db_table = 'third_party_auth_samlproviderdata'


class ThumbnailKvstore(models.Model):
    key = models.CharField(primary_key=True, max_length=200)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'thumbnail_kvstore'


class UserApiRetirementstate(models.Model):
    state_name = models.CharField(unique=True, max_length=30)
    state_execution_order = models.SmallIntegerField(unique=True)
    is_dead_end_state = models.IntegerField()
    required = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_api_retirementstate'


class UserApiUsercoursetag(models.Model):
    key = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    value = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_api_usercoursetag'
        unique_together = (('user', 'course_id', 'key'),)


class UserApiUserorgtag(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    key = models.CharField(max_length=255)
    org = models.CharField(max_length=255)
    value = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_api_userorgtag'
        unique_together = (('user', 'org', 'key'),)


class UserApiUserpreference(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_api_userpreference'
        unique_together = (('user', 'key'),)


class UserApiUserretirementpartnerreportingstatus(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    original_username = models.CharField(max_length=150)
    original_email = models.CharField(max_length=254)
    original_name = models.CharField(max_length=255)
    is_being_processed = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'user_api_userretirementpartnerreportingstatus'


class UserApiUserretirementrequest(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'user_api_userretirementrequest'


class UserApiUserretirementstatus(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    original_username = models.CharField(max_length=150)
    original_email = models.CharField(max_length=254)
    original_name = models.CharField(max_length=255)
    retired_username = models.CharField(max_length=150)
    retired_email = models.CharField(max_length=254)
    responses = models.TextField()
    current_state = models.ForeignKey(UserApiRetirementstate, models.DO_NOTHING)
    last_state = models.ForeignKey(UserApiRetirementstate, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'user_api_userretirementstatus'


class UserTasksUsertaskartifact(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(unique=True, max_length=32)
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=100, blank=True, null=True)
    url = models.TextField()
    text = models.TextField()
    status = models.ForeignKey('UserTasksUsertaskstatus', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_tasks_usertaskartifact'


class UserTasksUsertaskstatus(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    uuid = models.CharField(unique=True, max_length=32)
    task_id = models.CharField(unique=True, max_length=128)
    is_container = models.IntegerField()
    task_class = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=128)
    completed_steps = models.PositiveSmallIntegerField()
    total_steps = models.PositiveSmallIntegerField()
    attempts = models.PositiveSmallIntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_tasks_usertaskstatus'


class UtilRatelimitconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'util_ratelimitconfiguration'


class VerifiedTrackContentMigrateverifiedtrackcohortssetting(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    old_course_key = models.CharField(max_length=255)
    rerun_course_key = models.CharField(max_length=255)
    audit_cohort_names = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verified_track_content_migrateverifiedtrackcohortssetting'


class VerifiedTrackContentVerifiedtrackcohortedcourse(models.Model):
    course_key = models.CharField(unique=True, max_length=255)
    enabled = models.IntegerField()
    verified_cohort_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'verified_track_content_verifiedtrackcohortedcourse'


class VerifyStudentManualverification(models.Model):
    status = models.CharField(max_length=100)
    status_changed = models.DateTimeField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    reason = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verify_student_manualverification'


class VerifyStudentSoftwaresecurephotoverification(models.Model):
    status = models.CharField(max_length=100)
    status_changed = models.DateTimeField()
    name = models.CharField(max_length=255)
    face_image_url = models.CharField(max_length=255)
    photo_id_image_url = models.CharField(max_length=255)
    receipt_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    display = models.IntegerField()
    submitted_at = models.DateTimeField(blank=True, null=True)
    reviewing_service = models.CharField(max_length=255)
    error_msg = models.TextField()
    error_code = models.CharField(max_length=50)
    photo_id_key = models.TextField()
    copy_id_photo_from = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    reviewing_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    expiry_date = models.DateTimeField(blank=True, null=True)
    expiry_email_date = models.DateTimeField(blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verify_student_softwaresecurephotoverification'


class VerifyStudentSsoverification(models.Model):
    status = models.CharField(max_length=100)
    status_changed = models.DateTimeField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    identity_provider_type = models.CharField(max_length=100)
    identity_provider_slug = models.CharField(max_length=30)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verify_student_ssoverification'


class VerifyStudentSspverificationretryconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    arguments = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verify_student_sspverificationretryconfig'


class VerifyStudentVerificationdeadline(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_key = models.CharField(unique=True, max_length=255)
    deadline = models.DateTimeField()
    deadline_is_explicit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'verify_student_verificationdeadline'


class VideoConfigCoursehlsplaybackenabledflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    course_id = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_config_coursehlsplaybackenabledflag'


class VideoConfigCoursevideotranscriptenabledflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    course_id = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_config_coursevideotranscriptenabledflag'


class VideoConfigCourseyoutubeblockedflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    course_id = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_config_courseyoutubeblockedflag'


class VideoConfigHlsplaybackenabledflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    enabled_for_all_courses = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_config_hlsplaybackenabledflag'


class VideoConfigMigrationenqueuedcourse(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(primary_key=True, max_length=255)
    command_run = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'video_config_migrationenqueuedcourse'


class VideoConfigTranscriptmigrationsetting(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    force_update = models.IntegerField()
    commit = models.IntegerField()
    all_courses = models.IntegerField()
    course_ids = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    command_run = models.PositiveIntegerField()
    batch_size = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'video_config_transcriptmigrationsetting'


class VideoConfigUpdatedcoursevideos(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    edx_video_id = models.CharField(max_length=100)
    command_run = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'video_config_updatedcoursevideos'
        unique_together = (('course_id', 'edx_video_id'),)


class VideoConfigVideothumbnailsetting(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    command_run = models.PositiveIntegerField()
    batch_size = models.PositiveIntegerField()
    videos_per_task = models.PositiveIntegerField()
    commit = models.IntegerField()
    all_course_videos = models.IntegerField()
    course_ids = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    offset = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'video_config_videothumbnailsetting'


class VideoConfigVideotranscriptenabledflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    enabled_for_all_courses = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_config_videotranscriptenabledflag'


class VideoPipelineCoursevideouploadsenabledbydefault(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    course_id = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_pipeline_coursevideouploadsenabledbydefault'


class VideoPipelineVempipelineintegration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    client_name = models.CharField(max_length=100)
    api_url = models.CharField(max_length=200)
    service_username = models.CharField(max_length=100)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_pipeline_vempipelineintegration'


class VideoPipelineVideouploadsenabledbydefault(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    enabled_for_all_courses = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_pipeline_videouploadsenabledbydefault'


class WaffleFlag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    everyone = models.IntegerField(blank=True, null=True)
    percent = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    testing = models.IntegerField()
    superusers = models.IntegerField()
    staff = models.IntegerField()
    authenticated = models.IntegerField()
    languages = models.TextField()
    rollout = models.IntegerField()
    note = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'waffle_flag'


class WaffleFlagGroups(models.Model):
    flag = models.ForeignKey(WaffleFlag, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'waffle_flag_groups'
        unique_together = (('flag', 'group'),)


class WaffleFlagUsers(models.Model):
    flag = models.ForeignKey(WaffleFlag, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'waffle_flag_users'
        unique_together = (('flag', 'user'),)


class WaffleSample(models.Model):
    name = models.CharField(unique=True, max_length=100)
    percent = models.DecimalField(max_digits=4, decimal_places=1)
    note = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'waffle_sample'


class WaffleSwitch(models.Model):
    name = models.CharField(unique=True, max_length=100)
    active = models.IntegerField()
    note = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'waffle_switch'


class WaffleUtilsWaffleflagcourseoverridemodel(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    waffle_flag = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    override_choice = models.CharField(max_length=3)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waffle_utils_waffleflagcourseoverridemodel'


class WikiArticle(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    group_read = models.IntegerField()
    group_write = models.IntegerField()
    other_read = models.IntegerField()
    other_write = models.IntegerField()
    current_revision = models.ForeignKey('WikiArticlerevision', models.DO_NOTHING, unique=True, blank=True, null=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_article'


class WikiArticleforobject(models.Model):
    object_id = models.PositiveIntegerField()
    is_mptt = models.IntegerField()
    article = models.ForeignKey(WikiArticle, models.DO_NOTHING)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wiki_articleforobject'
        unique_together = (('content_type', 'object_id'),)


class WikiArticleplugin(models.Model):
    deleted = models.IntegerField()
    created = models.DateTimeField()
    article = models.ForeignKey(WikiArticle, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wiki_articleplugin'


class WikiArticlerevision(models.Model):
    revision_number = models.IntegerField()
    user_message = models.TextField()
    automatic_log = models.TextField()
    ip_address = models.CharField(max_length=39, blank=True, null=True)
    modified = models.DateTimeField()
    created = models.DateTimeField()
    deleted = models.IntegerField()
    locked = models.IntegerField()
    content = models.TextField()
    title = models.CharField(max_length=512)
    article = models.ForeignKey(WikiArticle, models.DO_NOTHING)
    previous_revision = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_articlerevision'
        unique_together = (('article', 'revision_number'),)


class WikiReusableplugin(models.Model):
    articleplugin_ptr = models.ForeignKey(WikiArticleplugin, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'wiki_reusableplugin'


class WikiReusablepluginArticles(models.Model):
    reusableplugin = models.ForeignKey(WikiReusableplugin, models.DO_NOTHING)
    article = models.ForeignKey(WikiArticle, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wiki_reusableplugin_articles'
        unique_together = (('reusableplugin', 'article'),)


class WikiRevisionplugin(models.Model):
    articleplugin_ptr = models.ForeignKey(WikiArticleplugin, models.DO_NOTHING, primary_key=True)
    current_revision = models.ForeignKey('WikiRevisionpluginrevision', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_revisionplugin'


class WikiRevisionpluginrevision(models.Model):
    revision_number = models.IntegerField()
    user_message = models.TextField()
    automatic_log = models.TextField()
    ip_address = models.CharField(max_length=39, blank=True, null=True)
    modified = models.DateTimeField()
    created = models.DateTimeField()
    deleted = models.IntegerField()
    locked = models.IntegerField()
    plugin = models.ForeignKey(WikiRevisionplugin, models.DO_NOTHING)
    previous_revision = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_revisionpluginrevision'


class WikiSimpleplugin(models.Model):
    articleplugin_ptr = models.ForeignKey(WikiArticleplugin, models.DO_NOTHING, primary_key=True)
    article_revision = models.ForeignKey(WikiArticlerevision, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wiki_simpleplugin'


class WikiUrlpath(models.Model):
    slug = models.CharField(max_length=255, blank=True, null=True)
    lft = models.PositiveIntegerField()
    rght = models.PositiveIntegerField()
    tree_id = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    article = models.ForeignKey(WikiArticle, models.DO_NOTHING)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wiki_urlpath'
        unique_together = (('site', 'parent', 'slug'),)


class WorkflowAssessmentworkflow(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=100)
    status_changed = models.DateTimeField()
    submission_uuid = models.CharField(unique=True, max_length=36)
    uuid = models.CharField(unique=True, max_length=32)
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'workflow_assessmentworkflow'


class WorkflowAssessmentworkflowcancellation(models.Model):
    comments = models.TextField()
    cancelled_by_id = models.CharField(max_length=40)
    created_at = models.DateTimeField()
    workflow = models.ForeignKey(WorkflowAssessmentworkflow, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'workflow_assessmentworkflowcancellation'


class WorkflowAssessmentworkflowstep(models.Model):
    name = models.CharField(max_length=20)
    submitter_completed_at = models.DateTimeField(blank=True, null=True)
    assessment_completed_at = models.DateTimeField(blank=True, null=True)
    order_num = models.PositiveIntegerField()
    workflow = models.ForeignKey(WorkflowAssessmentworkflow, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'workflow_assessmentworkflowstep'


class WorkflowTeamassessmentworkflow(models.Model):
    assessmentworkflow_ptr = models.ForeignKey(WorkflowAssessmentworkflow, models.DO_NOTHING, primary_key=True)
    team_submission_uuid = models.CharField(unique=True, max_length=128)

    class Meta:
        managed = False
        db_table = 'workflow_teamassessmentworkflow'


class XapiXapilearnerdatatransmissionaudit(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    enterprise_course_enrollment_id = models.PositiveIntegerField(blank=True, null=True)
    course_id = models.CharField(max_length=255)
    course_completed = models.IntegerField()
    completed_timestamp = models.DateTimeField(blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100)
    error_message = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'xapi_xapilearnerdatatransmissionaudit'
        unique_together = (('user', 'course_id'),)


class XapiXapilrsconfiguration(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    version = models.CharField(max_length=16)
    endpoint = models.CharField(max_length=200)
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    active = models.IntegerField()
    enterprise_customer = models.ForeignKey(EnterpriseEnterprisecustomer, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'xapi_xapilrsconfiguration'


class XblockConfigCourseeditltifieldsenabledflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    course_id = models.CharField(max_length=255)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xblock_config_courseeditltifieldsenabledflag'


class XblockConfigStudioconfig(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    disabled_blocks = models.TextField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xblock_config_studioconfig'


class XblockDjangoXblockconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    name = models.CharField(max_length=255)
    deprecated = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xblock_django_xblockconfiguration'


class XblockDjangoXblockstudioconfiguration(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    name = models.CharField(max_length=255)
    template = models.CharField(max_length=255)
    support_level = models.CharField(max_length=2)
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xblock_django_xblockstudioconfiguration'


class XblockDjangoXblockstudioconfigurationflag(models.Model):
    change_date = models.DateTimeField()
    enabled = models.IntegerField()
    changed_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xblock_django_xblockstudioconfigurationflag'
