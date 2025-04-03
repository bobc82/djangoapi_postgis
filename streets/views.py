from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from streets.models import NycStreet
from streets.models import NycStreetSerializer
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

class NycStreetListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        neigh = NycStreet.objects.all().order_by("gid")[:10]
        serializer = NycStreetSerializer(neigh, many=True)
        return Response(serializer.data)

def map_view(request):
    street = NycStreet.objects.get(gid=1)
    serializer = NycStreetSerializer(street)
    print(serializer.data)
    template = loader.get_template('street_map.html')
    context = {
        'street': serializer.data,
    }
    return HttpResponse(template.render(context, request))
