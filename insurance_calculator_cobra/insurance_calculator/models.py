from django.db import models

# Create your models here.
class User(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    bmi = models.FloatField()
    children = models.IntegerField()
    smoker = models.BooleanField(default=True)
    region = models.CharField(max_length=50)
