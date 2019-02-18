# Generated by Django 2.1.3 on 2019-02-18 11:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_auto_20190218_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('filepath', models.FileField(null=True, upload_to='files/', verbose_name='')),
            ],
        ),
        migrations.AlterField(
            model_name='quiz',
            name='Date',
            field=models.CharField(default=datetime.datetime(2019, 2, 18, 11, 44, 45, 963593, tzinfo=utc), max_length=250),
        ),
    ]