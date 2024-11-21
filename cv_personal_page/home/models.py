from django.db import models


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
    end_date = models.DateField(null=True)
