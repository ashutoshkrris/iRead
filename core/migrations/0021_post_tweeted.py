# Generated by Django 3.2.10 on 2021-12-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_series_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tweeted',
            field=models.BooleanField(default=False),
        ),
    ]