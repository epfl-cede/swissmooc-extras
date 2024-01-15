# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.db import models


DB_TYPE_MYSQL = 'mysql'
DB_TYPE_MONGO = 'mongo'
DB_TYPE_CHOICES = (
    (DB_TYPE_MYSQL, DB_TYPE_MYSQL),
    (DB_TYPE_MONGO, DB_TYPE_MONGO),
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


class FileOriginalDocker(models.Model):
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
    name = models.CharField(max_length=255, unique=True)
    aliases = models.CharField(max_length=1024)
    public_key = models.ForeignKey(
        PublicKey,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def bucket_name(self):
        return f"{settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS}-{self.name.lower()}"

    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.CharField(max_length=255)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    structure = models.JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def folder(self):
        return self.course_id.replace('+', '-').replace('course-v1:', '')

    def __str__(self):
        return self.course_id

    class Meta:
        unique_together = (('course_id', 'organisation'),)


class CourseDumpTable(models.Model):
    db_type = models.CharField(
        choices=DB_TYPE_CHOICES,
        max_length=128,
        default=DB_TYPE_MYSQL
    )
    name = models.CharField(max_length=255)
    db_name = models.CharField(max_length=255)
    primary_key = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}/{}.{}'.format(self.db_type, self.db_name, self.name)


class CourseDump(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    table = models.ForeignKey(CourseDumpTable, on_delete=models.CASCADE)
    date = models.DateField()
    is_encypted = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course.course_id

    def dump_folder_name(self):
        return '{path}/{org_name_lower}-{date}'.format(
            path=settings.DUMP_DB_PATH,
            org_name_lower=self.course.organisation.name.lower(),
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
        )

    def dump_file_name(self):
        if self.table.db_type == DB_TYPE_MYSQL:
            suffix = 'prod-analytics.sql'
        elif self.table.db_type == DB_TYPE_MONGO:
            suffix = 'prod.mongo'
        else:
            raise Exception("Unsupported db_type table")

        # epflx-2019-04-21/EPFLx-Algebre2X-1T2017-auth_user-prod-analytics.sql.gpg
        return "{folder_name}/{course_folder}-{table_name}-{suffix}".format(
            folder_name=self.dump_folder_name(),
            course_folder=self.course.folder,
            table_name=self.table.name,
            suffix=suffix,
        )

    def encrypred_file_name(self):
        return '{}.gpg'.format(self.dump_file_name())

    class Meta:
        unique_together = (('course', 'table', 'date'),)
