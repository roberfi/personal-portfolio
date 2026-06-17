from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = (("home", "0009_education_remove_experience_company_and_more"),)

    operations = (
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("title_en", models.CharField(max_length=200, null=True)),
                ("title_es", models.CharField(max_length=200, null=True)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("problem", models.TextField()),
                ("problem_en", models.TextField(null=True)),
                ("problem_es", models.TextField(null=True)),
                ("approach", models.TextField()),
                ("approach_en", models.TextField(null=True)),
                ("approach_es", models.TextField(null=True)),
                ("outcome", models.TextField()),
                ("outcome_en", models.TextField(null=True)),
                ("outcome_es", models.TextField(null=True)),
                ("hero_image", models.ImageField(blank=True, null=True, upload_to="projects/")),
                ("featured", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
                ("technologies", models.ManyToManyField(blank=True, related_name="projects", to="home.technology")),
            ],
            options={
                "ordering": ("order", "title"),
            },
        ),
    )
