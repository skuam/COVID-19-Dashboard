from django.db import models

from django_pandas.managers import DataFrameManager

class Country(models.Model):
    Country = models.CharField(max_length=150)
    Date = models.DateField()
    Infected = models.IntegerField()
    Recovered = models.IntegerField()
    Dead = models.IntegerField()

    objects = DataFrameManager()
