from django.db import models

from django.conf import settings

# Create your models here.
class count(models.Model):
    cou=models.CharField(max_length=30)
class track(models.Model):
    trace=models.IntegerField()
