from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class votersdb(models.Model):
    Name=models.CharField(max_length=20)
    mail=models.EmailField(max_length=254)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    pos=ArrayField(models.CharField(max_length=50), blank=True,default=list)
    votepos=ArrayField(models.BooleanField())
class minerdb(models.Model):
    Name=models.CharField(max_length=20)
    mail=models.EmailField(max_length=254)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    voteval=models.BooleanField()

class organizations(models.Model):
    org=models.CharField(max_length=30,unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    def __str__(self):
        return self.org
