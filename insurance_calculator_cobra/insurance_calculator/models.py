from django.db import models

# Create your models here.
class User(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    bmi = models.FloatField()
    children = models.IntegerField()
    region = models.CharField(max_length=50)
