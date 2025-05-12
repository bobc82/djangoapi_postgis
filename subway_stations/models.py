from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from rest_framework import serializers


# Create your models here.
class NycSubwayStations(models.Model):
    gid = models.BigAutoField(primary_key=True)
    objectid = models.IntegerField()
    id = models.FloatField()
    name = models.CharField(max_length=31)
    alt_name = models.CharField(null=True, max_length=38)
    cross_st = models.CharField(null=True, max_length=27)
    long_name = models.CharField(max_length=60)
    label = models.CharField(max_length=50)
    borough = models.CharField(max_length=15)
    nghbhd = models.CharField(null=True, max_length=30)
    routes = models.CharField(max_length=20)
    transfers = models.CharField(max_length=25)
    color = models.CharField(max_length=30)
    express = models.CharField(null=True, max_length=10)
    closed = models.CharField(null=True, max_length=10)
    geom = models.MultiPolygonField(srid=26918)

    '''
    def __str__(self):
        return self.name
    '''

    class Meta:
        db_table = 'nyc_subway_stations'

class NycSubwayStationsSerializer(serializers.ModelSerializer):
    geog = serializers.SerializerMethodField()

    class Meta:
        model = NycSubwayStations
        fields = ('gid', 'objectid', 'id', 'name', 'alt_name', 'cross_st', 'long_name', 'label', 'borough',
                  'nghbhd', 'routes', 'transfers', 'color', 'express', 'closed', 'geom', 'geog')  # Add the additional field

    def get_geog(self, obj):
        if obj.geom:
            return obj.geom.transform(4326, clone=True).geojson  # Convert to GeoJSON
        return None
