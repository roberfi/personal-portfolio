from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import migrations
from django.utils.text import slugify

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def migrate_subprojects_to_projects(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    SubProject = apps.get_model("home", "SubProject")
    Project = apps.get_model("home", "Project")

    existing_slugs = set(Project.objects.values_list("slug", flat=True))

    for order, subproject in enumerate(SubProject.objects.order_by("pk").prefetch_related("technologies"), start=1):
        base_slug = slugify(subproject.title_en or subproject.title or str(subproject.pk))
        slug = base_slug
        counter = 1
        while slug in existing_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        existing_slugs.add(slug)

        project = Project.objects.create(
            title=subproject.title,
            title_en=subproject.title_en,
            title_es=subproject.title_es,
            slug=slug,
            problem=subproject.description,
            problem_en=subproject.description_en,
            problem_es=subproject.description_es,
            approach="",
            outcome="",
            featured=False,
            order=order,
        )
        project.technologies.set(subproject.technologies.all())


class Migration(migrations.Migration):
    dependencies = (("home", "0010_create_project"),)

    operations = (migrations.RunPython(migrate_subprojects_to_projects, migrations.RunPython.noop),)
