from django.contrib.gis.db import models
from rest_framework import serializers

# Create your models here.
class NycNeighborhood(models.Model):
    gid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=43)
    boroname = models.CharField(max_length=64)
    geom = models.MultiPolygonField(srid=26918)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nyc_neighborhoods'

class NycNeighborhoodSerializer(serializers.ModelSerializer):
    geog = serializers.SerializerMethodField()

    class Meta:
        model = NycNeighborhood
        fields = ('gid', 'name', 'boroname', 'geom', 'geog')

    def get_geog(self, obj):
        if obj.geom:
            return obj.geom.transform(4326, clone=True).geojson  # Convert to GeoJSON
        return None