from __future__ import annotations

import datetime
from functools import cached_property
from typing import TYPE_CHECKING, NamedTuple

from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import date as datefilter
from django.utils.translation import gettext, ngettext
from django.utils.translation import gettext_lazy as _
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
    icon_name = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)

    def __str__(self) -> str:
        return self.title


class Education(DatedModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Education entries"

    def __str__(self) -> str:
        return gettext("%(title)s at %(institution)s") % {"title": self.title, "institution": self.institution}
