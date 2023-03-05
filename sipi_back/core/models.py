from django.db import models
from users.models import User


class Subject(models.Model):
    title = models.CharField(max_length=128, unique=True)


class Queue(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='User'
    )
    subject_id = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='Subject'
    )
    timestamp = models.TimeField(
        auto_now=True
    )

    class Meta:
        ordering = ('subject_id', 'timestamp')
