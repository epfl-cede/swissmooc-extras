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
    @property
    def fullname(self):
        return "{}/{}".format(self.dir_original, self.name)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.fullname
    class Meta:
        unique_together = (("name", "dir_original"),)

