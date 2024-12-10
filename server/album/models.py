from django.db import models
from django.utils import timezone


class Album(models.Model):
    aid = models.AutoField(primary_key=True)
    pid = models.ForeignKey('person.Person', on_delete=models.CASCADE)
    description = models.TextField()
    time = models.DateTimeField(timezone.now)
