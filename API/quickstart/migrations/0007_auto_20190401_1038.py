# Generated by Django 2.1.3 on 2019-04-01 08:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0006_auto_20190305_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.CharField(default=datetime.datetime(2019, 4, 1, 8, 38, 8, 296020, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='date',
            field=models.CharField(default=datetime.datetime(2019, 4, 1, 8, 38, 8, 294022, tzinfo=utc), max_length=100),
        ),
    ]