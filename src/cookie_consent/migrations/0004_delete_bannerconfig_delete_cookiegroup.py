# Generated by Django 5.1.5 on 2025-01-23 19:06
from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = (
        ("cookie_consent", "0003_alter_cookiegroup_version"),
        ("base", "0003_googleanalytics"),
    )

    operations = (
        migrations.SeparateDatabaseAndState(
            state_operations=(
                migrations.DeleteModel(
                    name="BannerConfig",
                ),
                migrations.DeleteModel(
                    name="CookieGroup",
                ),
            ),
            database_operations=(
                migrations.AlterModelTable(
                    name="BannerConfig",
                    table="cooco_bannerconfig",
                ),
                migrations.AlterModelTable(
                    name="CookieGroup",
                    table="cooco_cookiegroup",
                ),
            ),
        ),
    )
