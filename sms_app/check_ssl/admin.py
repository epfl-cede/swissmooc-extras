# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Site
# Register your models here.

class SiteAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'expires', 'expires_days', 'error', 'updated')
    exclude = ('ssl_expire', 'error',)


admin.site.register(Site, SiteAdmin)
