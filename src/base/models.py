from functools import cached_property

from django.db import models


class LegalAndPrivacy(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()

    def __str__(self) -> str:
        return self.title

    @cached_property
    def modal_name(self) -> str:
        return f"{self.title.lower().replace(" ", "_")}_modal"