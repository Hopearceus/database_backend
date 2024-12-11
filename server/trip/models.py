from django.db import models
from person.models import Person

class Trip(models.Model):
    tid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    stime = models.DateField()
    ttime = models.DateField()
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    description = models.TextField()

class Trip_Person(models.Model):
    tid = models.ForeignKey(Trip, on_delete=models.CASCADE)
    pid = models.ForeignKey(Person, on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return self.notes[:50]
    
    class Meta:
        unique_together = (('tid', 'pid'),)