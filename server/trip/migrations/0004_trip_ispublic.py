# Generated by Django 5.1.4 on 2024-12-11 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_alter_trip_stime_alter_trip_ttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='isPublic',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
