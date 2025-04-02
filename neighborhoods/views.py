from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from neighborhoods.models import NycNeighborhood
from neighborhoods.models import NycNeighborhoodSerializer

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
