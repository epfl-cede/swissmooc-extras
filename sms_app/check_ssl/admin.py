from django.contrib import admin

# Register your models here.
from .models import Site

class SiteAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'expires', 'expires_days', 'error', 'updated')
    exclude = ('ssl_expire', 'error',)

    
admin.site.register(Site, SiteAdmin)

