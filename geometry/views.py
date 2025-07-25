from django.shortcuts import render
from .models import Geometries
from .models import GeometriesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Func, F, IntegerField
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.types import OpenApiTypes

from drf_spectacular.utils import extend_schema, OpenApiParameter

class MyRequestSerializer(serializers.Serializer):
    nome = serializers.CharField()


# Create your views here.
class SimulazioneAPIView(APIView):

    @extend_schema(
        #request=MyRequestSerializer, #Ad esempio ho un JSON nel body nel caso di una richiesta POST
        summary="API futura: ricerca semantica",
        description="Questa API restituirà risultati di ricerca basati su NLP.",
        tags=["v1 - geometry"],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response(status=501)  # 501 Not Implemented

class SimulazionePostAPIView(APIView):

    @extend_schema(
        request=MyRequestSerializer, #Ad esempio ho un JSON nel body nel caso di una richiesta POST
        summary="API Protetta - Richiede Token JWT",
        description="Questa API restituirà risultati di ricerca basati su NLP. Solo per utenti con permesso `can_view_reports`",
        tags=["v1 - geometry"],
        responses={200: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        return Response(status=501)  # 501 Not Implemented

class SimulazionePostAPIViewFutura(APIView):

    @extend_schema(
        request=MyRequestSerializer, #Ad esempio ho un JSON nel body nel caso di una richiesta POST
        summary="API Protetta - Richiede Token JWT - Versione 2",
        description="Questa API restituirà risultati di ricerca basati su NLP. Solo per utenti con permesso `can_view_reports`",
        tags=["v2 - geometry"],
        responses={200: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        return Response(status=501)  # 501 Not Implemented

class GeometriesListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        listgeom = Geometries.objects.annotate(ndims=STNDims(F('geom'))).all()
        print(listgeom)
        serializer = GeometriesSerializer(listgeom, many=True)
        print(serializer.data)
        return Response(serializer.data)


#In lavorazione - gest. funzioni spaziali non native con django model base
class STNDims(Func):
    function = 'ST_NDims'
    output_field = IntegerField()



class GeometriesListSearchAPIView(APIView):

    def get(self, request, **kwargs):
        search_str = self.kwargs.get("search")
        print(search_str)
        listgeom = Geometries.objects.annotate(ndims=STNDims(F('geom'))).filter(name__icontains=search_str)
        print(listgeom)
        serializer = GeometriesSerializer(listgeom, many=True)
        print(serializer.data)
        return Response(serializer.data)


