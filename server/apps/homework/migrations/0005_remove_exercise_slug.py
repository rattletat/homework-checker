# Generated by Django 3.1.7 on 2021-04-22 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0004_auto_20210404_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='slug',
        ),
    ]
