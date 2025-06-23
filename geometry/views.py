from django.shortcuts import render
from .models import Geometries
from .models import GeometriesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Func, F, IntegerField

# Create your views here.

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



