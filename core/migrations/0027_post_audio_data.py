# Generated by Django 4.0.3 on 2022-04-04 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_post_audio_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='audio_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]