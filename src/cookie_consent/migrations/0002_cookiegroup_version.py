# Generated by Django 5.1.4 on 2025-01-14 15:24
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = (("cookie_consent", "0001_initial"),)

    operations = (
        migrations.AddField(
            model_name="cookiegroup",
            name="version",
            field=models.PositiveBigIntegerField(default=1, editable=False),
        ),
    )
