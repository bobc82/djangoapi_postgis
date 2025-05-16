from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from subway_stations.models import NycSubwayStations
from subway_stations.models import NycSubwayStationsSerializer
from neighborhoods.models import NycNeighborhood
from django.db.models import F

class NycSubwayStationsListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        subways = NycSubwayStations.objects.all().order_by("gid")[:10]
        serializer = NycSubwayStationsSerializer(subways, many=True)
        return Response(serializer.data)

class FindNeighborhoodsInSubway(APIView):

    def get(self, request):
        # Get the subway station named 'Broad St'
        station = NycSubwayStations.objects.get(name='Broad St')

        # Find all neighborhoods that contain this station
        neighborhoods = NycNeighborhood.objects.filter(geom__contains=station.geom)

        # Combine the data
        list_neigh = []
        for neighborhood in neighborhoods:
            dict_n = {
                'subway_name': station.name,
                'neighborhood_name': neighborhood.name,
                'borough': neighborhood.boroname
            }
            print(dict_n)
            list_neigh.append(dict_n)


        return Response(list_neigh)

class NycSubwayGetGeog(APIView):

    def get(self, request):
        station_geog = NycSubwayStations.objects.get(name='Broad St')
        serializer = NycSubwayStationsSerializer(station_geog, many=False)
        print(serializer.data)
        return Response({'geog': serializer.data['geog']})