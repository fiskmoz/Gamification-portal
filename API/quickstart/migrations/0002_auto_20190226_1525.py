# Generated by Django 2.1.3 on 2019-02-26 14:25

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(max_length=250, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('date', models.CharField(default=datetime.datetime(2019, 2, 26, 14, 25, 32, 301096, tzinfo=utc), max_length=100)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleLink',
            fields=[
                ('id', models.AutoField(max_length=250, primary_key=True, serialize=False)),
                ('article', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quickstart.Article')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('file', models.FileField(default='UNDEFINED', unique=True, upload_to='files/')),
            ],
        ),
        migrations.CreateModel(
            name='QuizLink',
            fields=[
                ('id', models.AutoField(max_length=250, primary_key=True, serialize=False)),
                ('article', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quickstart.Article')),
            ],
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='Date',
        ),
        migrations.AddField(
            model_name='quiz',
            name='date',
            field=models.CharField(default=datetime.datetime(2019, 2, 26, 14, 25, 32, 299096, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='id',
            field=models.AutoField(max_length=250, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='quizlink',
            name='quiz',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quickstart.Quiz'),
        ),
        migrations.AddField(
            model_name='articlelink',
            name='filePath',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quickstart.File', to_field='file'),
        ),
    ]