# Generated by Django 3.2.7 on 2021-09-25 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_calculator', '0002_auto_20210917_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='smoker',
            field=models.BooleanField(default=0),
        ),
    ]
