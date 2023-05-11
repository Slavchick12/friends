from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Friends(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_friend_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_friend_user')

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'


class Notification(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user_to')

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
