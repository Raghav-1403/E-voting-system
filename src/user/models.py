from django.db import models
from django.conf import settings
from main.models import organizations


# Create your models here.


class position(models.Model):
    participant=models.CharField(max_length=30)
    org=models.ForeignKey(organizations,on_delete=models.CASCADE)


class hashvalue(models.Model):
    hash_values=models.CharField(max_length=65)

class partymembers(models.Model):
    party=models.CharField(max_length=20)
    party_display=models.CharField(max_length=20)
    party_pos=models.ForeignKey(position,on_delete=models.CASCADE)

class partyselection(models.Model):
    pos=models.ForeignKey(position,on_delete=models.CASCADE)

