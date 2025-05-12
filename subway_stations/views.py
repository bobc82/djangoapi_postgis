from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from subway_stations.models import NycSubwayStations
from subway_stations.models import NycSubwayStationsSerializer

class NycSubwayStationsListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        subways = NycSubwayStations.objects.all().order_by("gid")[:10]
        serializer = NycSubwayStationsSerializer(subways, many=True)
        return Response(serializer.data)