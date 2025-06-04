"""
URL configuration for django_postgis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import neighborhoods.views
import streets.views
from neighborhoods.views import NycNeighborhoodListCreateAPIView, NycNeighborhoodDetail, NycSharedTopoElementsAsView
from streets.views import NycStreetListCreateAPIView
from streets.views import NycStreetLength
from streets.views import NycStreetTotalLength
from streets.views import NycStreetFilterWithin
from streets.views import NycStreetGeometryValue
from streets.views import NycStreetsIntersectMeridian
from streets.views import NycStreetsNearest
from streets.views import NycStreetsNearestAll
from subway_stations.views import NycSubwayStationsListCreateAPIView
from subway_stations.views import FindNeighborhoodsInSubway
from subway_stations.views import NycSubwayGetGeog
from neighborhoods.views import NycNeighborhoodArea
from neighborhoods.views import NycNeighborhoodIntersects
from neighborhoods.views import NycSharedTopoElements
from census_sociodata.views import NycCensusSociodataListCreateAPIView
from geometry.views import GeometriesListCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("neighborhoods/",NycNeighborhoodListCreateAPIView.as_view(),name="neighborhoods"),
    path("neighborhoodArea/",NycNeighborhoodArea.as_view(),name="neighborhood_area"),
    path("neighborhoodIntersects/",NycNeighborhoodIntersects.as_view(),name="neighborhood_intersects"),
    path("neighborhood/<int:pk>/",NycNeighborhoodDetail.as_view(),name="neighborhood"),
    path("streets/",NycStreetListCreateAPIView.as_view(),name="streets"),
    path("streetLength/",NycStreetLength.as_view(),name="street_length"),
    path("streetWithin/",NycStreetFilterWithin.as_view(),name="street_within"),
    path("streetGeom/", NycStreetGeometryValue.as_view(), name="street_geom"),
    path("streetTotalLength/", NycStreetTotalLength.as_view(), name="street_total_length"),
    path("streetIntersects/", NycStreetsIntersectMeridian.as_view(), name="street_intersects"),
    path("streetNearest/", NycStreetsNearest.as_view(), name="street_nearest"),
    path("streetNearestAll/", NycStreetsNearestAll.as_view(), name="street_nearest_all"),
    path("subwayStations/",NycSubwayStationsListCreateAPIView.as_view(),name="subway_stations"),
    path("subwayGeom/",NycSubwayGetGeog.as_view(),name="subway_geog"),
    path("neighborhoodInSubway/",FindNeighborhoodsInSubway.as_view(),name="neighborhood_in_subway"),
    path("neighborhoodTopoElements/", NycSharedTopoElements.as_view(), name="neighborhood_topo_elements"),
    path("neighborhoodTopoElementsView/", NycSharedTopoElementsAsView.as_view(), name="neighborhood_topo_elements_view"),
    path("censusSociodata/", NycCensusSociodataListCreateAPIView.as_view(), name="census_sociodata"),
    path("geometries/", GeometriesListCreateAPIView.as_view(), name="geometries"),
    path('censusBlocks/', include('census_blocks.urls')),
    path('map/streets/<int:id>/', streets.views.map_view, name='map_streets'),
    path('map/neigh/<int:id>/', neighborhoods.views.map_neigh_view, name='map_neigh'),
]
