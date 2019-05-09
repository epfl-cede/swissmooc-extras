import datetime

from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models

ACTIVE = '1'
NOT_ACTIVE = '0'
ACTIVE_CHOICES = (
    (NOT_ACTIVE, 'not active'),
    (ACTIVE, 'active'),
)
YES = '1'
NO = '0'
YES_NO_CHOICES = (
    (NO, 'no'),
    (YES, 'yes'),
)

class DirOriginal(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class FileOriginal(models.Model):
    name = models.CharField(max_length=255)
    dir_original = models.ForeignKey(DirOriginal, on_delete=models.CASCADE)
    lines_total = models.PositiveIntegerField(default=0)
    lines_error = models.PositiveIntegerField(default=0)
    @property
    def fullname(self):
        return "{}/{}".format(self.dir_original, self.name)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.fullname
    class Meta:
        unique_together = (("name", "dir_original"),)

class PublicKey(models.Model):
    name = models.CharField(max_length=128)
    recipient = models.CharField(max_length=128)
    value = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Organisation(models.Model):
    name = models.CharField(max_length=255)
    aliases = models.CharField(max_length=1024)
    public_key = models.ForeignKey(PublicKey, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    active = models.CharField(
        choices=ACTIVE_CHOICES,
        max_length=1,
        default=NOT_ACTIVE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    @property
    def folder(self):
        return self.name.replace('+', '-').replace('course-v1:', '')
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (('name', 'organisation'),)

class CourseDumpTable(models.Model):
    name = models.CharField(max_length=255)
    primary_key = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class CourseDump(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    table = models.ForeignKey(CourseDumpTable, on_delete=models.CASCADE)
    date = models.DateField()
    is_dumped = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=1,
        default=NO
    )
    is_encypted = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=1,
        default=NO
    )
    id_uploaded = models.CharField(
        choices=YES_NO_CHOICES,
        max_length=1,
        default=NO
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.course.name
    def dump_file_name(self):
        #epflx-2019-04-21/EPFLx-Algebre2X-1T2017-auth_user-prod-analytics.sql.gpg
        return "{path}/{org_name}/{date}/{org_name_lower}x-{date}/{course_folder}-{table_name}-prod-analytics.sql".format(
            path=settings.DUMP_DB_RAW,
            org_name=self.course.organisation.name,
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
            course_folder=self.course.folder,
            org_name_lower=self.course.organisation.name.lower(),
            table_name=self.table.name,
        )

    class Meta:
        unique_together = (('course', 'table', 'date'),)
