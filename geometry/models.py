from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from rest_framework import serializers
from django.db.models import Func, F, IntegerField
from django.contrib.gis.db.models.functions import Area, Perimeter


# Create your models here.
class Geometries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    geom = models.GeometryField()

    class Meta:
        db_table = 'geometries'


class GeometriesSerializer(serializers.ModelSerializer):
    srid = serializers.SerializerMethodField()
    ndims = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    perimeter = serializers.SerializerMethodField()

    def get_srid(self, obj):
        if obj.geom:
            return obj.geom.srid
        return None

    def get_ndims(self, obj):
        return getattr(obj, 'ndims', None)

    def get_area(self, obj):
        if obj.geom:
            return obj.geom.area
        return None

    def get_perimeter(self, obj):
        if obj.geom:
            return obj.geom.length
        return None

    class Meta:
        model = Geometries
        fields = ('id', 'name', 'geom', 'srid', 'ndims', 'area', 'perimeter')
