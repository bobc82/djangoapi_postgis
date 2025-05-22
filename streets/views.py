from django.contrib.gis.geos import Point
from django.contrib.gis.geos import LineString
from django.contrib.gis.measure import D
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from streets.models import NycStreet
from streets.models import NycStreetSerializer
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.db.models.functions import Length
from django.db.models import Sum
from django.db.models import Count

# Create your views here.

class NycStreetListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        neigh = NycStreet.objects.all().order_by("gid")[:10]
        serializer = NycStreetSerializer(neigh, many=True)
        return Response(serializer.data)

class NycStreetLength(APIView):
    '''
      SELECT ST_Length(geom)
      FROM nyc_streets
      WHERE name = 'Columbus Cir';
    '''
    def get(self, request):
        street_length = NycStreet.objects.filter(name="Pelham St")[:1].annotate(length=Length('geom'))
        return Response({'l': street_length[0].length.m})

class NycStreetTotalLength(APIView):
    '''
    SELECT Sum(ST_Length(geom))
    FROM nyc_streets;
    '''
    def get(self, request):
        street_length = NycStreet.objects.annotate(length=Length('geom')).aggregate(Sum("length"))
        print(street_length)
        return Response({'l': street_length['length__sum'].m})

class NycStreetFilterWithin(APIView):
    '''
    SELECT name
    FROM nyc_streets
    WHERE ST_DWithin(
            geom,
            ST_GeomFromText('POINT(583571 4506714)',26918),
            10
          );
    '''
    def get(self, request):
        streets_within = NycStreet.objects.filter(geom__dwithin=(Point(583571, 4506714, srid=26918), D(m=10))).values_list('name')
        print(streets_within)
        return Response(streets_within)

class NycStreetGeometryValue(APIView):
    '''
    SELECT
    ST_AsText(geom)
    FROM
    nyc_streets
    WHERE
    name = 'Atlantic Commons';
    '''
    def get(self, request):
        street = NycStreet.objects.get(name='Atlantic Commons').geom
        print(street)
        return Response({'geom':str(street)})

class NycStreetsIntersectMeridian(APIView):
    '''
    SELECT Count(*)
    FROM nyc_streets
    WHERE ST_Intersects(
      ST_Transform(geom, 4326),
      'SRID=4326;LINESTRING(-74 20, -74 60)'
      );
    '''
    def get(self, request):
        count_meridian = NycStreet.objects.annotate(geog=Transform('geom', 4326)).filter(geog__intersects=LineString((-74, 20), (-74, 60), srid=4326)).count()
        print(count_meridian)
        return Response({'count': count_meridian})


def map_view(request, id):
    street = NycStreet.objects.annotate(geog=Transform('geom', 4326)).get(gid=id)
    print(street.__dict__)
    serializer = NycStreetSerializer(street)
    print(serializer.data)
    template = loader.get_template('street_map.html')
    context = {
        'street': serializer.data,
    }
    return HttpResponse(template.render(context, request))
