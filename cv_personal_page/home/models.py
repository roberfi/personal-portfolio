from django.db import models


# TODO: make row unique
class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()


class Experience(models.Model):
    title = models.CharField(max_length=200)
    # TODO: location = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
