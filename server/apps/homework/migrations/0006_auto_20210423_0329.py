# Generated by Django 3.1.7 on 2021-04-23 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0002_auto_20210404_1521'),
        ('homework', '0005_remove_exercise_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='teaching.lesson'),
        ),
    ]