from django.contrib import admin

from .models import FileOriginal, DirOriginal

class DirOriginalAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
class FileOriginalAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'lines_total', 'lines_error', 'created', 'updated')
    list_filter = ['dir_original']

admin.site.register(DirOriginal, DirOriginalAdmin)
admin.site.register(FileOriginal, FileOriginalAdmin)
