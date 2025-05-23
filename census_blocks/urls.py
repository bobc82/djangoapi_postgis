from django.urls import path
from . import views

urlpatterns = [
    path('blocks/', views.NycCensusBlocksListCreateAPIView.as_view(), name='census_blocks'),
    path('population/', views.NycCensusNeighPopulation.as_view(), name='census_neigh_population'),
    path('nycPopulation/', views.NycPopulationAPIView.as_view(), name='nyc_population')
    #path("censusBlocks/",NycCensusBlocksListCreateAPIView.as_view(),name="census_blocks"),
    #path("censusBlocksPopulation/",NycCensusNeighPopulation.as_view(),name="census_neigh_population"),
    #path("nycPopulation/", NycPopulationAPIView.as_view(), name="nyc_population"),
]