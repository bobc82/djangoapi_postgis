from django.contrib.gis.db import models
from rest_framework import serializers


# Create your models here.
class NycStreet(models.Model):
    gid = models.BigAutoField(primary_key=True)
    id = models.FloatField()
    name = models.CharField(max_length=200)
    oneway = models.CharField(null=True, max_length=10)
    type = models.CharField(max_length=50)
    geom = models.MultiPolygonField(srid=26918)

    '''
    def __str__(self):
        return self.name
    '''

    class Meta:
        db_table = 'nyc_streets'


class NycStreetSerializer(serializers.ModelSerializer):
    geog = serializers.SerializerMethodField()

    class Meta:
        model = NycStreet
        fields = ('gid', 'name', 'oneway', 'type', 'geom', 'geog')  # Add the additional field

    def get_geog(self, obj):
        if obj.geom:
            return obj.geom.transform(4326, clone=True).geojson  # Convert to GeoJSON
        return None
