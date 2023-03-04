from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    BASIC_USER = 1
    MODERATOR = 2
    ADMIN = 3
    ROLE_CHOICES = [
        (BASIC_USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    ]

    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, default=BASIC_USER,
        verbose_name='Роль', blank=False, null=False)

    personal_cipher = models.CharField(max_length=16, unique=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_basic_user(self):
        return self.role == self.BASIC_USER
