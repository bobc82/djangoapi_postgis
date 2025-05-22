from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from census_blocks.models import NycCensusBlocks
from census_blocks.models import NycCensusBlocksSerializer
from neighborhoods.models import NycNeighborhood
from django.db.models import Sum

class NycCensusBlocksListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        censlist = NycCensusBlocks.objects.all().order_by("gid")[:10]
        serializer = NycCensusBlocksSerializer(censlist, many=True)
        return Response(serializer.data)

class NycPopulationAPIView(APIView):

    def get(self, request):
        population = NycCensusBlocks.objects.aggregate(Sum("popn_total"))
        print(population)
        return Response(population)

class NycCensusNeighPopulation(APIView):
    '''
    SELECT
      neighborhoods.name,
      Sum(census.popn_total) AS population,
        FROM nyc_neighborhoods AS neighborhoods
        JOIN nyc_census_blocks AS census
        ON ST_Intersects(neighborhoods.geom, census.geom)
        WHERE neighborhoods.boroname = 'Manhattan'
        GROUP BY neighborhoods.name
    '''
    def get(self, request):
        neighborhoods = NycNeighborhood.objects.filter(boroname='Manhattan').order_by('name')

        population_list = []
        for n in neighborhoods:
            #print({'name':n.name})
            census_blocks = NycCensusBlocks.objects.filter(geom__intersects=n.geom).aggregate(Sum('popn_total'))
            #for c in census_blocks:
            print(census_blocks)
            population_list.append({'name': n.name, 'population':census_blocks['popn_total__sum']})

        return Response(population_list)
