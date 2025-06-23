from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from rest_framework import serializers
from django.db.models import Func, F, IntegerField


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

    def get_srid(self, obj):
        if obj.geom:
            return obj.geom.srid
        return None

    def get_ndims(self, obj):
        return getattr(obj, 'ndims', None)

    class Meta:
        model = Geometries
        fields = ('id', 'name', 'geom', 'srid', 'ndims')
