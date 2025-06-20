from django.shortcuts import render
from .models import Geometries
from .models import GeometriesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class GeometriesListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        listgeom = Geometries.objects.all()
        serializer = GeometriesSerializer(listgeom, many=True)
        return Response(serializer.data)

'''
In lavorazione - gest. funzioni spaziali non native con django model base
class STNDims(Func):
    function = 'ST_NDims'
    output_field = IntegerField()

class GeometriesListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        listgeom = Geometries.objects.annotate(ndims=STNDims(F('geom'))).values_list('ndims', flat=True)
        #geojson = serialize('geojson', listgeom, geometry_field='geom', fields=('id', 'name', 'geom', 'ndims'))
        #print(geojson)
        #serializer = GeometriesSerializer(listgeom, many=True)
        return Response(listgeom)
'''


