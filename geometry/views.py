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
