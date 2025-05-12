from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from rest_framework import serializers


# Create your models here.
class NycCensusBlocks(models.Model):
    gid = models.BigAutoField(primary_key=True)
    blkid = models.CharField(max_length=15)
    popn_total = models.FloatField()
    popn_white = models.FloatField()
    popn_black = models.FloatField()
    popn_nativ = models.FloatField()
    popn_asian = models.FloatField()
    popn_other = models.FloatField()
    boroname = models.CharField(max_length=32)
    geom = models.MultiPolygonField(srid=26918)

    class Meta:
        db_table = 'nyc_census_blocks'

class NycCensusBlocksSerializer(serializers.ModelSerializer):
    geog = serializers.SerializerMethodField()

    class Meta:
        model = NycCensusBlocks
        fields = ('gid', 'blkid', 'popn_total', 'popn_white', 'popn_black', 'popn_nativ', 'popn_asian', 'popn_other', 'boroname',
                 'geom', 'geog')  # Add the additional field

    def get_geog(self, obj):
        if obj.geom:
            return obj.geom.transform(4326, clone=True).geojson  # Convert to GeoJSON
        return None
