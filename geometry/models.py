from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from rest_framework import serializers


# Create your models here.
class Geometries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    geom = models.GeometryField()

    class Meta:
        db_table = 'geometries'
