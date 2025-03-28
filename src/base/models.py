from __future__ import annotations

from functools import cached_property

from django.db import models
from django_cooco.models import CookieGroup
from solo.models import SingletonModel


class LegalAndPrivacy(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()

    def __str__(self) -> str:
        return self.title

    @cached_property
    def modal_name(self) -> str:
        return f"legal_and_privacy_{self.id}_modal"


class FollowMeLink(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField()
    svg_view_box = models.CharField(max_length=16)
    svg_path = models.TextField()

    def __str__(self) -> str:
        return self.name


class GoogleAnalytics(SingletonModel):
    use_analytics = models.BooleanField(default=False)
    gtag = models.CharField(max_length=20, blank=True)
    cookie_consent = models.ForeignKey(CookieGroup, on_delete=models.RESTRICT, null=True)
    debug_mode = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Google Analytics"
