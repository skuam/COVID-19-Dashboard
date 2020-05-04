from django.db import models


class Country(models.Model):
    Country = models.CharField(max_length=150)
    Date = models.DateField()
    Infected = models.IntegerField()
    Recoverd = models.IntegerField()
    Dead = models.IntegerField()
