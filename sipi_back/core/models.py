from django.db import models
from django.utils.text import slugify
from users.models import User


class Subject(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Queue(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='User'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='Subject',
    )
    timestamp = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ('id', 'timestamp')
        constraints = [
            models.UniqueConstraint(fields=['subject', 'user'],
                                    name='unique_fields'),
        ]


class Poll(models.Model):
    title = models.CharField(max_length=200)


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
