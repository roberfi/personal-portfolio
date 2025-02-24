# Generated by Django 5.1.3 on 2024-11-15 12:24
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = (("home", "0002_experience_location"),)

    operations = (
        migrations.AddField(
            model_name="experience",
            name="description_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="experience",
            name="description_es",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="experience",
            name="location_en",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="experience",
            name="location_es",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="experience",
            name="title_en",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="experience",
            name="title_es",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="personalinfo",
            name="biography_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="personalinfo",
            name="biography_es",
            field=models.TextField(null=True),
        ),
    )
