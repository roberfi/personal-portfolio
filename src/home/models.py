from __future__ import annotations

import datetime
from functools import cached_property
from typing import TYPE_CHECKING, NamedTuple

from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import date as datefilter
from django.utils.translation import gettext, ngettext
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from solo.models import SingletonModel

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise


class Technology(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    name = models.CharField(max_length=100, unique=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ("priority", "name")

    def __str__(self) -> str:
        return self.name


class PersonalInfo(SingletonModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    introduction = models.TextField(max_length=500)
    biography = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, related_name="personal_info")

    @cached_property
    def technology_names(self) -> tuple[str, ...]:
        """Return a tuple of technology names associated with this personal info."""
        return tuple(tech.name for tech in self.technologies.all())

    def __str__(self) -> str:
        """Return the string representation of the PersonalInfo."""
        return self.name

    def get_page_title(self) -> str:
        """Return the page title for SEO purposes."""
        return f"{self.name} | {self.title}"

    def get_page_description(self) -> str:
        """Return the page description for SEO purposes."""
        description = gettext("Personal web of %(name)s. %(title)s") % {
            "name": self.name,
            "title": self.title,
        }

        if self.technologies.exists():
            description += " " + gettext("specialized in %(tech)s") % {
                "tech": ", ".join(self.technology_names[:3]),
            }

        return description

    def get_page_keywords(self) -> str:
        """Return the page keywords for SEO purposes."""
        return ", ".join(tech.lower() for tech in self.technology_names)


class DatedModel(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    def clean(self) -> None:
        if self.end_date and self.end_date < self.start_date:
            error_message = gettext("End date must be after start date")
            raise ValidationError(error_message, code="invalid_dates")

    @cached_property
    def actual_end_date(self) -> datetime.date:
        return self.end_date or datetime.date.today()

    @cached_property
    def period(self) -> str:
        start_date = datefilter(self.start_date, "M, Y")
        end_date = datefilter(self.end_date, "M, Y") if self.end_date else gettext("Present")

        return f"{start_date} - {end_date}"

    class _YearsAndMonths(NamedTuple):
        years: int
        months: int

    @cached_property
    def __years_and_months(self) -> _YearsAndMonths:
        years = self.actual_end_date.year - self.start_date.year
        months = self.actual_end_date.month - self.start_date.month

        # Adjust for negative months (when end month is earlier in the year than start month)
        if months < 0:
            years -= 1
            months += 12

        return self._YearsAndMonths(years, months)

    @cached_property
    def duration(self) -> str:
        if self.start_date > datetime.date.today():
            return gettext("Not yet started")

        years, months = self.__years_and_months

        if years == 0 and months == 0:
            return gettext("Less than a month")

        parts = (
            ngettext("%d year", "%d years", years) % years if years else "",
            ngettext("%d month", "%d months", months) % months if months else "",
        )

        return ", ".join((p for p in parts if p))


class Experience(DatedModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, blank=True, verbose_name="Company")
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, related_name="experiences")

    def __str__(self) -> str:
        if self.institution:
            return gettext("%(title)s at %(institution)s") % {"title": self.title, "institution": self.institution}

        return self.title


class Project(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.CharField(max_length=200, help_text="Short, problem-oriented excerpt shown on project cards.")
    problem = models.TextField()
    approach = models.TextField()
    outcome = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, related_name="projects")
    hero_image = models.ImageField(upload_to="projects/", blank=True, null=True)

    # Card thumbnail — keeps the listing/featured grids light
    card_image = ImageSpecField(
        source="hero_image",
        processors=[SmartResize(400, 225)],
        format="WEBP",
        options={"quality": 80},
    )

    # Larger 16:9 render for the project detail hero.
    hero_display = ImageSpecField(
        source="hero_image",
        processors=[SmartResize(1600, 900)],
        format="WEBP",
        options={"quality": 85},
    )

    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "title")

    def __str__(self) -> str:
        return self.title


# Heroicon (outline, 24x24) SVG paths keyed by a short, human-friendly name. The
# name is chosen in the admin via Service.icon_name; blank or unknown names fall
# back to DEFAULT_SERVICE_ICON_PATH. This mirrors the raw-path convention already
# used by the c-heading component.
class ServiceIconPaths(NamedTuple):
    name: StrOrPromise
    path: str


SERVICE_ICON_PATHS: dict[str, ServiceIconPaths] = {
    "code": ServiceIconPaths(
        name=_("Code"),
        path="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4",
    ),
    "server": ServiceIconPaths(
        name=_("Server"),
        path=(
            "M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2"
            "M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"
        ),
    ),
    "lightning": ServiceIconPaths(
        name=_("Lightning"),
        path="M13 10V3L4 14h7v7l9-11h-7z",
    ),
    "chat": ServiceIconPaths(
        name=_("Chat"),
        path=(
            "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949"
            "L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
        ),
    ),
    "globe": ServiceIconPaths(
        name=_("Globe"),
        path=(
            "M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9"
            "s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"
        ),
    ),
    "briefcase": ServiceIconPaths(
        name=_("Briefcase"),
        path=(
            "M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2"
            "h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
        ),
    ),
    "chart": ServiceIconPaths(
        name=_("Chart"),
        path=(
            "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2"
            "h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14"
            "a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
        ),
    ),
    "shield": ServiceIconPaths(
        name=_("Shield"),
        path=(
            "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04"
            "A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042"
            "-.133-2.052-.382-3.016z"
        ),
    ),
    "search": ServiceIconPaths(
        name=_("Search"),
        path="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
    ),
    "clock": ServiceIconPaths(
        name=_("Clock"),
        path="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
    ),
    "cog": ServiceIconPaths(
        name=_("Cog"),
        path=(
            "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066"
            "c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35"
            "a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065"
            "c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37"
            "a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573"
            "c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065zM15 12a3 3 0 11-6 0 3 3 0 016 0z"
        ),
    ),
    "pencil": ServiceIconPaths(
        name=_("Pencil"),
        path="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z",
    ),
    "sparkles": ServiceIconPaths(
        name=_("Sparkles"),
        path="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z",
    ),
    "eye": ServiceIconPaths(
        name=_("Eye"),
        path=(
            "M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            "M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7"
            "-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
        ),
    ),
    "phone": ServiceIconPaths(
        name=_("Phone"),
        path=(
            "M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21"
            "l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502"
            "l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 7V5z"
        ),
    ),
    "document": ServiceIconPaths(
        name=_("Document"),
        path=(
            "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293"
            "l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        ),
    ),
}

DEFAULT_SERVICE_ICON_PATH = ServiceIconPaths(
    name=_("— default (check-circle) —"),
    path="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
)

SERVICE_ICON_CHOICES = (
    ("", DEFAULT_SERVICE_ICON_PATH.name),
    *((k, v.name) for k, v in SERVICE_ICON_PATHS.items()),
)


class Service(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField()
    icon_name = models.CharField(max_length=100, blank=True, choices=SERVICE_ICON_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "title")

    def __str__(self) -> str:
        return self.title

    @cached_property
    def icon_path(self) -> str:
        """Return the SVG path for the service icon, falling back to a default."""
        return SERVICE_ICON_PATHS.get(self.icon_name, DEFAULT_SERVICE_ICON_PATH).path


class ProcessStep(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_name = models.CharField(max_length=100, blank=True, choices=SERVICE_ICON_CHOICES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)

    def __str__(self) -> str:
        return self.title

    @cached_property
    def icon_path(self) -> str:
        return SERVICE_ICON_PATHS.get(self.icon_name, DEFAULT_SERVICE_ICON_PATH).path


class Education(DatedModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Education entries"

    def __str__(self) -> str:
        return gettext("%(title)s at %(institution)s") % {"title": self.title, "institution": self.institution}
