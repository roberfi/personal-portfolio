from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = (("home", "0013_reorder_technology_priority"),)

    operations = (
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("title_en", models.CharField(max_length=200, null=True)),
                ("title_es", models.CharField(max_length=200, null=True)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("short_description", models.CharField(max_length=300)),
                ("short_description_en", models.CharField(max_length=300, null=True)),
                ("short_description_es", models.CharField(max_length=300, null=True)),
                ("long_description", models.TextField()),
                ("long_description_en", models.TextField(null=True)),
                ("long_description_es", models.TextField(null=True)),
                ("icon_name", models.CharField(blank=True, max_length=100)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ("order", "title"),
            },
        ),
    )
