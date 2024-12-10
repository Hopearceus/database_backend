# Generated by Django 5.1.4 on 2024-12-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='url',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
    ]