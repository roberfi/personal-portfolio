from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Sequence

if TYPE_CHECKING:
    from django.utils.safestring import SafeString

from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, register
from django.forms.widgets import Select
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin

from home.models import (
    DEFAULT_SERVICE_ICON_PATH,
    SERVICE_ICON_PATHS,
    Education,
    Experience,
    PersonalInfo,
    ProcessStep,
    Project,
    Service,
    Technology,
)


class IconSelectWidget(Select):
    """Select widget that shows an SVG preview of the chosen icon alongside the dropdown."""

    def create_option(self, name: str, value: Any, *args: Any, **kwargs: Any) -> dict[str, Any]:
        option = super().create_option(name, value, *args, **kwargs)
        entry = SERVICE_ICON_PATHS.get(str(value)) if value else None
        option["attrs"]["data-path"] = entry.path if entry else DEFAULT_SERVICE_ICON_PATH.path
        return option

    class Media:
        css: ClassVar = {"all": ("admin/css/icon_select_widget.css",)}
        js: ClassVar = ("admin/js/icon_select_widget.js",)

    def render(self, name: str, value: Any, attrs: dict[str, Any] | None = None, renderer: Any = None) -> SafeString:
        select_html = super().render(name, value, attrs, renderer)
        entry = SERVICE_ICON_PATHS.get(str(value)) if value else None
        current_path = entry.path if entry else DEFAULT_SERVICE_ICON_PATH.path
        return mark_safe(
            render_to_string(
                "admin/widgets/icon_select.html",
                {
                    "select_html": select_html,
                    "current_path": current_path,
                    "default_path": DEFAULT_SERVICE_ICON_PATH.path,
                },
            )
        )


@register(PersonalInfo)
class PersonalInfoAdmin(SingletonModelAdmin):
    filter_horizontal = ("technologies",)


@register(Experience)
class ExperienceAdmin(ModelAdmin[Experience]):
    filter_horizontal = ("technologies",)


@register(Project)
class ProjectAdmin(SortableAdminMixin, ModelAdmin[Project]):  # type: ignore[misc]
    prepopulated_fields: ClassVar[dict[str, Sequence[str]]] = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    list_display = ("title", "featured", "order")
    list_editable = ("featured",)


@register(ProcessStep)
class ProcessStepAdmin(SortableAdminMixin, ModelAdmin[ProcessStep]):  # type: ignore[misc]
    list_display = ("title", "order")

    def formfield_for_dbfield(self, db_field: Any, request: Any, **kwargs: Any) -> Any:
        if db_field.name == "icon_name":
            kwargs["widget"] = IconSelectWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@register(Service)
class ServiceAdmin(SortableAdminMixin, ModelAdmin[Service]):  # type: ignore[misc]
    prepopulated_fields: ClassVar[dict[str, Sequence[str]]] = {"slug": ("title",)}
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active",)

    def formfield_for_dbfield(self, db_field: Any, request: Any, **kwargs: Any) -> Any:
        if db_field.name == "icon_name":
            kwargs["widget"] = IconSelectWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@register(Education)
class EducationAdmin(ModelAdmin[Education]):
    pass


@register(Technology)
class TechnologyAdmin(SortableAdminMixin, ModelAdmin[Technology]):  # type: ignore[misc]
    list_display = ("name", "priority")
