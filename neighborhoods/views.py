from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from neighborhoods.models import NycNeighborhood
from neighborhoods.models import NycNeighborhoodSerializer

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.db.models.functions import Area
from django.template import loader
from django.http import HttpResponse

# Create your views here.

class NycNeighborhoodListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        neigh = NycNeighborhood.objects.all()
        serializer = NycNeighborhoodSerializer(neigh, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NycNeighborhoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NycNeighborhoodDetail(APIView):

    def get_object(self, pk):
        job = get_object_or_404(NycNeighborhood, pk=pk)
        return job

    def get(self, request, pk):
        neigh = self.get_object(pk)
        serializer = NycNeighborhoodSerializer(neigh)
        return Response(serializer.data)

    def delete(self, request, pk):
        neigh = self.get_object(pk)
        neigh.delete()
        return Response({"message":"deleted"}, status=status.HTTP_204_NO_CONTENT)

class NycNeighborhoodArea(APIView):
    '''
      SELECT ST_Area(geom)
      FROM nyc_neighborhoods
      WHERE name = 'West Village';
    '''
    def get(self, request):
        neigh_area = NycNeighborhood.objects.filter(name="West Village")[:1].annotate(area=Area('geom'))
        #neigh_area_p = 0
        #for obj in neigh_area:
        #    neigh_area_p = obj.area.sq_m
        #return Response({'area':neigh_area_p})
        return Response({'area': neigh_area[0].area.sq_m})

class NycNeighborhoodIntersects(APIView):
    '''
    SELECT name, boroname
    FROM nyc_neighborhoods
    WHERE ST_Intersects(geom, ST_GeomFromText('POINT(583571 4506714)',26918));
    '''
    def get(self, request):
        neigh_intersects = NycNeighborhood.objects.filter(geom__intersects=(Point(583571, 4506714, srid=26918),
                                                                            D(m=10))).values('name', 'boroname')
        print(neigh_intersects)
        return Response(neigh_intersects)


def map_neigh_view(request, id):
    neigh = NycNeighborhood.objects.annotate(geog=Transform('geom', 4326)).get(gid=id)
    print(neigh.__dict__)
    serializer = NycNeighborhoodSerializer(neigh)
    print(serializer.data)
    template = loader.get_template('neigh_map.html')
    context = {
        'neigh': serializer.data,
    }
    return HttpResponse(template.render(context, request))
