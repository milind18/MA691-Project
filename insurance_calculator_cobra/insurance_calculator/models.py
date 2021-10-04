from django.db import models

REGION_CHOICES = (
    ('southwest', 'South-West'), 
    ('southeast', 'South-East'), 
    ('northwest', 'North-West'), 
    ('northeast', 'North-East')
)
SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)
# Create your models here.
class User(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default="M")
    bmi = models.FloatField()
    children = models.IntegerField()
    smoker = models.BooleanField(default=True)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, default='southeast')
