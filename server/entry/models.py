from django.db import models

from trip.models import Trip

class Entry(models.Model):
    eid = models.AutoField(primary_key=True)
    tid = models.ForeignKey(Trip, on_delete=models.CASCADE)
    time = models.DateField()
    place = models.TextField()
    description = models.TextField()
    title = models.CharField(max_length=255)