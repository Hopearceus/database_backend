# Generated by Django 5.1.4 on 2024-12-10 06:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='time',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
    ]