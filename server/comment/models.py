from django.db import models

class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    mid = models.ForeignKey('moment.Moment', on_delete=models.CASCADE)
    pid = models.ForeignKey('person.Person', on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField()

    def __str__(self):
        return self.content[:50]
    
    class Meta:
        unique_together = (('mid', 'pid'),)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(content__isnull=True) | ~models.Q(like__isnull=True),
                name='check_like_or_content_not_null'
            )
        ]