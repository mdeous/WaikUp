from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name


class Link(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    submit_date = models.DateTimeField(default=datetime.now)
    archived = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class Recipient(models.Model):
    class Meta:
        verbose_name = 'E-mail'
    address = models.EmailField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.address

