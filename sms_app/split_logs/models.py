from django.db import models

# Create your models here.
from django.db import models

class DirOriginal(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class FileOriginal(models.Model):
    name = models.CharField(max_length=1024)
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
    name = models.CharField(max_length=256)
    aliases = models.CharField(max_length=1024)
    public_key = models.ForeignKey(PublicKey, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
