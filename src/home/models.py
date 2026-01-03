from __future__ import annotations

import datetime
from functools import cached_property
from typing import NamedTuple

from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import date as datefilter
from django.utils.translation import gettext, ngettext
from solo.models import SingletonModel


class Technology(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    name = models.CharField(max_length=100, unique=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ("priority", "name")

    def __str__(self) -> str:
        return f"{self.name} (Priority: {self.priority})"


class PersonalInfo(SingletonModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    introduction = models.TextField(max_length=500)
    biography = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, related_name="personal_info")

    def __str__(self) -> str:
        return self.name


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


class SubProject(DatedModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="sub_projects")
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, related_name="sub_projects")

    class Meta:
        ordering = ("-start_date",)

    def __str__(self) -> str:
        if self.client:
            return f"{self.title} - {self.client}"
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
