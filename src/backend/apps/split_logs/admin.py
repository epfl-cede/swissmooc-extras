# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Course
from .models import CourseDump
from .models import CourseDumpTable
from .models import DirOriginal
from .models import FileOriginal
from .models import FileOriginalDocker
from .models import Organisation
from .models import PublicKey

class DirOriginalAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
class FileOriginalAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'lines_total', 'lines_error', 'created', 'updated')
    search_fields = ['name']
    list_filter = ['dir_original']
class FileOriginalDockerAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'lines_total', 'lines_error', 'created', 'updated')
    search_fields = ['name']
    list_filter = ['dir_original']
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'active', 'created', 'updated')
    search_fields = ['name', 'organisation__name']
class CourseDumpAdmin(admin.ModelAdmin):
    list_display = ('course', 'table', 'date', 'is_encypted', 'created', 'updated')
    list_filter = ['course__organisation', 'date', 'is_encypted']
    search_fields = ['course__name']
class CourseDumpTableAdmin(admin.ModelAdmin):
    list_display = ('db_type', 'db_name', 'name', 'primary_key', 'created', 'updated')
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')

admin.site.register(DirOriginal, DirOriginalAdmin)
admin.site.register(FileOriginal, FileOriginalAdmin)
admin.site.register(FileOriginalDocker, FileOriginalDockerAdmin)
admin.site.register(PublicKey)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseDump, CourseDumpAdmin)
admin.site.register(CourseDumpTable, CourseDumpTableAdmin)
