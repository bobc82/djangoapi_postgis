from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from census_sociodata.models import NycCensusSociodata
from census_sociodata.models import NycCensusSociodataSerializer

class NycCensusSociodataListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        censsocio = NycCensusSociodata.objects.all().order_by("tractid")[:10]
        serializer = NycCensusSociodataSerializer(censsocio, many=True)
        return Response(serializer.data)
