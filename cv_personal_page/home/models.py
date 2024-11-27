from __future__ import annotations

import datetime
from functools import cached_property
from typing import NamedTuple

from django.db import models
from django.utils.translation import ngettext


# TODO: make row unique
class PersonalInfo(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    biography = models.TextField()


class Experience(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    @cached_property
    def actual_end_date(self) -> datetime.date:
        return self.end_date or datetime.date.today()

    @cached_property
    def __total_days(self) -> int:
        return (self.actual_end_date - self.start_date).days

    class _YearsAndMonths(NamedTuple):
        years: int
        months: int

    @cached_property
    def __years_and_months(self) -> _YearsAndMonths:
        years = int(self.__total_days / 365)

        months = self.actual_end_date.month - self.start_date.month + 1

        # If substraction is negative, we have to sum one year
        if self.actual_end_date.month < self.start_date.month:
            months += 12

        return self._YearsAndMonths(years, months)

    @cached_property
    def duration(self) -> str:
        years, months = self.__years_and_months
        parts = (
            ngettext("%d year", "%d years", years) % years if years else "",
            ngettext("%d month", "%d months", months) % months if months else "",
        )

        return ", ".join((p for p in parts if p))
