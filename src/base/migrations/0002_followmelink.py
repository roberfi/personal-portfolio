# Generated by Django 5.1.3 on 2025-01-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = (("base", "0001_initial"),)

    operations = (
        migrations.CreateModel(
            name="FollowMeLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("link", models.URLField()),
                ("svg_view_box", models.CharField(max_length=16)),
                ("svg_path", models.TextField()),
            ],
        ),
    )