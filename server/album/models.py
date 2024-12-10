from django.db import models
from django.utils import timezone


class Album(models.Model):
    aid = models.AutoField(primary_key=True)
    pid = models.ForeignKey('person.Person', on_delete=models.CASCADE)
    description = models.TextField()
    time = models.DateTimeField(timezone.now)
    name = models.CharField(max_length=50, default='默认相册')
    cover_url = models.CharField(max_length=255, default='')
