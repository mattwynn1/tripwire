from django.db import models

class Inmate(models.Model):
    last = models.CharField(max_length=50)
    rest = models.CharField(max_length=50)
    crime = models.TextField()
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    race = models.CharField(max_length=1)
    height = models.CharField(max_length=5, null=True, blank=True)
    weight = models.CharField(max_length=5, null=True, blank=True)
    facility = models.CharField(max_length=60, null=True, blank=True)
    admissiondate = models.DateField()
    admissiontime = models.TimeField()
    bond = models.CharField(max_length=60, null=True, blank=True)
    fine = models.CharField(max_length=60, null=True, blank=True)
    freshness = models.CharField(max_length=10)

class Name(models.Model):
    first = models.CharField(max_length=50, null=True, blank=True)
    last = models.CharField(max_length=50)

