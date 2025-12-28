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
        return self.name


class PersonalInfo(SingletonModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    introduction = models.TextField(max_length=500)
    biography = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, related_name="personal_info")

    def __str__(self) -> str:
        return self.name


class Experience(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True, related_name="experiences")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return gettext("%(job)s at %(company)s") % {"job": self.title, "company": self.company}

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
