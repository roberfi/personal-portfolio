from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = (("home", "0011_migrate_subproject_to_project"),)

    operations = (
        migrations.DeleteModel(
            name="SubProject",
        ),
    )
