from django.contrib import admin

from .models import FileOriginal, DirOriginal, PublicKey, Organisation

class DirOriginalAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
class FileOriginalAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'lines_total', 'lines_error', 'created', 'updated')
    search_fields = ['name']
    list_filter = ['dir_original']

admin.site.register(DirOriginal, DirOriginalAdmin)
admin.site.register(FileOriginal, FileOriginalAdmin)
admin.site.register(PublicKey)
admin.site.register(Organisation)
