# Generated by Django 3.1.2 on 2020-11-17 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0007_auto_20201116_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='min_upload_size',
            field=models.PositiveIntegerField(default=30, verbose_name='Minimale Upload Größe in Bytes'),
        ),
    ]