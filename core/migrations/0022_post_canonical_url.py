# Generated by Django 4.0.2 on 2022-02-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_post_tweeted'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='canonical_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
