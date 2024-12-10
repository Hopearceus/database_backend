from django.db import models
from django.utils import timezone

class Picture(models.Model):
    pid = models.AutoField(primary_key=True)
    creator = models.ForeignKey('person.Person', on_delete=models.SET_DEFAULT, default=0)
    create_time = models.DateField(default=timezone.now)
    file_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/')

class Picture_Album(models.Model):
    pid = models.ForeignKey(Picture, on_delete=models.CASCADE)
    aid = models.ForeignKey('album.Album', on_delete=models.CASCADE)
    moved_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('pid', 'aid'),)

class Picture_Moment(models.Model):
    pid = models.ForeignKey(Picture, on_delete=models.CASCADE)
    mid = models.ForeignKey('moment.Moment', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('pid', 'mid'),)
