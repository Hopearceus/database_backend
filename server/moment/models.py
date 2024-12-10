from django.db import models

from person.models import Person
from trip.models import Trip
from django.db.models import CheckConstraint, Q, F

class Moment(models.Model):
    mid = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    tid = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True)
    discover = models.ImageField(upload_to='discover/', null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
    
class Moment_Person(models.Model):
    pid = models.ForeignKey(Person, on_delete=models.CASCADE)
    mid = models.ForeignKey(Moment, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    time = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(null=True)

    class Meta:
        unique_together = (('pid', 'mid'),)
        constraints = [
            CheckConstraint(
                check=~Q(content__isnull=True) | ~Q(like__isnull=True),
                name='check_like_or_content_not_null'
            )
        ]
