from django.db import models
from django.utils import timezone

from person.models import Person
from album.models import Album
from moment.models import Moment

class Picture(models.Model):
    pid = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Person, on_delete=models.SET_DEFAULT, default=settings.DEFAULT_PERSON_ID)
    create_time = models.DateField(default=timezone.now)
    file_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

class Picture_Album(models.Model):
    pid = models.ForeignKey(Picture, on_delete=models.CASCADE)
    aid = models.ForeignKey(Album, on_delete=models.CASCADE)
    moved_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('pid', 'aid'),)

class Picture_Moment(models.Model):
    pid = models.ForeignKey(Picture, on_delete=models.CASCADE)
    mid = models.ForeignKey(Moment, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('pid', 'mid'),)
