from django.db import models

# Create your models here.
from django.db import models

class Execute(models.Model):
    command = models.CharField(max_length=1024)
    return_code = models.SmallIntegerField(default=0)
    str_out = models.TextField()
    str_err = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.command

