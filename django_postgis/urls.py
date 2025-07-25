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
import subway_stations.views
from neighborhoods.views import NycNeighborhoodListCreateAPIView, NycNeighborhoodDetail, NycSharedTopoElementsAsView
from streets.views import NycStreetListCreateAPIView
from streets.views import NycStreetLength
from streets.views import NycStreetTotalLength
from streets.views import NycStreetFilterWithin
from streets.views import NycStreetGeometryValue
from streets.views import NycStreetsIntersectMeridian
from streets.views import NycStreetsNearest
from streets.views import NycStreetsNearestAll
from subway_stations.views import NycSubwayStationsListCreateAPIView, NycRoutesFromStations, NycPopulationFromTrainStop, \
    FindSubwaysInRoute
from subway_stations.views import FindNeighborhoodsInSubway
from subway_stations.views import NycSubwayGetGeog
from neighborhoods.views import NycNeighborhoodArea, NycNeighborhoodBoroArea
from neighborhoods.views import NycNeighborhoodIntersects
from neighborhoods.views import NycSharedTopoElements
from census_sociodata.views import NycCensusSociodataListCreateAPIView
from geometry.views import GeometriesListCreateAPIView, SimulazionePostAPIViewFutura
from geometry.views import GeometriesListSearchAPIView
from geometry.views import SimulazioneAPIView, SimulazionePostAPIView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_api_versioning.urls import urlpatterns as api_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("neighborhoods/",NycNeighborhoodListCreateAPIView.as_view(),name="neighborhoods"),
    path("neighborhoodArea/",NycNeighborhoodArea.as_view(),name="neighborhood_area"),
    path("neighborhoodBoroArea/",NycNeighborhoodBoroArea.as_view(),name="neighborhood_boro_area"),
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
    path("routesInSubway/",NycRoutesFromStations.as_view(),name="routes_subway"),
    path("subwaysInRoute/",FindSubwaysInRoute.as_view(),name="subways_route"),
    path("subwayPopulationTrainStop/<str:route>/",NycPopulationFromTrainStop.as_view(),name="subway_routes"),
    path("neighborhoodInSubway/",FindNeighborhoodsInSubway.as_view(),name="neighborhood_in_subway"),
    path("neighborhoodTopoElements/", NycSharedTopoElements.as_view(), name="neighborhood_topo_elements"),
    path("neighborhoodTopoElementsView/", NycSharedTopoElementsAsView.as_view(), name="neighborhood_topo_elements_view"),
    path("censusSociodata/", NycCensusSociodataListCreateAPIView.as_view(), name="census_sociodata"),
    path("geometries/", GeometriesListCreateAPIView.as_view(), name="geometries"),
    path("geometries/urlFutura/", SimulazioneAPIView().as_view(), name="esempio_non_implementata"),
    path("geometries/urlFuturaPost/", SimulazionePostAPIView().as_view(), name="esempio_post_non_implementata"),
    path("geometries/urlFuturaPostV2/", SimulazionePostAPIViewFutura().as_view(), name="esempio_post_non_implementata_v2"),
    path("geometries/<str:search>/", GeometriesListSearchAPIView.as_view(), name="geometries_search"),
    path('censusBlocks/', include('census_blocks.urls')),
    path('map/streets/<int:id>/', streets.views.map_view, name='map_streets'),
    path('map/neigh/<int:id>/', neighborhoods.views.map_neigh_view, name='map_neigh'),
    path('map/subway/<int:id>/', subway_stations.views.map_view, name='map_neigh'),
    path('', include(api_urlpatterns)),
]
