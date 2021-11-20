from django.db import models
from django.contrib.auth.models import User


class GoogleAccount(models.Model):
    username = models.CharField(max_length=100)
    uuid = models.CharField(max_length=100)
    token = models.TextField(max_length=2000)
    linked_username = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.username