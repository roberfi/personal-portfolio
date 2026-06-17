from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = (("home", "0014_create_service"),)

    operations = (
        migrations.CreateModel(
            name="ProcessStep",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("title_en", models.CharField(max_length=200, null=True)),
                ("title_es", models.CharField(max_length=200, null=True)),
                ("description", models.TextField()),
                ("description_en", models.TextField(null=True)),
                ("description_es", models.TextField(null=True)),
                ("icon_name", models.CharField(blank=True, max_length=100)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ("order",),
            },
        ),
    )
