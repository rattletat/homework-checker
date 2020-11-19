# Generated by Django 3.1.2 on 2020-11-18 18:27

import apps.homework.storage
import apps.teaching.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0006_auto_20201118_1920'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lecture',
            options={},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={},
        ),
        migrations.AlterField(
            model_name='lectureresource',
            name='file',
            field=models.FileField(max_length=255, storage=apps.homework.storage.OverwriteStorage(), upload_to=apps.teaching.helpers.get_lecture_rsc_path),
        ),
        migrations.AlterField(
            model_name='lessonresource',
            name='file',
            field=models.FileField(max_length=255, storage=apps.homework.storage.OverwriteStorage(), upload_to=apps.teaching.helpers.get_lesson_rsc_path),
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together=set(),
        ),
    ]
