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

# Create your views here.

class NycStreetListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        neigh = NycStreet.objects.all().order_by("gid")[:10]
        serializer = NycStreetSerializer(neigh, many=True)
        return Response(serializer.data)

class NycStreetLength(APIView):

    def get(self, request):
        street_length = NycStreet.objects.filter(name="Pelham St")[:1].annotate(length=Length('geom'))
        return Response({'l': street_length[0].length.m})

class NycStreetTotalLength(APIView):

    def get(self, request):
        street_length = NycStreet.objects.annotate(length=Length('geom')).aggregate(Sum("length"))
        print(street_length)
        return Response({'l': street_length['length__sum'].m})

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
