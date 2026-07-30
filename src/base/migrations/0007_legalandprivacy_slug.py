from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import migrations, models
from django.utils.text import slugify

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def populate_slugs(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    LegalAndPrivacy = apps.get_model("base", "LegalAndPrivacy")
    existing_slugs: set[str] = set()

    for entry in LegalAndPrivacy.objects.order_by("pk"):
        base_slug = slugify(entry.title_en or entry.title or str(entry.pk))
        slug = base_slug
        counter = 1
        while slug in existing_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        existing_slugs.add(slug)
        entry.slug = slug
        entry.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = (("base", "0006_rename_background_image_to_portrait_image"),)

    operations = (
        migrations.AlterModelOptions(
            name="legalandprivacy",
            options={"ordering": ("id",)},
        ),
        migrations.AddField(
            model_name="legalandprivacy",
            name="slug",
            field=models.SlugField(blank=True, default="", max_length=100),
            preserve_default=False,
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="legalandprivacy",
            name="slug",
            field=models.SlugField(max_length=100, unique=True),
        ),
    )
