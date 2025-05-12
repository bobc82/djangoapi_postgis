from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from census_blocks.models import NycCensusBlocks
from census_blocks.models import NycCensusBlocksSerializer

class NycCensusBlocksListCreateAPIView(APIView):

    def get(self, request):
        print(request)
        censlist = NycCensusBlocks.objects.all().order_by("gid")[:10]
        serializer = NycCensusBlocksSerializer(censlist, many=True)
        return Response(serializer.data)
