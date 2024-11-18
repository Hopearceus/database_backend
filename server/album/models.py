from django.db import models
from django.utils import timezone

from person.models import Person

class Album(models.Model):
    aid = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Person, on_delete=models.CASCADE)
    description = models.TextField()
    time = models.DateField(timezone.now)
