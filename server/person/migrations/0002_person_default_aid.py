# Generated by Django 5.1.4 on 2024-12-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='default_aid',
            field=models.IntegerField(null=True),
        ),
    ]
