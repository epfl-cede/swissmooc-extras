import datetime

from django.db import models

class Site(models.Model):
    hostname = models.CharField(max_length=256, unique=True)
    expires = models.DateTimeField('expire date', null=True, blank=True)
    error = models.CharField(max_length=256, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.hostname
    @property
    def expires_days(self):
        if self.expires:
            return self.expires - datetime.datetime.utcnow()
        else:
            return '-'

