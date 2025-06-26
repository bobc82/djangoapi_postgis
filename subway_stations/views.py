from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from census_blocks.models import NycCensusBlocks
from subway_stations.models import NycSubwayStations
from subway_stations.models import NycSubwayStationsSerializer
from neighborhoods.models import NycNeighborhood

from django.contrib.gis.db.models.functions import Transform
from django.template import loader
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models import F
import json

class NycSubwayStationsListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        subways = NycSubwayStations.objects.all().order_by("gid")[:10]
        serializer = NycSubwayStationsSerializer(subways, many=True)
        return Response(serializer.data)

class FindNeighborhoodsInSubway(APIView):
    '''
    SELECT
      subways.name AS subway_name,
      neighborhoods.name AS neighborhood_name,
      neighborhoods.boroname AS borough
    FROM nyc_neighborhoods AS neighborhoods
    JOIN nyc_subway_stations AS subways
    ON ST_Contains(neighborhoods.geom, subways.geom)
    WHERE subways.name = 'Broad St';
    '''
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
    '''
        SELECT
        geog
        FROM nyc_subway_station
        WHERE name = 'Broad St';
    '''
    def get(self, request):
        station_geog = NycSubwayStations.objects.get(name='Broad St')
        serializer = NycSubwayStationsSerializer(station_geog, many=False)
        print(serializer.data)
        return Response({'geog': json.loads(serializer.data['geog'])})

class NycRoutesFromStations(APIView):
    '''
    SELECT DISTINCT routes
    FROM nyc_subway_stations;
    '''
    def get(self, request):
        routes = NycSubwayStations.objects.values('routes').distinct()
        print(routes)
        return Response(routes)

class NycPopulationFromTrainStop(APIView):
    '''
    SELECT
      100*SUM(c.popn_white)/SUM(c.popn_total) AS white_pct,
      100*SUM(c.popn_black)/SUM(c.popn_total) AS black_pct,
      SUM(popn_total) AS popn_total
    FROM nyc_census_blocks AS c
    JOIN nyc_subway_stations AS s
      ON ST_DWithin(
        c.geom,
        s.geom,
        200
      )
    WHERE strpos(s.routes,'A') > 0;
    '''
    def get(self, request):
        subway_stations = NycSubwayStations.objects.filter(routes__contains='A')
        popn_white_total = 0
        popn_black_total = 0
        popn_total_t = 0
        for s in subway_stations:
            census_blocks = NycCensusBlocks.objects.filter(geom__dwithin=(s.geom, 200)).aggregate(Sum('popn_total'), Sum('popn_white'), Sum('popn_black'))
            popn_total_t = popn_total_t + census_blocks["popn_total__sum"]
            popn_white_total = popn_white_total + census_blocks["popn_white__sum"]
            popn_black_total = popn_black_total + census_blocks["popn_black__sum"]
        r_make_up = {"white_pct": 100 * (popn_white_total / popn_total_t),
                     "black_pct": 100 * (popn_black_total / popn_total_t),
                     "popn_total": popn_total_t}
        return Response(r_make_up)

def map_view(request, id):
    subway = NycSubwayStations.objects.annotate(geog=Transform('geom', 4326)).get(gid=id)
    print(subway.__dict__)
    serializer = NycSubwayStationsSerializer(subway)
    print(serializer.data)
    template = loader.get_template('subway.html')
    context = {
        'subway': serializer.data,
    }
    return HttpResponse(template.render(context, request))