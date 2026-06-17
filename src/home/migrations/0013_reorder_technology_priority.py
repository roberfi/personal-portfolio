from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import migrations

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def reorder_technology_priority(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Technology = apps.get_model("home", "Technology")
    for priority, tech in enumerate(Technology.objects.order_by("priority", "name"), start=1):
        if tech.priority != priority:
            tech.priority = priority
            tech.save(update_fields=["priority"])


class Migration(migrations.Migration):
    dependencies = (("home", "0012_delete_subproject"),)

    operations = (migrations.RunPython(reorder_technology_priority, migrations.RunPython.noop),)
