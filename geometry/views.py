from django.shortcuts import render
from .models import Geometries
from .models import GeometriesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Func, F, IntegerField
from rest_framework import status
from rest_framework import serializers

from drf_spectacular.utils import extend_schema, OpenApiParameter

class MyRequestSerializer(serializers.Serializer):
    nome = serializers.CharField()


# Create your views here.
class SimulazioneAPIView(APIView):

    @extend_schema(
        #request=MyRequestSerializer, #Ad esempio ho un JSON nel body nel caso di una richiesta POST
        summary="API futura: ricerca semantica",
        description="Questa API restituirà risultati di ricerca basati su NLP.",
        responses={status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN},
    )
    def get(self, request):
        return Response(status=501)  # 501 Not Implemented

class SimulazionePostAPIView(APIView):

    @extend_schema(
        request=MyRequestSerializer, #Ad esempio ho un JSON nel body nel caso di una richiesta POST
        summary="API futura: ricerca semantica con parametri su POST request",
        description="Questa API restituirà risultati di ricerca basati su NLP.",
        responses={status.HTTP_200_OK},
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


